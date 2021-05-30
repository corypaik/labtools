load("@rules_python//python:defs.bzl", "py_library")
load("@labtools__pip//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

py_library(
    name = "jupyterlab_helper",
    srcs = ["_src/jupyterlab_helper.py"],
    deps = [
        requirement("jupyterlab"),
        requirement("jupyter_contrib_nbextensions"),
        requirement("ipywidgets"),
    ],
)
