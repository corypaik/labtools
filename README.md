
---

<div align="center">

# LabTools

</div>

## Description
A collection of research-oriented tools for working with Bazel. 

### Main Features
- [Drop in PyType integration](#pytype-integration). 
- [Support for running JupyterLab](#jupyterlab).
- [Python tooling and utilites](#python-tooling).

## Setup
Add the following to your `WORKSPACE` file:
```python
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "labtools",
    branch = "main",
    remote = "https://github.com/corypaik/labtools",
)
load("@labtools//repositories:repositories.bzl", labtools_repos = "repositories")

labtools_repos()

load("@labtools//repositories:deps.bzl", labtools_deps = "deps")

labtools_deps()
```

We recommend following Bazel's output instructions to pin the repo by using `commit` and `shallow_since`. See the Bazel documentation [here](https://docs.bazel.build/versions/master/repo/git.html#git_repository) for more details.

<!-- TODO(corypaik): implement versioning -->

## Features

### PyType Integration
The macros `pytype_binary`, `pytype_library`, and `pytype_test` are direct replacments for `py_binary`, `py_library`, and `py_test` respectively. You can use them load in your `BUILD` file as:

```python
load("@labtools//pytype:defs.bzl",
    "pytype_binary",
    "pytype_library",
    "pytype_test",
)
```

For each rule, these macros create an additional rule to run `pytype` on the files. This all operates under Bazel and thus allows finer-grained dependency checking on a per-rule basis. For example a rule with the name `run_model` generate `run_model__pytype`. These tests will be ran as python tests, but you can filter them by tags (or configs as shown below).

```bash
# To run exclusive/exclude PyType tests
bazel test --test_tag_filters=pytype //...
bazel test --test_tag_filters=-pytype //...
```

You can find more information about PyType [here](https://github.com/google/pytype).

### JupyterLab
The macro `jupyterlab_sever` can be used to launch a JupyterLab server using pip dependencies from Bazel.

```python 
# in BUILD file
load("@labtools//jupyter:defs.bzl", "jupyterlab_server")

jupyterlab_server(
    name = "jupyterlab",
    deps = [
        "//src:mylibrary",
        "@labtools//labtools",
        "@pip//:pandas",
    ],
)
```
You can find more information about JupyterLab [here](https://github.com/jupyterlab/jupyterlab)

### Python Tooling
The library `@labtools//labtools` provides various utilities for use cases such as experiment managers with error handling and cache cleanup, profiling, working with tfrecords, converting arbitrary array-type objects to lists, etc. 

This library relies only on `toolz` and `absl` at an import-level, and other third-party packages for specific functionalities. Some of these are givens, e.g. you won't need to clean up PyTorch's CUDA cache PyTorch is installed. Other functions, such as loading YML files, do require specific packages. See the error messages or `@require('<pkg>')` decorators for details on what package is required.

