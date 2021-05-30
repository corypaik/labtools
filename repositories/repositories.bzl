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
""" Loads all required dependeices (skip exisiting) """

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def repositories():
    """ Download dependecies"""
    existing = native.existing_rules().keys()

    ############################################################################
    # Python
    ############################################################################
    if "rules_python" not in existing:
        http_archive(
            name = "rules_python",
            sha256 = "b6d46438523a3ec0f3cead544190ee13223a52f6a6765a29eae7b7cc24cc83a0",
            url = "https://github.com/bazelbuild/rules_python/releases/download/0.1.0/rules_python-0.1.0.tar.gz",
        )

    if "com_github_ali5h_rules_pip" not in existing:
        http_archive(
            name = "com_github_ali5h_rules_pip",
            sha256 = "630a7cab43a87927353efca116d20201df88fb443962bf01c7383245c7f3a623",
            strip_prefix = "rules_pip-3.0.0",
            urls = ["https://github.com/ali5h/rules_pip/archive/3.0.0.tar.gz"],
        )

    ############################################################################
    # Angular
    ############################################################################
    # Source:
    #   https://github.com/bazelbuild/rules_nodejs/tree/stable/examples/angular
    if "bazel_skylib" not in existing:
        http_archive(
            name = "bazel_skylib",
            sha256 = "1c531376ac7e5a180e0237938a2536de0c54d93f5c278634818e0efc952dd56c",
            urls = [
                "https://github.com/bazelbuild/bazel-skylib/releases/download/1.0.3/bazel-skylib-1.0.3.tar.gz",
                "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.0.3/bazel-skylib-1.0.3.tar.gz",
            ],
        )

    if "build_bazel_rules_nodejs" not in existing:
        http_archive(
            name = "build_bazel_rules_nodejs",
            sha256 = "dd7ea7efda7655c218ca707f55c3e1b9c68055a70c31a98f264b3445bc8f4cb1",
            urls = ["https://github.com/bazelbuild/rules_nodejs/releases/download/3.2.3/rules_nodejs-3.2.3.tar.gz"],
        )

    # Fetch sass rules for compiling sass files
    if "io_bazel_rules_sass" not in existing:
        http_archive(
            name = "io_bazel_rules_sass",
            patch_args = ["-p1"],
            # We need the latest rules_sass to get the --bazel_patch_module_resolver behavior
            # However it seems to have a bug, so we patch back to the prior dart-sass version.
            # See https://github.com/bazelbuild/rules_sass/issues/127
            # TODO(alexeagle): fix upstream and remove patch
            patches = ["@build_bazel_rules_nodejs//:rules_sass.issue127.patch"],
            sha256 = "8392cf8910db2b1dc3b488ea18113bfe4fd666037bf8ec30d2a3f08fc602a6d8",
            strip_prefix = "rules_sass-1.30.0",
            urls = [
                "https://github.com/bazelbuild/rules_sass/archive/1.30.0.zip",
                "https://mirror.bazel.build/github.com/bazelbuild/rules_sass/archive/1.30.0.zip",
            ],
        )

    ####################
    # Remote Execution #
    ####################
    if "bazel_toolchains" not in existing:
        http_archive(
            name = "bazel_toolchains",
            sha256 = "1adf5db506a7e3c465a26988514cfc3971af6d5b3c2218925cd6e71ee443fc3f",
            strip_prefix = "bazel-toolchains-4.0.0",
            urls = [
                "https://mirror.bazel.build/github.com/bazelbuild/bazel-toolchains/releases/download/4.0.0/bazel-toolchains-4.0.0.tar.gz",
                "https://github.com/bazelbuild/bazel-toolchains/releases/download/4.0.0/bazel-toolchains-4.0.0.tar.gz",
            ],
        )

    ##########
    # Docker #
    ##########
    if "io_bazel_rules_docker" not in existing:
        http_archive(
            name = "io_bazel_rules_docker",
            sha256 = "95d39fd84ff4474babaf190450ee034d958202043e366b9fc38f438c9e6c3334",
            strip_prefix = "rules_docker-0.16.0",
            urls = ["https://github.com/bazelbuild/rules_docker/releases/download/v0.16.0/rules_docker-v0.16.0.tar.gz"],
        )

    # buildifier
    # Source: https://github.com/bazelbuild/buildtools
    if "io_bazel_rules_go" not in existing:
        http_archive(
            name = "io_bazel_rules_go",
            sha256 = "d1ffd055969c8f8d431e2d439813e42326961d0942bdf734d2c95dc30c369566",
            urls = [
                "https://mirror.bazel.build/github.com/bazelbuild/rules_go/releases/download/v0.24.5/rules_go-v0.24.5.tar.gz",
                "https://github.com/bazelbuild/rules_go/releases/download/v0.24.5/rules_go-v0.24.5.tar.gz",
            ],
        )
    if "bazel_gazelle" not in existing:
        http_archive(
            name = "bazel_gazelle",
            sha256 = "b85f48fa105c4403326e9525ad2b2cc437babaa6e15a3fc0b1dbab0ab064bc7c",
            urls = [
                "https://mirror.bazel.build/github.com/bazelbuild/bazel-gazelle/releases/download/v0.22.2/bazel-gazelle-v0.22.2.tar.gz",
                "https://github.com/bazelbuild/bazel-gazelle/releases/download/v0.22.2/bazel-gazelle-v0.22.2.tar.gz",
            ],
        )
    if "com_google_protobuf" not in existing:
        http_archive(
            name = "com_google_protobuf",
            sha256 = "9b4ee22c250fe31b16f1a24d61467e40780a3fbb9b91c3b65be2a376ed913a1a",
            strip_prefix = "protobuf-3.13.0",
            urls = [
                "https://github.com/protocolbuffers/protobuf/archive/v3.13.0.tar.gz",
            ],
        )
    if "com_github_bazelbuild_buildtools" not in existing:
        http_archive(
            name = "com_github_bazelbuild_buildtools",
            strip_prefix = "buildtools-4.0.1",
            sha256 = "932160d5694e688cb7a05ac38efba4b9a90470c75f39716d85fb1d2f95eec96d",
            url = "https://github.com/bazelbuild/buildtools/archive/4.0.1.zip",
        )

    # linting
    # Note: This requires @io_bazel_rules_go from buildifer.
    if "linting_system" not in existing:
        http_archive(
            name = "linting_system",
            sha256 = "a254c73bdde03214b62cacdb570229ed1a1814a2ed749448a1db4e90b18ac0a1",
            strip_prefix = "bazel-linting-system-0.4.0",
            url = "https://github.com/thundergolfer/bazel-linting-system/archive/v0.4.0.zip",
        )
