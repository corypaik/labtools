load("@labtools//pytype:defs.bzl", "pytype_library")
load("@labtools__pip//:requirements.bzl", "requirement")
load("@rules_python//python:packaging.bzl", "py_wheel")

package(default_visibility = ["//visibility:private"])

pytype_library(
    name = "labtools",
    srcs = glob(
        ["**/*.py"],
        exclude = ["**/*_test.py"],
    ),
    data = [":altair-saver-deps"],
    # PyType Dependencies
    pytype_deps = [
        "@pip//:ml_collections",
        "@pip//:pyyaml",
        "@pip//:icecream",
    ],
    visibility = ["//visibility:public"],
    deps = [
        requirement("absl-py"),
        requirement("toolz"),
    ],
)

filegroup(
    name = "altair-saver-deps",
    srcs = [
        "@labtools__yarn//:node_modules/vega-cli/bin/vg2pdf",
        "@labtools__yarn//canvas",
        "@labtools__yarn//vega-cli",
        "@labtools__yarn//vega-lite",
    ],
    visibility = ["//visibility:public"],
)

py_wheel(
    name = "wheel",
    distribution = "labtools",
    python_tag = "py3",
    version = "0.0.1.dev1",
    visibility = ["//visibility:public"],
    deps = [":labtools"],
)
