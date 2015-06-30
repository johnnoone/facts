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

Get the human readable memory usage::

    fact read memory --human

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


Grafting
--------

Facts allow you to extends with 'grafts'. There is 2 ways


1. by modules
~~~~~~~~~~~~~

You can extend with your own facts. Any python modules under ``~/.facts/grafts`` will be loaded. For example::

    # ~/.facts/grafts/my_grafts.py

    from facts import graft, mark

    @graft
    def hello_world():
        return {
            'hello': 'world',
            'size': mark(1234567890, 'bytes')
        }

Will append the fact ``hello`` with the value ``world``, and the fact ``size``
with one of these values (depending the --human switch) ``1234567890`` or ``1234567890K``.


2. with setuptools
~~~~~~~~~~~~~~~~~~

You also write python libraries that will contribute to facts with using setuptools. Add the following to the setup.py function::

    entry_points={
        'facts.graft': [
            'plugin-1 = mylib:plugin_1',
            'plugin-2 = mylib:plugin_2'
        ]
    }
