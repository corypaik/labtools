""" General utilities and patch tools """

def clean_dep(target):
    """Returns string to 'target' in the current repository.

    Use this function when referring to targets in the @rules_kubeflow
    repository from macros that may be called from external repositories.

    Source:
        github.com/tensorflow/tensorflow.bzl
    """

    # A repo-relative label is resolved relative to the file in which the
    # Label() call appears, i.e. @rules_kubeflow.
    return str(Label(target))
