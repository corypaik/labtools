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
from pathlib import Path
from typing import Union

from labtools._src.util import is_installed
from labtools._src.util import require


def setup_jupyter_env(ensure_project_root: Union[None, str] = 'WORKSPACE',
                      max_parents: int = 1):
  """  Setup a jupyter notebook environemnt.

  Args:
    ensure_project_root: File name that indicates the desired root. When using
      bazel this is usually the WORSPACE file. To disable this behavior, use
      ensure_project_root=None.
    max_parents: maximum number of parent directories to climb out of. This is a
      safegaurd against cd failures to find the specified file.

  Example:
    >>> import labtools
    ... from absl import logging
    ... labtools.setup_jupyter_env()
    ... logging.info('I work now!')
        12:00:00 ── INFO ▷ I work now!

  """
  import logging as py_logging
  import os
  import sys

  py_logging.basicConfig(format="%(asctime)s ── %(levelname)s ▷ %(message)s",
                         datefmt="%H:%M:%S",
                         handlers=[py_logging.StreamHandler(sys.stdout)])
  logging = py_logging.getLogger('absl')
  logging.setLevel('INFO')

  # check for a workspace file
  if ensure_project_root:
    og_pwd = os.getcwd()
    try:
      for pdepth in range(max_parents + 1):
        if Path(ensure_project_root).is_file():
          break
        os.chdir('..')
      else:
        logging.warning(
          'Failed to find %s in CWD at level=%d. PWD=%s, '
          'Original PWD=%s. Switching back to Original wd.',
          ensure_project_root, pdepth, os.getcwd(), og_pwd)
        # switch back as a safegaurd.
        os.chdir(og_pwd)
    except:
      logging.exception(
        'Failed to find %s in CWD at level=%d. PWD=%s, '
        'Original PWD=%s. Switching back to Original wd.', ensure_project_root,
        pdepth, os.getcwd(), og_pwd)
      os.chdir(og_pwd)


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
      r'^(.+)(bazel-out)\/\w+-fastbuild\/bin(.+)\/.+runfiles_manifest$',
      r'\1\2/results\3', mainfest_path)
    result_dir = result_dir

  return result_dir


@require('absl')
def configure_logging(third_party_offset: int = 0, **offsets):
  """ Configure logging formatters and levels

  Configures logging formatters and levels for absl and third party libraries.
  Default logging levels for external libraries:

    | --------------- | --------------------------------------------|
    | `transformers`  | FLAGS.verbosity - third_party_verbosity - 1 |
    | `datasets`      | FLAGS.verbosity - third_party_verbosity - 2 |

  Example:
    A verbosity of 0 (info) would result in a verbosity of warning for
    transformers and error for datasets.
  Args:
    third_party_offset: offset to add to all third party verbosity levels. For
      example, in a dristributied configuration, one could use a value of `0` on
      the main process and `1` on all other processes.
    **offset: offsets for third party libraries
  """
  import logging as py_logging
  import warnings

  from absl import logging
  from absl.flags import FLAGS
  from absl.logging.converter import absl_to_standard

  warnings.filterwarnings("ignore",
                          message='The given NumPy array is not writeable')

  logging.get_absl_handler().setFormatter(_logging_formatter())

  # default third party offsets
  default_offsets = {'transformers': 0, 'datasets': 1}
  offsets = {**default_offsets, **offsets}

  third_party_verbosity = FLAGS.verbosity - third_party_offset

  for name, offset in offsets.items():
    logger = py_logging.getLogger(name)
    # clip verbosity
    verbosity = max(third_party_verbosity - offset, logging.FATAL)
    logger.setLevel(absl_to_standard(verbosity))
    # apply format
    for handler in logger.handlers:
      handler.setFormatter(_logging_formatter())

  # ic only in debug if installed.
  if is_installed('icecream'):
    from icecream import ic
    if FLAGS.verbosity < 1:
      ic.disable()
    else:
      ic.configureOutput(includeContext=True)


def _logging_formatter():
  """ Logginging formatter """
  import logging as py_logging
  return py_logging.Formatter(
    fmt="%(asctime)s ── %(levelname)s ── %(name)s ▷ %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S")


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
