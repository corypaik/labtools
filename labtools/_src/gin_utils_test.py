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
"""Tests for gin_utils.

This module was adapted from https://github.com/google-research/t5x in Oct. 2021
to be more portable. See `labtools._src.gin_utils` for more details.
"""

from absl.testing import absltest

from labtools._src.gin_utils import rewrite_gin_args


class GinUtilsTest(absltest.TestCase):

  def test_rewrite_gin_args(self):
    test_args = [
        '--gin_file=path/to/file',
        'gin.value=3',
        '--gin.value=3',
        '--gin.value="3"',
        '--gin.value=\'3\'',
        '--gin.tricky="key = value"',
        '--gin.dict={"foo": 4, "bar": "four"}',
        '--gin.gin=bar',
        '--gin.scope/foo=bar',
    ]
    expected_args = [
        '--gin_file=path/to/file',
        'gin.value=3',
        '--gin_bindings=value = 3',
        '--gin_bindings=value = "3"',
        '--gin_bindings=value = \'3\'',
        '--gin_bindings=tricky = "key = value"',
        '--gin_bindings=dict = {"foo": 4, "bar": "four"}',
        '--gin_bindings=gin = bar',
        '--gin_bindings=scope/foo = bar',
    ]
    self.assertSequenceEqual(rewrite_gin_args(test_args), expected_args)

  def test_rewrite_gin_args_malformed(self):
    test_args = ['--gin.value=3', '--gin.test']
    with self.assertRaisesWithLiteralMatch(
        ValueError,
        "Gin bindings must be of the form '--gin.<param>=<value>', got: "
        '--gin.test'):
      rewrite_gin_args(test_args)


if __name__ == '__main__':
  absltest.main()
