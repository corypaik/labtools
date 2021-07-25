# Description:
#   enum34 provides a backport of the enum module for Python 2.
# Source:
#   https://github.com/abseil/abseil-py/blob/master/third_party/enum34.BUILD

load("@rules_python//python:defs.bzl", "py_library")

licenses(["notice"])  # MIT

exports_files(["LICENSE"])

py_library(
    name = "enum",
    srcs = ["enum34-1.1.6/enum/__init__.py"],
    srcs_version = "PY2AND3",
    visibility = ["//visibility:public"],
)
