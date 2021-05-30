# Copyright 2021 The LabTools Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
""" A low dependence collection of general utilities. 
  
  This file relies on third-party packages for specfic fucnctionalities. Some 
  of these are givens, e.g. you won't need to convert Torch Tensors -> lists 
  unless PyTorch is installed. Others, such as loading yml files, do require 
  specific packages. See the error messages or `@require('<pkg>')` decorators 
  for details on what packeges are required.
"""
from __future__ import annotations

import gc
import hashlib
import importlib
import inspect
import json
import time
from collections import OrderedDict
from collections.abc import MutableMapping, Sequence
from contextlib import contextmanager
from functools import lru_cache, wraps
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Literal, Tuple, TypeVar, Union, overload

import toolz.curried as T
from absl import flags, logging

El = TypeVar('El')

FLAGS = flags.FLAGS


@lru_cache(maxsize=None)
def maybe_import(name: str) -> Union[ModuleType, None]:
  return importlib.import_module(name) if is_installed(name) else None


@lru_cache(maxsize=None)
def is_installed(name: str) -> bool:
  return importlib.util.find_spec(name) is not None


def require(name: str):
  """Create a decorator to check if a package is installed. """
  msg = '%s requires %s, but it is not installed.'

  def wrapped_with_params(fn):
    @wraps(fn)
    def _require(*args, **kwargs):
      if is_installed(name):
        return fn(*args, **kwargs)
      else:
        raise ImportError(msg % (fn.__name__, name))

    return _require

  return wrapped_with_params


@contextmanager
def catch_exp_failures(name: str, verbose: bool = True):
  """ Context manager for catching experiment failures. 

    This context manager will ignore all exceptions within context except 
    Keyboard Interrupts and is useful for running sets of experiments. Failed
    experiments will be logged to stderr (absl) and skipped. If torch is 
    installed, we empty the catch on exit of the context manager. We also run 
    Garbage collection. This should cleanup most GPU allocations, and is known 
    to work with Jax, PyTorch, and DALI.

    Examples:
      >>> with catch_exp_failures('Model'):
      ...   lambda : raise RuntimeError
      Failed to run Model after * s. Skipping...
      >>> with catch_exp_failures('Model'):
      ...   lambda : None
      Succesfully ran Model in * s.

    Args:
      name: Name of the experiment
      verbose: Predicate indicating whether to log details about timing 
        information of the experiment on success.
  """
  tick = time.time()
  try:
    yield
    if verbose:
      logging.info('Succesfully ran %s in %0.3d s.', name, time.time() - tick)
  # fail on KeyboardInterrupt
  except KeyboardInterrupt:
    logging.info('Detected KeyboardInterrupt, exiting.')
    import os
    os._exit(1)
  # catch other errors
  except Exception:
    logging.exception('Failed to run %s after %s s. Skipping...', name,
                      time.time() - tick)
  finally:
    # maybe emty torch cuda cache
    if (torch := maybe_import('torch')) is not None:
      torch.cuda.empty_cache()
    gc.collect()


def topylist(x) -> list:
  x_type = str(type(x))
  if x_type == '<class \'torch.Tensor\'>':
    x = x.tolist()
  elif x_type.endswith('DeviceArray\'>'):
    onp = maybe_import('numpy')
    if onp is not None:
      x = onp.asarray(x).tolist()
  else:
    try:
      x = x.tolist()
    except:
      pass
  return x


def compute_obj_hash(obj) -> str:
  """ computes the hash of an object."""
  str_obj = json.dumps(obj, cls=BestEffortJSONEncoder, sort_keys=True)
  return hashlib.sha256(str_obj.encode('utf-8')).hexdigest()


