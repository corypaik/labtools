""" Linting aspects. """

load("@linting_system//:generator.bzl", "linting_aspect_generator")

lint = linting_aspect_generator(
    name = "python",
    linters = ["@//tools/linting:python"],
)
