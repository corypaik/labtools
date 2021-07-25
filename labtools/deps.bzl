""" Dependencies that are needed for labtools tests. """

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")

def labtools_deps():
    """ Fetch and install all pip deps for labtools. """

    # For `absl-py`
    #    Source: https://github.com/abseil/abseil-py/blob/master/WORKSPACE
    maybe(
        http_archive,
        name = "absl_archive",
        urls = [
            "https://github.com/abseil/abseil-py/archive/refs/tags/pypi-v0.13.0.tar.gz",
        ],
        sha256 = "82423ef923465cb628424c93be2fd29bff70f3e6aca90fe5fade6fc4cefca669",
        strip_prefix = "abseil-py-pypi-v0.13.0",
        build_file = "//third_party:absl.BUILD",
        patch_args = ["-p1"],
        patches = ["//third_party:absl-py.patch"],
    )

    maybe(
        http_archive,
        name = "six_archive",
        urls = [
            "http://mirror.bazel.build/pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz",
            "https://pypi.python.org/packages/source/s/six/six-1.10.0.tar.gz",
        ],
        sha256 = "105f8d68616f8248e24bf0e9372ef04d3cc10104f1980f54d57b2ce73a5ad56a",
        strip_prefix = "six-1.10.0",
        build_file = "//third_party:six.BUILD",
    )

    maybe(
        http_archive,
        name = "mock_archive",
        urls = [
            "http://mirror.bazel.build/pypi.python.org/packages/a2/52/7edcd94f0afb721a2d559a5b9aae8af4f8f2c79bc63fdbe8a8a6c9b23bbe/mock-1.0.1.tar.gz",
            "https://pypi.python.org/packages/a2/52/7edcd94f0afb721a2d559a5b9aae8af4f8f2c79bc63fdbe8a8a6c9b23bbe/mock-1.0.1.tar.gz",
        ],
        sha256 = "b839dd2d9c117c701430c149956918a423a9863b48b09c90e30a6013e7d2f44f",
        strip_prefix = "mock-1.0.1",
        build_file = "//third_party:mock.BUILD",
    )

    maybe(
        http_archive,
        # NOTE: The name here is used in _enum_module.py to find the sys.path entry.
        name = "enum34_archive",
        urls = [
            "https://mirror.bazel.build/pypi.python.org/packages/bf/3e/31d502c25302814a7c2f1d3959d2a3b3f78e509002ba91aea64993936876/enum34-1.1.6.tar.gz",
            "https://pypi.python.org/packages/bf/3e/31d502c25302814a7c2f1d3959d2a3b3f78e509002ba91aea64993936876/enum34-1.1.6.tar.gz",
        ],
        sha256 = "8ad8c4783bf61ded74527bffb48ed9b54166685e4230386a9ed9b1279e2df5b1",
        build_file = "//third_party:enum34.BUILD",
    )

    # For `toolz`
    #  See: https://github.com/pytoolz/toolz
    maybe(
        http_archive,
        name = "toolz_archive",
        urls = [
            "https://files.pythonhosted.org/packages/d6/0d/fdad31347bf3d058002993a094da1ca95f0f3ef9beec08856d0fe4ad9766/toolz-0.11.1.tar.gz",
        ],
        strip_prefix = "toolz-0.11.1",
        sha256 = "c7a47921f07822fe534fb1c01c9931ab335a4390c782bd28c6bcc7c2f71f3fbf",
        build_file = "//third_party:toolz.BUILD",
    )
