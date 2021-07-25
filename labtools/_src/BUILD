load("@rules_python//python:defs.bzl", "py_library", "py_test")

###############
# core libs.
#  These should only have internal deps. pip/external dependencies are commented
#  for documentation purposes only. This allows users to depend on labtools w/
#  bazel w/o having to match our specific versions. We should add version checks
#  somewhere if possible.

py_library(
    name = "config",
    srcs = ["config.py"],
    srcs_version = "PY3",
    visibility = ["//labtools:__pkg__"],
    deps = [
        "//labtools/_src:util",
        # pip: absl-py
    ],
)

py_library(
    name = "huggingface",
    srcs = ["huggingface.py"],
    srcs_version = "PY3",
    visibility = ["//labtools:__pkg__"],
    deps = [
        # pip: absl-py
    ],
)

py_library(
    name = "io",
    srcs = ["io.py"],
    srcs_version = "PY3",
    visibility = ["//labtools:__pkg__"],
    deps = [
        "//labtools/_src:util",
        # pip :toolz
    ],
)

py_library(
    name = "plotting",
    srcs = ["plotting.py"],
    srcs_version = "PY3",
    visibility = ["//labtools:__pkg__"],
    deps = ["//labtools/_src:util"],
)

py_library(
    name = "profiling",
    srcs = ["profiling.py"],
    srcs_version = "PY3",
    visibility = ["//labtools:__pkg__"],
    deps = [
        "//labtools/_src:util",
        # pip: absl-py
    ],
)

py_library(
    name = "util",
    srcs = ["util.py"],
    srcs_version = "PY3",
    visibility = ["//labtools:__pkg__"],
    deps = [
        # pip: absl-py
        # pip: toolz
    ],
)

################
# Tests
# unlike the core libs, these are not exported, and should reference all deps
# necessary to run. certain tests require additional packages to test specific
# features/codepaths. Ideally we could mock these somehow.
py_test(
    name = "config_test",
    srcs = ["config_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        "//labtools/_src:config",
        "@absl_archive//:absl",
        "@pip//:ml_collections",
        "@toolz_archive//:toolz",
    ],
)

py_test(
    name = "io_test",
    srcs = ["io_test.py"],
    python_version = "PY3",
    srcs_version = "PY3",
    deps = [
        "//labtools/_src:io",
        "@absl_archive//:absl",
        "@toolz_archive//:toolz",
    ],
)

py_test(
    name = "plotting_test",
    srcs = ["plotting_test.py"],
    data = ["//labtools:altair-saver-pdf-deps"],
    deps = [
        "//labtools/_src:plotting",
        "@absl_archive//:absl",
        "@pip//:altair",
        "@pip//:altair-saver",
    ],
)
