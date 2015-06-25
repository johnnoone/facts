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

    fact read foo

Set one custom fact::

    fact write foo 'It is nice'

When value is a mapping, then you can choose between 2 merging strategies::

    fact write foo '{is: bar}' --format yaml --replace
    fact write foo '{not: baz}' --format yaml --merge

Delete a custom fact::

    fact delete foo


Targeting
---------

By convention key facts can't have colon marks.
Because facts can be nested, and it's possible to target these sub data.
Each parts must be seperated by a colon. For example if::

    fact read foo

returns::

    is: bar
    not: baz

Then::

    fact read foo:is

returns::

    bar

But::

    fact read foo:wrong:key

will return nothing.


Matching
--------

It is also possible to check if a certain fact turns out true::

    fact match foo:is:bar


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
