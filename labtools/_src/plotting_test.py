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

import altair as alt
from absl.testing import absltest
from absl.testing import parameterized

from labtools._src import plotting


def make_chart():
  """ Make a simple altair chart

  Source: https://altair-viz.github.io/user_guide/internals.html
  """
  return alt.Chart.from_dict({
    "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
    "description": "A simple bar chart with embedded data.",
    "data": {
      "values": [{
        "a": "A",
        "b": 28}, {
          "a": "B",
          "b": 55}, {
            "a": "C",
            "b": 43}, {
              "a": "D",
              "b": 91}, {
                "a": "E",
                "b": 81}, {
                  "a": "F",
                  "b": 53}, {
                    "a": "G",
                    "b": 19}, {
                      "a": "H",
                      "b": 87}, {
                        "a": "I",
                        "b": 52}]},
    "mark": "bar",
    "encoding": {
      "x": {
        "field": "a",
        "type": "ordinal"},
      "y": {
        "field": "b",
        "type": "quantitative"}}})


class PlottingTest(parameterized.TestCase):
  def test_altair_saver(self):
    altair_saver = plotting.altair_saver()
    chart = make_chart()
    tempdir = self.create_tempdir()
    altair_saver.save(chart, osp.join(tempdir, 'out.pdf'))
    print(list(Path().iterdir()))


if __name__ == '__main__':
  absltest.main()
