# Copyright 2021 The LabTools Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
workspace(
    name = "labtools",
    managed_directories = {"@labtools_yarn": ["node_modules"]},
)

load("//repositories:repositories.bzl", "labtools_repos")

labtools_repos()

load("//repositories:deps.bzl", "labtools_deps")

labtools_deps()

##############
# Dependencies
##############

load("@com_github_ali5h_rules_pip//:defs.bzl", "pip_import")

pip_import(
    name = "pip",
    python_interpreter = "python3",
    requirements = "//tools:test-requirements.txt",
)

load("@pip//:requirements.bzl", "pip_install")

pip_install(["--no-deps"])

##############
# Kubernetes
##############
load("@io_bazel_rules_k8s//k8s:k8s.bzl", "k8s_defaults")

k8s_defaults(
    name = "k8s_deploy",
    cluster = "gke_kln-lab_us-central1-a_kln-lab-k8s",
    image_chroot = "us-docker.pkg.dev/kln-lab/kln",
    kind = "deployment",
)

load("//config/infra/buildkite:deps.bzl", "buildkite_deps")

buildkite_deps()

##############
# Test Deps
##############
load("//labtools:deps.bzl", _internal_labtools_deps = "labtools_deps")

_internal_labtools_deps()
