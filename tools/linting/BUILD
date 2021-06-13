load("@linting_system//:rules.bzl", "linter")

package(default_visibility = ["//visibility:public"])

linter(
    name = "python",
    config = "//:pyproject.toml",
    config_option = "-vv -ri --style",
    executable_path = "yapf",
)
