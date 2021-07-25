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

from pathlib import Path

from absl import flags
from absl import logging
from absl.testing import absltest
from absl.testing import parameterized
from ml_collections import ConfigDict
from ml_collections import FrozenConfigDict

from labtools._src.config import frozen
from labtools._src.config import get_results_dir

FLAGS = flags.FLAGS


class TestResultsDir(parameterized.TestCase):
  @parameterized.named_parameters(
    ('darwin', 'darwin'),
    ('linux', 'k8'),
  )
  def test_get_results_dir_manifest(self, bc_prefix):
    """ Check bazel behavior (with manifest) """
    from os import environ

    bazel_out_root = Path(self.create_tempdir(), 'bazel-out')
    runfiles_bcd = bazel_out_root / f'{bc_prefix}-fastbuild'
    runfiles_manifest_fpath = runfiles_bcd / 'bin/src/run.runfiles_manifest'
    environ['RUNFILES_MANIFEST_FILE'] = str(runfiles_manifest_fpath)

    results_dir = get_results_dir()
    expected_results_dir = str(bazel_out_root / 'results/src')
    self.assertEqual(results_dir, expected_results_dir)

  @parameterized.named_parameters(
    ('default', 'default'),
    ('as_kwarg', 'where'),
  )
  def test_get_results_dir_no_manifest(self, prefix):
    """ Check non-bazel behavior (no manifest) """
    from os import environ
    manifest_fpath = environ.get('RUNFILES_MANIFEST_FILE')
    del environ['RUNFILES_MANIFEST_FILE']
    # check non
    results_dir = get_results_dir(default_prefix=prefix)
    expected_results_dir = f'/tmp/{prefix}-results'

    self.assertEqual(results_dir, expected_results_dir)

    environ['RUNFILES_MANIFEST_FILE'] = manifest_fpath


class TestFrozen(parameterized.TestCase):
  def test_frozen(self):
    config = ConfigDict()

    @frozen
    def basic_config_fn():
      return config

    frozen_config = basic_config_fn()

    self.assertEqual(frozen_config, FrozenConfigDict(config))


if __name__ == '__main__':
  absltest.main()
