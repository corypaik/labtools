# Description:
#   Six provides simple utilities for wrapping over differences between Python 2
#   and Python 3.
# Source:
#   https://github.com/abseil/abseil-py/blob/master/third_party/six.BUILD

load("@rules_python//python:defs.bzl", "py_library")

licenses(["notice"])  # MIT

exports_files(["LICENSE"])

py_library(
    name = "six",
    srcs = ["six.py"],
    srcs_version = "PY2AND3",
    visibility = ["//visibility:public"],
)
