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
""" defines dependencies for building a buildkite deployment """

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive", "http_file")
load("@io_bazel_rules_docker//container:container.bzl", "container_pull")

def buildkite_deps():
    """ download buildkite deps """
    http_file(
        name = "com_github_krallin_tini",
        downloaded_file_path = "tini",
        urls = ["https://github.com/krallin/tini/releases/download/v0.19.0/tini"],
        sha256 = "93dcc18adc78c65a028a84799ecf8ad40c936fdfc5f2a57b1acda5a8117fa82c",
        executable = True,
    )

    http_archive(
        name = "com_github_buildkite_agent",
        url = "https://github.com/buildkite/agent/releases/download/v3.31.0/buildkite-agent-linux-amd64-3.31.0.tar.gz",
        build_file_content = "exports_files([\"buildkite-agent\", \"buildkite-agent.cfg\"])",
        sha256 = "f8b3b59d1c27e7e2ccc46819e4cafedb6d58ee1fdbfd006b22f34950558e4a27",
    )

    container_pull(
        name = "bazel_ubuntu_2004",
        registry = "gcr.io",
        repository = "bazel-public/ubuntu2004-nojava",
        digest = "sha256:4fceaeb1734849aa3d08168e1845165c98b3acfc69901cd4bf097f7512764d8f",
    )
