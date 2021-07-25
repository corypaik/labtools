# Description:
#   MarkupSafe implements a text object that escapes characters so it is safe
#   to use in HTML and XML.

load("@rules_python//python:defs.bzl", "py_library")

licenses(["notice"])  # BSD

exports_files(["LICENSE"])

py_library(
    name = "markupsafe",
    srcs = glob(["src/markupsafe/**/*.py"]),
    imports = ["src"],
    srcs_version = "PY3",
    visibility = ["//visibility:public"],
)
