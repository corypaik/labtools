load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:packaging.bzl", "py_wheel")

package(default_visibility = ["//visibility:private"])

py_library(
    name = "labtools",
    srcs = ["__init__.py"],
    srcs_version = "PY3",
    visibility = ["//visibility:public"],
    deps = [
        "//labtools/_src:config",
        "//labtools/_src:huggingface",
        "//labtools/_src:io",
        "//labtools/_src:plotting",
        "//labtools/_src:profiling",
        "//labtools/_src:util",
    ],
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
        "@labtools__yarn//:node_modules/vega-cli/bin/vg2pdf",
        "@labtools__yarn//canvas",
        "@labtools__yarn//vega-cli",
        "@labtools__yarn//vega-lite",
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
