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
load("@rules_python//python:defs.bzl", "py_library", "py_test")

package(default_visibility = ["//labtools:internal"])

py_library(
    name = "config",
    srcs = ["config.py"],
    imports = ["../.."],
    deps = [
        ":util",
        "@pypi_absl_py//:pkg",
    ],
)

py_library(
    name = "huggingface",
    srcs = ["huggingface.py"],
    imports = ["../.."],
    deps = [
        "@pypi_absl_py//:pkg",
    ],
)

py_library(
    name = "io_util",
    srcs = ["io_util.py"],
    imports = ["../.."],
    deps = [
        ":util",
        "@pypi_absl_py//:pkg",
        "@pypi_cytoolz//:pkg",
        "@pypi_requests//:pkg",
        "@rules_python//python/runfiles",
    ],
)


py_library(
    name = "profiling",
    srcs = ["profiling.py"],
    imports = ["../.."],
    deps = [
        ":util",
        "@pypi_absl_py//:pkg",
    ],
)

py_test(
    name = "profiling_test",
    srcs = ["profiling_test.py"],
    deps = [
        ":profiling",
        "@pypi_absl_py//:pkg",
    ],
)

py_library(
    name = "util",
    srcs = ["util.py"],
    imports = ["../.."],
    deps = [
        "@pypi_absl_py//:pkg",
        "@pypi_cytoolz//:pkg",
    ],
)

py_test(
    name = "config_test",
    srcs = ["config_test.py"],
    deps = [
        ":config",
        "@pypi_absl_py//:pkg",
        "@pypi_cytoolz//:pkg",
        "@pypi_fancyflags//:pkg",
        "@pypi_ml_collections//:pkg",
    ],
)

py_test(
    name = "io_util_test",
    srcs = ["io_util_test.py"],
    deps = [
        ":io_util",
        "@pypi_absl_py//:pkg",
        "@pypi_fsspec//:pkg",
    ],
)

py_library(
    name = "gin_utils",
    srcs = ["gin_utils.py"],
    imports = ["../.."],
    deps = [
        ":util",
        "@pypi_absl_py//:pkg",
        "@pypi_fsspec//:pkg",
        "@pypi_gin_config//:pkg",
    ],
)

py_test(
    name = "gin_utils_test",
    srcs = ["gin_utils_test.py"],
    main = "gin_utils_test.py",
    deps = [
        ":gin_utils",
        "@pypi_absl_py//:pkg",
    ],
)
