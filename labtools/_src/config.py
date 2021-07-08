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

from __future__ import annotations

import re
from functools import wraps

from absl import flags, logging

from labtools._src.util import is_installed, require

FLAGS = flags.FLAGS


def setup_jupyter_env():
  """ Sets up a jupyter notebook environment.

  FOr now this simply sets up basic logging.

  Example:
    >>> import labtools
    ... from absl import logging
    ... labtools.setup_jupyter_env()
    ... logging.info('I work now!')
        12:00:00 ── INFO ▷ I work now!
  """
  import logging as py_logging
  import sys

  py_logging.basicConfig(format="%(asctime)s ── %(levelname)s ▷ %(message)s",
                         datefmt="%H:%M:%S",
                         handlers=[py_logging.StreamHandler(sys.stdout)])
  logging = py_logging.getLogger('absl')
  logging.setLevel('INFO')


def get_results_dir(default_prefix: str = 'default') -> str:
  """ Get the Bazel Result Path
    Results stored in _bazel/out/results/<loc> where <loc> is the relative path
    in the source tree.
    For example, if the binary is in `projects/my_project/run.py`, then the
    results_dir would be `_bazel/out/results/projects/my_project`.
    This ensures that results are easily accesable between runs and from the
    workspace. Note that these files will still be cleaned up by `bazel clean`.

  Args:
    default_prefix: tmp dir prefix to use if not ran with Bazel

  """
  import os
  mainfest_path = os.getenv('RUNFILES_MANIFEST_FILE', None)
  result_dir = f'/tmp/{default_prefix}-results'
  if mainfest_path is not None:
    result_dir = re.sub(
      r'^(.+)(bazel-out)\/k8-fastbuild\/bin(.+)\/.+runfiles_manifest$',
      r'\1\2/results\3', mainfest_path)
    result_dir = result_dir

  return result_dir


def configure_logging():
  import logging as py_logging
  import warnings

  warnings.filterwarnings("ignore",
                          message='The given NumPy array is not writeable')

  logging.get_absl_handler().setFormatter(
    py_logging.Formatter(
      fmt="%(asctime)s ── %(levelname)s ── %(name)s ▷ %(message)s",
      datefmt="%m/%d/%Y %H:%M:%S"))

  # ic only in debug if installed.
  if is_installed('icecream'):
    from icecream import ic
    if FLAGS.verbosity < 1:
      ic.disable()
    else:
      ic.configureOutput(includeContext=True)


@require('ml_collections')
def frozen(fn):
  """ Wrapper to freeze a configuration function.
    Args:
      fn (Callable[[], ConfigDict]): configuration function

    Returns:
      FrozenConfigDict
  """
  from ml_collections import FrozenConfigDict

  @wraps(fn)
  def wrapped(*args, **kwargs):
    return FrozenConfigDict(fn(*args, **kwargs))

  return wrapped
