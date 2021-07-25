# Copyright 2021 The LabTools Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
""" Bazel rule for filling templates with Jinja2

This file is deprecated; please use the exports in defs.bzl instead.
"""

load("//jinja:defs.bzl", _jinja = "jinja")

def jinja(**kwargs):
    """ Deprecated jinja import location. """

    # buildifier: disable=print
    print("DEPRECATED: the jinja rule has been moved to //jinja:defs.bzl. " +
          "Please use: load(\"@labtools//jinja:defs.bzl\", \"jinja\") instead.")
    _jinja(**kwargs)
