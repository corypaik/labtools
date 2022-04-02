# Copyright 2021 The T5X Authors.
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
"""Utilities for using gin configurations with T5X binaries.

This module was adapted from https://github.com/google-research/t5x in Oct. 2021
to be more portable. The original depended on tensorflow, jax, and others. This
module retains the same functionality while only requiring the installation of
fsspec.

Note that certain functionalities may be limited depending on what you have
installed, as fsspec only supports certain backends with additional packages.
For GCS (supported by tensorflow) you'll need to also install gsspec.
See the github for more info: https://github.com/fsspec
"""
import inspect
import os
from typing import Any, Callable, List, Optional, Sequence, TypeVar

from absl import app
from absl import flags
from absl import logging
from fsspec.core import get_filesystem_class
from fsspec import filesystem
import gin

from labtools._src.util import maybe_import

T = TypeVar('T')
flags.disclaim_key_flags()


def register_gin_flags(module_name: Optional[str] = 'labtools.config',
                       use_caller_module_name: bool = False,
                       **kwargs):
  """ Register flags for parsing the gin configuration

  Args:
    module_name: By default the module name for these flags will be set to
      `labtools.config`, and will only show up in the help output if you
      use the flag --helpfull. You can manually set this to a specific value.
    use_caller_module_for_gin_flags: Predicate indicating that we should ignore
      `module_name` and set the flag's `module_name` to None. Set this to `True`
      if you would like the flags to be declared as if you defined them from
      the calling module (e.g., so they also show up in --help).
  """
  if use_caller_module_name:
    module_name = None

  flags.DEFINE_multi_string(
      'gin_file',
      default=None,
      help='Path to gin configuration file. Multiple paths may be passed and '
      'will be imported in the given order, with later configurations  '
      'overriding earlier ones.',
      module_name=module_name,
      **kwargs)

  flags.DEFINE_multi_string('gin_bindings',
                            default=[],
                            help='Individual gin bindings.',
                            module_name=module_name,
                            **kwargs)

  flags.DEFINE_list(
      'gin_search_paths',
      default=['.'],
      help='Comma-separated list of gin config path prefixes to be prepended '
      'to suffixes given via `--gin_file`. If a file appears in. Only the '
      'first prefix that produces a valid path for each suffix will be '
      'used.',
      module_name=module_name,
      **kwargs)


def parse_gin_flags(gin_search_paths: Sequence[str],
                    gin_files: Sequence[str],
                    gin_bindings: Sequence[str],
                    skip_unknown: bool = False,
                    finalize_config: bool = True):
  """Parses provided gin files override params.

  Args:
    gin_search_paths: paths that will be searched for gin files.
    gin_files: paths to gin config files to be parsed. Files will be parsed in
      order with conflicting settings being overridden by later files. Paths may
      be relative to paths in `gin_search_paths`.
    gin_bindings: individual gin bindings to be applied after the gin files are
      parsed. Will be applied in order with conflicting settings being
      overridden by later ones.
    skip_unknown: whether to ignore unknown bindings or raise an error (default
      behavior).
    finalize_config: whether to finalize the config so that it cannot be
      modified (default behavior).
  """
  # Register .gin file search paths with gin
  for gin_file_path in gin_search_paths:
    gin.add_config_file_search_path(gin_file_path)

  # Parse config files and bindings passed via flag.
  gin.parse_config_files_and_bindings(gin_files,
                                      gin_bindings,
                                      skip_unknown=skip_unknown,
                                      finalize_config=finalize_config)
  logging.info('Gin Configuration:\n%s', gin.config_str())


