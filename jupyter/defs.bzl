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
""" Jupyter Integration Macros """

load("@rules_python//python:defs.bzl", "py_binary")
load("//tools:defs.bzl", "clean_dep")

def jupyterlab_server(name = "jupyterlab", **kwargs):
    """ A macro for creating a Jupyterlab Server.

    Args:
      name: A unique name for this rule.
      **kwargs: are passed to py_binary, with srcs and deps attrs modified
    """

    deps = kwargs.pop("deps", []) + [clean_dep("//jupyter:jupyterlab_helper")]
    srcs = kwargs.pop("srcs", []) + [clean_dep("//jupyter:jupyterlab_helper")]

    # patch env
    env = kwargs.pop("env", {})

    # env['JUPYTERLAB_DIR'] = "$(RUNFILES_DIR)/pypi__jupyterlab/jupyterlab"
    # print(env['JUPYTERLAB_DIR'])
    py_binary(
        name = name,
        srcs = srcs,
        deps = deps,
        main = "jupyterlab_helper.py",
        env = env,
        **kwargs
    )
