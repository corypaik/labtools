load(":jinja.bzl", "jinja")
load("@labtools__pip//:requirements.bzl", "requirement")

package(default_visibility = ["//:__subpackages__"])

py_binary(
    name = "jinja_runner",
    srcs = ["_src/jinja.py"],
    main = "_src/jinja.py",
    visibility = ["//visibility:public"],
    deps = [requirement("j2cli")],
)

jinja(
    name = "test-1",
    data = {"flag.value": "hello"},
    template = "dummy.yml.j2",
)
