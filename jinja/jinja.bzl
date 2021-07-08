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
# ==============================================================================
""" Bazel rule for filling templates with Jinja2 """

def assoc_in(d, keys, value, factory = dict):
    """ Update value in a (potentially) nested dictionary

    This function was inspired by toolz.update_in and adopted for bazel.

    Source:
        https://github.com/pytoolz/toolz/blob/master/toolz/dicttoolz.py

    Args:
        d: dictionary on which to operate
        keys: list or tuple giving the location of the value to be changed in d
        value: function to operate on that value
        factory: function at

    Returns:
        If keys == [k0,..,kX] and d[k0]..[kX] == v, update_in returns a copy of the
        original dictionary with v replaced by func(v), but does not mutate the
        original dictionary.

        If k0 is not a key in d, update_in creates nested dictionaries to the depth
        specified by the keys, with the innermost value set to func(default).

        >>> inc = lambda x: x + 1
        >>> update_in({'a': 0}, ['a'], inc)
        {'a': 1}

        >>> transaction = {'name': 'Alice',
        ...                'purchase': {'items': ['Apple', 'Orange'],
        ...                             'costs': [0.50, 1.25]},
        ...                'credit card': '5555-1234-1234-1234'}
        >>> update_in(transaction, ['purchase', 'costs'], sum) # doctest: +SKIP
        {'credit card': '5555-1234-1234-1234',
        'name': 'Alice',
        'purchase': {'costs': 1.75, 'items': ['Apple', 'Orange']}}

        >>> # updating a value when k0 is not in d
        >>> update_in({}, [1, 2, 3], str, default="bar")
        {1: {2: {3: 'bar'}}}
        >>> update_in({1: 'foo'}, [2, 3, 4], inc, 0)
        {1: 'foo', 2: {3: {4: 1}}}
    """

    k = keys[0]

    rv = factory()
    inner = rv

    rv.update(d)

    for key in keys[1:]:
        if k in d:
            d = d[k]
            dtemp = factory()
            dtemp.update(d)
        else:
            d = factory()
            dtemp = d

        inner[k] = dtemp
        inner = inner[k]
        k = key

    if k in d:
        inner[k] = value
    else:
        inner[k] = value
    return rv

def _convert_data_to_nested(data, sep = "."):
    items = data.items()

    # -> flat
    flat_items = [(k.split("."), v) for k, v in items]

    result = {}
    for k_parts, v in flat_items:
        result = assoc_in(result, k_parts, v)

    return result

def _jinja(ctx):
    # The input file is given to us from the BUILD file via an attribute.
    template_file = ctx.file.template

    # The output file is declared with a name based on the target's name.
    out_file = ctx.actions.declare_file("%s.%s" % (ctx.attr.name, ctx.attr.format))

    # Check data or data_file
    if ctx.file.data_file and ctx.attr.data != {}:
        fail("Multiple data sources are not supported, please use either data_file or data, but not both")

    if ctx.file.data_file:
        var_file = ctx.file.data_file
    else:
        # format the data as json.
        flat_data = ctx.attr.data

        # print(flat_data, type(flat_data))
        nested_data = _convert_data_to_nested(flat_data)

        # add flags
        nested_data["flags"] = ctx.attr.flags

        in_data = json.encode(nested_data)

        # Write the json data
        var_file = ctx.actions.declare_file("%s__jinja_data.json" % (ctx.attr.name))
        ctx.actions.write(var_file, in_data)

    # Generate Args
    # args = ["-f=json", "-o=%s" % out_file.path, template_file.path, var_file.path]
    args = ["-o=%s" % out_file.path, template_file.path, var_file.path]

    # Action to call the script.
    ctx.actions.run(
        inputs = [template_file, var_file],
        outputs = [out_file],
        arguments = args,
        progress_message = "[Jinja2] %s -> %s" % (template_file.short_path, out_file.short_path),
        executable = ctx.executable._renderer,
    )

    # Tell Bazel that the files to build for this target includes
    # `out_file`.
    return [DefaultInfo(files = depset([out_file]))]

jinja = rule(
    implementation = _jinja,
    attrs = {
        "template": attr.label(allow_single_file = True),
        "data": attr.string_dict(),
        "flags": attr.string_list(),
        "data_file": attr.label(allow_single_file = True),
        "format": attr.string(default = "yaml"),
        "_renderer": attr.label(
            executable = True,
            cfg = "exec",
            allow_files = True,
            default = Label("@labtools//jinja:jinja_runner"),
        ),
    },
    outputs = {
        "%{format}": "%{name}.%{format}",
    },
    doc = """
Given an input template and data, run jinja2 to produce an filled output file
with the specified extension.
""",
)
