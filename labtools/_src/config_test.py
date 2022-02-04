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
""" Provides tests for `labtools._src.config` """

from absl.testing import absltest
from absl.testing import parameterized
from ml_collections import ConfigDict
from ml_collections import FrozenConfigDict

from labtools._src.config import configurable
from labtools._src.config import frozen


class TestFrozen(parameterized.TestCase):
  """ Provides tests for the @frozen decorator """

  def test_frozen(self):
    config = ConfigDict()

    @frozen
    def basic_config_fn():
      return config

    frozen_config = basic_config_fn()

    self.assertEqual(frozen_config, FrozenConfigDict(config))


class TestConfigurable(absltest.TestCase):
  """ Tests for configurable decorator. """

  def test_configurable_minimal(self):
    """ Test configurable with no parameters """

    @configurable
    def dummy_func(x: str = 'hi', y: int = 1) -> int:
      return x, y

    # test it's callable
    self.assertEqual(dummy_func(), ('hi', 1))
    # and can be overridden with args.
    self.assertEqual(dummy_func('bye', 2), ('bye', 2))
    # and kwargs
    self.assertEqual(dummy_func(x='bye', y=2), ('bye', 2))

  def test_configurable_named(self):
    """ Test configurable with no parameters """

    @configurable('dummy', 'no')
    def dummy_func(x: str = 'hi', y: int = 1) -> int:
      return x, y

    # test it's callable
    self.assertEqual(dummy_func(), ('hi', 1))
    # and can be overridden with args.
    self.assertEqual(dummy_func('bye', 2), ('bye', 2))
    # and kwargs
    self.assertEqual(dummy_func(x='bye', y=2), ('bye', 2))


if __name__ == '__main__':
  absltest.main()
