load("@bazel_skylib//rules:common_settings.bzl", "bool_flag")
load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:packaging.bzl", "py_wheel")
load("//pytype:defs.bzl", "pytype_library")

package(default_visibility = ["//visibility:private"])

pytype_library(
    name = "labtools",
    srcs = ["__init__.py"],
    srcs_version = "PY3",
    visibility = ["//visibility:public"],
    deps = [
        "//labtools/_src:config",
        "//labtools/_src:huggingface",
        "//labtools/_src:io_util",
        "//labtools/_src:plotting",
        "//labtools/_src:profiling",
        "//labtools/_src:util",
    ],
)

bool_flag(
    name = "include_py_deps",
    build_setting_default = False,
    visibility = ["//visibility:private"],
)

config_setting(
    name = "include_packaged_deps",
    flag_values = {":include_py_deps": "True"},
    visibility = ["//visibility:public"],
)

#################
# External deps.
#   It should not be necessary for users to depend on this library, as it just
#   packages 3rd-party pip/external dependencies. This allows users to depend on
#   labtools w/ bazel w/o having to match our specific versions. However, in
#   cases where the user is not using `toolz` or `absl-py` in their project,
#   they may wish to depend on `labtools_deps`.

# Minimal external deps necessary to use labtools.
py_library(
    name = "labtools_deps",
    srcs = [
        "@absl_archive//:absl",
        "@toolz_archive//:toolz",
    ],
    visibility = ["//visibility:public"],
)

# defines the necessary files to leverage altair-saver w/ pdf export.
filegroup(
    name = "altair-saver-pdf-deps",
    srcs = [
        "@labtools__npm//:node_modules/vega-cli/bin/vg2pdf",
        "@labtools__npm//canvas",
        "@labtools__npm//vega-cli",
        "@labtools__npm//vega-lite",
    ],
    visibility = ["//visibility:public"],
)

##############
# Distribution
##############

py_wheel(
    name = "wheel",
    distribution = "labtools",
    python_tag = "py3",
    version = "0.0.1.rc0",
    visibility = ["//visibility:public"],
    deps = [":labtools"],
)

filegroup(
    name = "distribution",
    srcs = glob(["**"]),
    visibility = ["//:__pkg__"],
)
