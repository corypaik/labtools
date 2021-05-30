load("@rules_python//python:defs.bzl", "py_library")
load("@labtools__pip//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "pytype_helper",
    srcs = ["_src/pytype_helper.py"],
    data = ["//:pytype.cfg"],
    deps = [requirement("pytype")],
)
