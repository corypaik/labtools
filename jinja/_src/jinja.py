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
""" Simple runner for jinja2.

Usage: python jinja.py [out_path] [template_path] [data_path]

NOTE:
  Only json data is supported. This script is meant only as an interface for the
  `jinja` rule in @labtools//jinja:defs.bzl.
"""

import json
from argparse import ArgumentParser
from pathlib import Path

from jinja2 import Template


def main(output_path, template_path, data_path):
  data = json.loads(Path(data_path).read_text())
  resolved = Template(Path(template_path).read_text()).render(data)
  Path(output_path).write_text(resolved)


if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('--template_path')
  parser.add_argument('--data_path')
  parser.add_argument('--output_path')
  args = parser.parse_args()
  main(**vars(args))
