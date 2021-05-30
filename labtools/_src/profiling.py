# Copyright 2021 The LabTools Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
""" Profiler with opttional synchronizion of JAX ant Torch OPS if installed.

Example:
>>> import profiler from labtools 
... profiler.start('train', 'fetch_batch')
... for batch in batch_iter:
...    profiler.end('fetch_batch')
...    # forward pass
...    with profile_kv('forward'):
...      image_features = model.encode_image(images)
...    profiler.start('fetch_batch')
... profiler.end('train')
... profiler.log_profiles()
"""
from __future__ import annotations

import time
from collections import defaultdict
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Optional, Union

from absl import flags, logging

from labtools._src.util import maybe_import

Number = Union[int, float]

FLAGS = flags.FLAGS
flags.DEFINE_string('profiling', 'disabled', 'Profiling mode.')
flags.register_validator(
  'profiling', lambda value: value in ('disabled', 'enabled', 'strict'),
  flag_values=FLAGS)


class AverageMeter(object):
  """Computes and stores the average and current value"""

  __slots__ = ['val', 'avg', 'sum', 'count']

  def __init__(self):
    self.reset()

  def reset(self):
    self.val = 0
    self.avg = 0
    self.sum = 0
    self.count = 0

  def update(self, val: Number, n: Number = 1):
    self.val = val
    self.sum += val * n
    self.count += n
    self.avg = self.sum / self.count


def synchroized(fn: Callable, sync_in: bool = True,
                sync_out: bool = False) -> Callable:
  def _jax_blocker():
    return jax.jit(lambda x: jax.device_put(x))(0.0).block_until_ready()  # pytype: disable=attribute-error

  _sync_fns = []
  if (torch := maybe_import('torch')) is not None:
    _sync_fns.append(torch.cuda.synchronize)
  if (jax := maybe_import('jax')) is not None:
    _sync_fns.append(_jax_blocker)

  _sync_fn = lambda: [f() for f in _sync_fns]
  _sync_fn_in = _sync_fn if sync_in else lambda: []
  _sync_fn_out = _sync_fn if sync_out else lambda: []

  @wraps(fn)
  def _synchroized(*args, **kwargs):
    _sync_fn_in()
    out = fn(*args, **kwargs)
    _sync_fn_out()
    return out

  return _synchroized


class Singleton(type):
  _instances = {}

  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances[cls]


class Profiler(metaclass=Singleton):
  _mode: str = None
  start: Callable[[str], None]
  end: Callable[[str], None]

  def __init__(self, name='root', mode=None):

    self._incontext = None
    self._enabled = False
    self._default_name = name

    # initilize
    self.reset_timers()

    # init once app initialized
    if name == 'root' and mode is None:
      from absl import app
      from absl import flags as absl_flags
      app.call_after_init(lambda: self.complete_absl_config(absl_flags))
    else:
      self.toggle(mode)

  def reset_timers(self):
    self._prevtimes = defaultdict(lambda: time.time())
    self._starttimes = defaultdict(lambda: time.time())
    self._counters = defaultdict(lambda: AverageMeter())

  def complete_absl_config(self, absl_flags):
    self.toggle(absl_flags.FLAGS.profiling)

  @property
  def prev(self):
    return self._prev

  def toggle(self, mode: str):
    # noop
    if mode == self._mode:
      return
    self._mode = mode
    self._enabled = True
    if mode == 'strict':
      logging.info('Profiler set to strict mode, will synchronize Torch/Jax.')
      self.start = synchroized(self.__start)
      self.end = synchroized(self.__end)
    elif mode == 'enabled':
      logging.warning('Profiler not in strict mode, timings may be inaccurate.')
      self.start = self.__start
      self.end = self.__end
    elif mode == 'disabled':
      self.start = self.__passthrough
      self.end = self.__passthrough
      self._enabled = False
    else:
      raise ValueError('Mode %s not a valid profiling mode.' % mode)

  def enable(self, strict: bool = True):
    self.toggle(mode='strict' if strict else 'enabled')

  def disable(self):
    self.toggle(mode='disabled')

  def __start(self, *names: Optional[list[str]]):
    for name in names:
      name = name or self._default_name
      self._starttimes[name] = time.time()

  def __end(self, *names: Optional[list[str]]):
    curr = time.time()
    for name in names:
      elapsed = curr - self._starttimes[name]
      name = name or self._default_name
      # this mightv'e been the first use, if so do count it
      if elapsed > 0:
        self._counters[name].update(elapsed)
      else:
        logging.warning(
          'Attemting to call profiler.end() on unitiialized timer.')

  def __str__(self):
    out = f'Profiler results ({self._default_name})\n'
    if len(self._counters) > 0:
      if (tabulate := maybe_import('tabulate')):
        out += tabulate(self._counters, headers='keys')
      else:
        out += str(self._counters)
    return out

  def log_profiles(self, force: bool = False):
    if self._enabled or force:
      logging.info(str(self))

  def __passthrough(self, *args, **kwargs):
    return


# creat default profiler (singleton)
profiler = Profiler()


@contextmanager
def profile_kv(scopename, log=True):
  profiler.start(scopename)
  try:
    yield
  finally:
    profiler.end(scopename)


def profile(fn, n=None):
  """
    Usage:
    @profile("my_func")
    def my_func(): code
    """
  scopename = n or fn.__name__

  @wraps(fn)
  def wrapped_fn(*args, **kwargs):
    profiler.start(scopename)
    out = fn(*args, **kwargs)
    profiler.end(scopename)
    return out

  return wrapped_fn
