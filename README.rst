Facts
=====

Returns facts of local machine.


Installation
------------

::

    pip install facts


CLI Usage
---------

Get all facts::

    facts all

Get one fact::

    fact read foo:bar

Set one custom fact::

    fact write foo:baz 'It is nice'

When value is a mapping, then you can choose between 2 merging strategies::

    fact write foo:baz '{is: baz}' --format yaml --replace
    fact write foo:baz '{is: baz}' --format yaml --merge

Delete a custom fact::

    fact delete foo:bar


Extending
---------

You can extend with your own facts. Any python modules under ``~/.facts/grafts``
will be loaded. For example::

    # ~/.facts/grafts/my_grafts.py

    from . import graft

    @graft
    def hello_world():
        return {
            'hello': 'world'
        }

Will append the fact ``hello`` with the value ``world``.
