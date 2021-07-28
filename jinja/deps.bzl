""" Dependencies that are needed for jinja rules """

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:utils.bzl", "maybe")

def jinja_deps():
    maybe(
        http_archive,
        name = "markupsafe_archive",
        urls = [
            "https://files.pythonhosted.org/packages/bf/10/ff66fea6d1788c458663a84d88787bae15d45daa16f6b3ef33322a51fc7e/MarkupSafe-2.0.1.tar.gz",
        ],
        strip_prefix = "MarkupSafe-2.0.1",
        build_file = "@labtools//third_party:markupsafe.BUILD",
        sha256 = "594c67807fb16238b30c44bdf74f36c02cdf22d1c8cda91ef8a0ed8dabf5620a",
    )

    maybe(
        http_archive,
        name = "jinja_archive",
        url = "https://files.pythonhosted.org/packages/39/11/8076571afd97303dfeb6e466f27187ca4970918d4b36d5326725514d3ed3/Jinja2-3.0.1.tar.gz",
        sha256 = "703f484b47a6af502e743c9122595cc812b0271f661722403114f71a79d0f5a4",
        build_file = "@labtools//third_party:jinja.BUILD",
        strip_prefix = "Jinja2-3.0.1",
    )
