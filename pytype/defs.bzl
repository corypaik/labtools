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
""" PyType Integration Macros"""

load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")

def pytype_binary(name, pytype_deps = [], **kwargs):
    """Proxy for py_binary that implicitly creates a PyType test.

    Args:
       name: name for the py_binary rule.
       pytype_deps: a list of pytype-only deps
       **kwargs: Keyword arguments passed to pytype_genrunle
    """

    python_version = kwargs.pop("python_version", "PY3")
    srcs_version = kwargs.pop("srcs_version", "PY3")

    py_binary(
        name = name,
        python_version = python_version,
        srcs_version = srcs_version,
        **kwargs
    )
    pytype_genrunle(
        name = name,
        pytype_deps = pytype_deps,
        srcs_version = srcs_version,
        **kwargs
    )

def pytype_library(name, pytype_deps = [], **kwargs):
    """Proxy for py_library that implicitly creates a PyType test. 

    Args:
       name: name for the py_binary rule.
       pytype_deps: a list of pytype-only deps
       **kwargs: Keyword arguments passed to pytype_genrunle
    """
    srcs_version = kwargs.pop("srcs_version", "PY3")

    py_library(name = name, srcs_version = srcs_version, **kwargs)
    pytype_genrunle(
        name = name,
        pytype_deps = pytype_deps,
        srcs_version = srcs_version,
        **kwargs
    )

def pytype_test(name, main = None, **kwargs):
    """Proxy for py_test that implicitly creates a PyType test.

    Note:
      This is a placeholder, currently no pytype rules are created.
    Args:
      name: name for the py_test rule.
      main: main script to be run for the test.
      **kwargs: extra keyword arguments to the test.
    """
    if main == None:
        main = name + ".py"

    python_version = kwargs.pop("python_version", "PY3")
    srcs_version = kwargs.pop("srcs_version", "PY3")

    py_test(
        name = name,
        main = main,
        python_version = python_version,
        srcs_version = srcs_version,
        **kwargs
    )

def pytype_genrunle(
        name,
        pytype_deps,
        pytype_args = [
            "-x=external/",
            # "--config=external/labtools/pytype.cfg",
            # "--config=pytype.cfg",
            " .",
        ],
        **kwargs):
    """A macro that runs pytest tests by using a test runner.

    Args:
        name: A unique name for this rule.
        pytype_deps: a list of pytype-only deps
        pytype_args: a list of arguments passed to pytype
        **kwargs: are passed to py_test, with srcs and deps attrs modified
    """

    kwargs.pop("main", [])
    deps = kwargs.pop("deps", []) + ["@labtools//pytype:pytype_helper"]
    srcs = kwargs.pop("srcs", []) + ["@labtools//pytype:pytype_helper"]
    args = kwargs.pop("args", []) + pytype_args

    # add pytype tag
    tags = kwargs.pop("tags", []) + ["pytype"]

    # add pytype deps
    deps += pytype_deps

    py_test(
        name = "%s__pytype" % name,
        srcs = srcs,
        main = "pytype_helper.py",
        python_version = "PY3",
        deps = deps,
        args = args,
        tags = tags,
        **kwargs
    )