class CustomJSONEncoder(json.JSONEncoder):
  """JSON encoder w/ support for ConfigDicts, Paths, and Arrays.
  Note:
    This is based off of ml_collections.CustomJSONEncoder, with added support 
    for Paths and Arrays (it also doesn't requrie ml_collections)
  """
  def default(self, obj):
    # maybe handle config dicts

    if (ml_collections := maybe_import('ml_collections')):
      if isinstance(obj, ml_collections.FieldReference):
        return obj.get()
      elif isinstance(obj, ml_collections.ConfigDict):
        return obj._fields
    # paths
    if isinstance(obj, Path):
      return str(obj)
    # lists
    else:
      obj = topylist(obj)
      if isinstance(obj, list):
        return obj
      raise TypeError(
        '{} is not JSON serializable. Instead use cls=BestEffortJSONEncoder'
        .format(type(obj)))


class BestEffortJSONEncoder(CustomJSONEncoder):
  """Best Effort JSON encoder (won't throw errors).
  Source:
    ml_collections._BestEffortCustomJSONEncoder
  """
  def default(self, obj):
    try:
      return super(BestEffortJSONEncoder, self).default(obj)
    except TypeError:
      if isinstance(obj, set):
        return sorted(list(obj))
      elif inspect.isfunction(obj):
        return 'function {}'.format(obj.__name__)
      elif (hasattr(obj, '__dict__') and obj.__dict__
            and not inspect.isclass(obj)):  # Instantiated object's variables
        return dict(obj.__dict__)
      elif hasattr(obj, '__str__'):
        return 'unserializable object: {}'.format(obj)
      else:
        return 'unserializable object of type: {}'.format(type(obj))


@overload
def ensure_listlike(x: Sequence[El]) -> Sequence[El]:
  ...


@overload
def ensure_listlike(x: str) -> list[str]:
  ...


@overload
def ensure_listlike(x: El) -> list[El]:
  ...


def ensure_listlike(x):
  return x if isinstance(x, Sequence) and not isinstance(x, str) else [x]


def __check_arg_lens(args):
  args = list(map(list, args))
  n = len(args[0])
  for arg in args[1:]:
    assert len(arg) == n, 'length mismatch: {}'.format(list(map(len, args)))


def safe_zip(*args):
  __check_arg_lens(args)
  return list(zip(*args))


def safe_map(f: Callable, *args):
  __check_arg_lens(args)
  return list(map(f, *args))


def unzip(obj):
  return list(zip(*obj))


@overload
def flatten_dict(d: dict[str, Any], parent_key: str = '', sep: str = '/',
                 sort: Literal[True] = True) -> OrderedDict:
  ...


@overload
def flatten_dict(d: dict[str, Any], parent_key: str = '', sep: str = '/',
                 sort: Literal[False] = True) -> dict:
  ...


def flatten_dict(d, parent_key, sep, sort=True):
  items = []
  for k, v in d.items():
    new_key = parent_key + sep + k if parent_key else k
    if isinstance(v, MutableMapping):
      items.extend(flatten_dict(v, new_key, sep=sep, sort=False).items())
    else:
      items.append((new_key, v))
  return OrderedDict(sorted(items, key=lambda x: x[0])) if sort else dict(items)


def split_by_keys(obj: dict[str, El],
                  keys: list[str]) -> Tuple[dict[str, El], dict[str, El]]:
  # split dict into 2, where first only contains keys in `keys`.
  return {k: obj.pop(k) for k in keys}, obj


@require('numpy')
def get_differences(x, y) -> str:
  """ Get differences of arrays (for debugging)

  Source:
  https://github.com/numpy/numpy/blob/6ee49178517088966e63c2aedf6a8a5779ad5384/numpy/testing/_private/utils.py#L828
  """
  import numpy as np

  remarks = []
  error = np.abs(x - y)
  max_abs_error = np.max(error)
  remarks.append('Max absolute difference: %f' % max_abs_error)

  # note: this definition of relative error matches that one
  # used by assert_allclose (found in np.isclose)
  # Filter values where the divisor would be zero
  nonzero = np.bool_(y != 0)
  if np.all(~nonzero):
    max_rel_error = np.array(np.inf)
  else:
    max_rel_error = np.max(error[nonzero] / np.abs(y[nonzero]))
  remarks.append('Max relative difference: %f' % max_rel_error)
  return '\n'.join(remarks)
