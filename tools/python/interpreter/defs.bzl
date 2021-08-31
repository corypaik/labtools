""" Macro to create a python REPL

Source:
    https://github.com/thundergolfer/example-bazel-monorepo
"""

load("@rules_python//python:defs.bzl", "py_binary")

def py_interpreter(name, deps, visibility = None):
    py_binary(
        name = name,
        srcs = [Label("//tools/python/interpreter:interpreter.py")],
        main = Label("//tools/python/interpreter:interpreter.py"),
        deps = deps,
    )