def rewrite_gin_args(args: Sequence[str]) -> Sequence[str]:
  """Rewrite `--gin.NAME=VALUE` flags to `--gin_bindings=NAME=VALUE`."""

  def _rewrite_gin_arg(arg):
    if not arg.startswith('--gin.'):
      return arg
    if '=' not in arg:
      raise ValueError(
          "Gin bindings must be of the form '--gin.<param>=<value>', got: " +
          arg)
    # Strip '--gin.'
    arg = arg[6:]
    name, value = arg.split('=', maxsplit=1)
    r_arg = f'--gin_bindings={name} = {value}'
    print(f'Rewritten gin arg: {r_arg}')
    return r_arg

  return [_rewrite_gin_arg(arg) for arg in args]


@gin.register
def summarize_gin_config(model_dir: str, summary_writer, step: int):
  """Writes gin config to the model dir and TensorBoard summary."""
  jax = maybe_import('jax')
  if jax and jax.host_id() == 0:
    config_str = gin.config_str()
    # Attempt to get the correct fsspec protocol.
    try:
      fs = get_filesystem_class(model_dir)
    except:  # pylint: disable=bare-except
      logging.warning(
          'Failed to retrive filespec for specified protocol, '
          'saving locally instead (model_dir=%s)', model_dir)
      fs = filesystem('file')

    fs.makedirs(model_dir, exist_ok=True)

    # Write the config as JSON.
    with fs.open(os.path.join(model_dir, 'config.gin'), 'w') as f:
      f.write(config_str)
    # Include a raw dump of the json as a text summary.
    if summary_writer is not None:
      summary_writer.write_texts(step, {'config': gin.markdown(config_str)})
      summary_writer.flush()


def run(main):
  """Wrapper for app.run that rewrites gin args before parsing."""
  app.run(
      main,
      flags_parser=lambda a: app.parse_flags_with_usage(rewrite_gin_args(a)))


def configure_and_run(run_fn: Callable[[Any], T],
                      default_gin_search_paths: Optional[List[str]] = None,
                      **kwargs) -> T:
  """ Wrapper to setup gin configuration and run run_fn

  Example:
    Suppose we want to confiigure some training function `train`, we can setup
    our main script to look like this:

    >>> def train(name, learning_rate=1e-3):
    ...    ...
    ... if __name__ == '__main__':
    ...    labtools.config.configure_and_run(train)

    This will add the flags --gin_file, --gin_bindings, and --gin_search_paths
    which can be used to configure `train`.

  Args:
    run_fn: The function to configure and run. It can be parameterized using
      it's original name.
    default_gin_search_paths: Defaults path relative to which we should look
      for configuration files. If None, then will set the default search paths
      relative to `dirname(run_fn.__file__)`
    kwargs: Additional keyword arguments to forward to
      `labtools.config.register_gin_flags`.

  Returns:
    Returns the output of run_fn. Typically run_fn is the main function but this
    can be useful for verifying results during testing.

  """
  register_gin_flags(**kwargs)
  del kwargs

  # Automatically search for gin files relative to the project
  if default_gin_search_paths is None:
    default_gin_search_paths = [os.path.dirname(inspect.getabsfile(run_fn))]

  def main(argv: Sequence[str]):
    """Wrapper for pdb post mortems."""
    return _main(argv)

  def _main(argv: Sequence[str]):
    """True main function."""
    if len(argv) > 1:
      raise app.UsageError('Too many command-line arguments.')

    # Create gin-configurable version of `run_fn`.
    run_fn_using_gin = gin.configurable(run_fn)

    parse_gin_flags(
        # User-provided gin paths take precedence if relative paths conflict.
        flags.FLAGS.gin_search_paths + default_gin_search_paths,
        flags.FLAGS.gin_file,
        flags.FLAGS.gin_bindings)

    # Run under gin
    return run_fn_using_gin()

  return run(main)


# ====================== Configurable Utility Functions ======================


@gin.configurable
def sum_fn(var1=gin.REQUIRED, var2=gin.REQUIRED):
  """sum function to use inside gin files."""
  return var1 + var2


@gin.configurable
def bool_fn(var1=gin.REQUIRED):
  """bool function to use inside gin files."""
  return bool(var1)
