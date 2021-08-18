# Copyright 2021 The LabTools Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" Repo dependencies """

load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")
load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")
load("@build_bazel_rules_nodejs//:index.bzl", "node_repositories", "npm_install")
load("@com_google_protobuf//:protobuf_deps.bzl", "protobuf_deps")
load("@io_bazel_rules_docker//container:container.bzl", "container_pull")
load("@io_bazel_rules_docker//nodejs:image.bzl", nodejs_image_repos = "repositories")
load("@io_bazel_rules_docker//python3:image.bzl", py3_image_repos = "repositories")
load("@io_bazel_rules_docker//repositories:deps.bzl", container_deps = "deps")
load(
    "@io_bazel_rules_docker//repositories:repositories.bzl",
    container_repositories = "repositories",
)
load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")
load("@io_bazel_rules_k8s//k8s:k8s.bzl", "k8s_repositories")
load("@io_bazel_rules_k8s//k8s:k8s_go_deps.bzl", k8s_go_deps = "deps")
load("@io_bazel_rules_sass//sass:sass_repositories.bzl", "sass_repositories")
load("@linting_system//repositories:go_repositories.bzl", linting_deps = "go_deps")
load("@linting_system//repositories:repositories.bzl", linting_repos = "repositories")
load("@rules_python//python:pip.bzl", "pip_install")

## local
load("//jinja:deps.bzl", "jinja_deps")
load("//tools:defs.bzl", "clean_dep")

def py_deps():
    """Pull in external Python packages needed by py binaries in this repo.
    """
    excludes = native.existing_rules().keys()
    if "labtools__pip" not in excludes:
        pip_install(
            python_interpreter = "python3.7",
            name = "labtools__pip",
            requirements = clean_dep("//tools:requirements.txt"),
        )

def deps():
    """Install all dependencies."""
    py_deps()

    bazel_skylib_workspace()

    node_repositories(package_json = [clean_dep("//:package.json")])
    npm_install(
        name = "labtools__npm",
        package_json = clean_dep("//:package.json"),
        quiet = False,
        package_lock_json = clean_dep("//:package-lock.json"),
    )

    sass_repositories()

    # docker
    container_repositories()
    container_deps()

    # Add support for python 3.7
    # TODO(corypaik): remove once @io_bazel_rules_docker updates.
    container_pull(
        name = "py3_image_base",
        digest = "sha256:ef51e4c3f5a123b14078731c8ae9f43223855ca761a430e435fdb413a1fbea45",
        registry = "gcr.io",
        repository = "distroless/python3",
    )

    py3_image_repos()
    nodejs_image_repos()

    # k8s
    k8s_repositories()
    k8s_go_deps()

    # buildifier
    go_rules_dependencies()
    go_register_toolchains()
    gazelle_dependencies()
    protobuf_deps()

    # linting
    linting_repos()
    linting_deps()

    ####
    jinja_deps()

labtools_deps = deps
