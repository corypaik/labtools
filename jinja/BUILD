load("@rules_python//python:defs.bzl", "py_binary")
load("//jinja:defs.bzl", "jinja")

filegroup(
    name = "distribution",
    srcs = glob(["**"]),
    visibility = ["//:__pkg__"],
)

py_binary(
    name = "jinja_runner",
    srcs = ["_src/jinja.py"],
    main = "_src/jinja.py",
    # visibility = ["//visibility:public"],
    deps = ["@jinja_archive//:jinja2"],
)

jinja(
    name = "test-1",
    data = {"flag.value": "hello"},
    template = "_src/dummy.yml.j2",
)
