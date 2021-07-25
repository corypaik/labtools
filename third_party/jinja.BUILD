# Description:
#   Jinja is a fast, expressive, extensible templating engine. Special
#   placeholders in the template allow writing code similar to Python syntax.
#   Then the template is passed data to render the final document.

load("@rules_python//python:defs.bzl", "py_library")

licenses(["notice"])  # BSD

exports_files(["LICENSE"])

py_library(
    name = "jinja2",
    srcs = glob(["src/jinja2/**/*.py"]),
    imports = ["src"],
    srcs_version = "PY3",
    visibility = ["//visibility:public"],
    deps = ["@markupsafe_archive//:markupsafe"],
)
