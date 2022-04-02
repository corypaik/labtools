# Copyright 2022 Cory Paik. All Rights Reserved.
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
"""Provides import tests for the labtools package."""
from absl.testing import absltest

import labtools


class TestLabtoolsImport(absltest.TestCase):

  def test_import_labtools_all_valid(self):

    for modname in labtools.__all__:
      with self.subTest(f'labtools.{modname}'):
        self.assertIn(modname, dir(labtools),
                      f'Expected labtools to export {modname}')


if __name__ == '__main__':
  absltest.main()
