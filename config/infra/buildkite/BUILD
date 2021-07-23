load("@io_bazel_rules_docker//container:container.bzl", "container_image", "container_layer")
load("@k8s_deploy//:defaults.bzl", "k8s_deploy")

k8s_deploy(
    name = "buildkite-agent",
    images = {
        "labtools/buildkite-agent": ":buildkite-image",
    },
    template = ":buildkite-agent.yaml",
)

container_layer(
    name = "buildkite-binaries",
    directory = "/usr/local/bin",
    empty_dirs = [
        "/buildkite/builds",
        "/buildkite/hooks",
        "/buildkite/plugins",
    ],
    files = [
        "entrypoint.sh",
        "ssh-env-config.sh",
        "@com_github_buildkite_agent//:buildkite-agent",
        "@com_github_krallin_tini//file",
    ],
    symlinks = {
        "/usr/local/bin/buildkite-agent-entrypoint": "/usr/local/bin/entrypoint.sh",
    },
)

container_image(
    name = "buildkite-image",
    base = "@bazel_ubuntu_2004//image",
    cmd = ["start"],
    directory = "/buildkite",
    entrypoint = ["buildkite-agent-entrypoint"],
    env = {
        "BUILDKITE_AGENT_CONFIG": "/buildkite/buildkite-agent.cfg",
    },
    files = [
        "@com_github_buildkite_agent//:buildkite-agent.cfg",
    ],
    layers = [":buildkite-binaries"],
    volumes = ["/buildkite"],
)
