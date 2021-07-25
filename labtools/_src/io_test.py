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
import os.path as osp
from pathlib import Path

from absl.testing import absltest
from absl.testing import parameterized

from labtools._src import io


class JsonlTest(parameterized.TestCase):
  def test_dump_jsonl(self):
    data = [{'a': 0}, {'b': 1}, {'me': 'the'}]
    io.dump_jsonl(self.create_tempfile(), data)


if __name__ == '__main__':
  absltest.main()
