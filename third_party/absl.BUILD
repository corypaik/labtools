# Description:
#   Abseil Python Common Libraries, see https://github.com/abseil/abseil-py.

load("@rules_python//python:defs.bzl", "py_library")

licenses(["notice"])  # Apache 2.0

exports_files(["LICENSE"])

py_library(
    name = "absl",
    srcs = [
        "//absl:__init__.py",
        "//absl:app",
        "//absl/flags",
        "//absl/logging",
        "//absl/testing:absltest",
        "//absl/testing:flagsaver",
        "//absl/testing:parameterized",
    ],
    srcs_version = "PY2AND3",
    visibility = ["//visibility:public"],
)
