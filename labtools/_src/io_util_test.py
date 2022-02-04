# Copyright 2021 Cory Paik. All Rights Reserved.
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
""" Provides tests for `labtools._src.io_util` """

import os

from absl.testing import absltest
from absl.testing import parameterized
from fsspec.registry import known_implementations

from labtools._src.io_util import _download_file
from labtools._src.io_util import download_files
from labtools._src.io_util import dump_jsonl
from labtools._src.io_util import resolve_path


class JsonlTest(parameterized.TestCase):

  def test_dump_jsonl(self):
    data = [{'a': 0}, {'b': 1}, {'me': 'the'}]
    dump_jsonl(self.create_tempfile(), data)


class DownloadFilesTest(parameterized.TestCase):

  def test__download_file(self):
    p = self.create_tempfile()
    url = 'https://dummyimage.com/600x400/000/fff'
    res = _download_file((url, p))
    # Check success.
    self.assertEqual(res, (1, None))

  def test_download_files(self):
    download_dir = self.create_tempdir()
    n = 10
    tasks = [{
        'filename': str(i),
        'url': url
    } for i, url in enumerate(['https://dummyimage.com/600x400/000/fff'] * n)]

    num_completed = download_files(tasks, download_dir)
    self.assertEqual(num_completed, n)

    # Default clobber=False should now download 0 files.
    num_completed = download_files(tasks, download_dir)
    self.assertEqual(num_completed, 0)

  @parameterized.parameters(
      (
          'bazel::rf://labtools/labtools/__init__.py',
          os.path.join(os.path.dirname(__file__), '../__init__.py'),
      ),)
  def test_resolve_path_runfiles(self, path, expected):
    res = resolve_path(path)
    # For runfiles paths, we have to use relative paths for expected. So we must
    # first resolve the path. It is expected that res will already be resolved
    # for us.
    expected = os.path.normpath(expected)
    self.assertEqual(res, expected)

  @parameterized.named_parameters(
      ('workspace', 'BUILD_WORKSPACE_DIRECTORY', 'bazel::ws://'),
      ('workdir', 'BUILD_WORKING_DIRECTORY', 'bazel::wd://'),
  )
  def test_resolve_path_env(self, env_key, prefix):
    """ Checks workspace-relative path resolution.

    Note that `BUILD_WORKSPACE_DIRECTORY` and `BUILD_WORKING_DIRECTORY` are
    not present during tests, so here we just define temporary directories as
    the environment variables and check that `resolved_path` returns the
    appropriate location.
    """
    td = self.create_tempdir()
    os.environ[env_key] = td.full_path
    path = 'my_great_important-file.txt'
    res = resolve_path(prefix + path)
    expected = os.path.join(td.full_path, path)
    self.assertEqual(res, expected)
    del os.environ[env_key]

  def test_resolve_path_local(self):
    td = self.create_tempdir()
    path = os.path.join(td, '..', 'my_great_important-file.txt')
    res = resolve_path(path)
    expected = os.path.normpath(path)
    self.assertEqual(res, expected)

  @parameterized.parameters(*known_implementations)
  def test_ignore_fsspec_protocols(self, protocol):
    """ Tests that we don't conflict with fsspec protocols """
    td = self.create_tempdir()
    path = 'my_great_important-file.txt'
    full_path = f'{protocol}://{td.full_path}{path}'
    res = resolve_path(full_path)
    self.assertEqual(res, full_path)


if __name__ == '__main__':
  absltest.main()
