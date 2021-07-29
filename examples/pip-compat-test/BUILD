load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")

py3_image(
    name = "pip_compat_test",
    srcs = ["pip_compat_test.py"],
    deps = [
        "@pip//:numpy",
        "@pip//:torch",
    ],
)
