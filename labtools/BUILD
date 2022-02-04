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

load("@rules_python//python:defs.bzl", "py_library")

package_group(
    name = "internal",
    packages = [
        "//labtools/...",
    ],
)

py_library(
    name = "labtools",
    srcs = ["__init__.py"],
    imports = [".."],
    srcs_version = "PY3",
    visibility = ["//visibility:public"],
    deps = [
        "//labtools/_src:config",
        "//labtools/_src:huggingface",
        "//labtools/_src:io_util",
        "//labtools/_src:profiling",
        "//labtools/_src:util",
    ],
)

py_library(
    name = "experimental",
    srcs = ["experimental.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":labtools",
        "//labtools/_src:config",
        "//labtools/_src:io_util",
    ],
)

py_library(
    name = "testing",
    srcs = ["testing.py"],
    visibility = ["//visibility:public"],
    deps = [
        ":labtools",
        "//labtools/_src/testing:_testcase",
    ],
)

py_library(
    name = "config",
    srcs = ["config.py"],
    imports = [".."],
    visibility = ["//visibility:public"],
    deps = [
        ":labtools",
        "//labtools/_src:gin_utils",
    ],
)
