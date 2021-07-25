# Description:
#   A set of utility functions for iterators, functions, and dictionaries.
#   See the PyToolz documentation at https://toolz.readthedocs.io

load("@rules_python//python:defs.bzl", "py_library")

licenses(["notice"])  # New BSD

exports_files(["LICENSE"])

py_library(
    name = "toolz",
    srcs = glob(
        ["toolz/**/*.py"],
        exclude = [
            "**/test_*.py",
            "**/*_test.py",
        ],
    ),
    srcs_version = "PY3",
    visibility = ["//visibility:public"],
)
