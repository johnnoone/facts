import pytest
from facts.targeting import Target, NotFound, WrongType


def test_match():
    obj1 = {'foo': 42, 'bar': ['baz', 'qux']}
    obj2 = {'one': 42, 'two': {'three': 4}}

    target = Target('foo')
    assert target.match(obj1) is True
    assert target.match(obj2) is False

    target = Target('foo:42')
    assert target.match(obj1) is True
    assert target.match(obj2) is False

    target = Target('bar:baz')
    assert target.match(obj1) is True
    assert target.match(obj2) is False

    target = Target('bar:qux')
    assert target.match(obj1) is True
    assert target.match(obj2) is False

    target = Target('two:three:4')
    assert target.match(obj1) is False
    assert target.match(obj2) is True


def test_read():
    obj1 = {'foo': 42, 'bar': ['baz', 'qux']}
    obj2 = {'one': 42, 'two': {'three': 4}}

    target = Target('foo')
    assert target.read(obj1) == 42
    with pytest.raises(NotFound):
        target.read(obj2)

    target = Target('foo:42')
    with pytest.raises(WrongType):
        target.read(obj1)
    with pytest.raises(NotFound):
        target.read(obj2)

    target = Target('bar:baz')
    with pytest.raises(WrongType):
        target.read(obj1)
    with pytest.raises(NotFound):
        target.read(obj2)

    target = Target('bar:qux')
    with pytest.raises(WrongType):
        target.read(obj1)
    with pytest.raises(NotFound):
        target.read(obj2)

    target = Target('two:three')
    with pytest.raises(NotFound):
        target.read(obj1)
    assert target.read(obj2) == 4


def test_read_2():
    obj = {'one': {'two': None}}
    target = Target('one:two:three')
    with pytest.raises(NotFound):
        target.read(obj)


def test_write_1():
    obj1 = {'foo': 42}
    target = Target('foo')
    obj2 = target.write(obj1, 'bar')
    assert target.read(obj1) == 42
    assert target.read(obj2) == 'bar'
    obj3 = target.delete(obj1)
    assert 'foo' not in obj3


def test_write_2():
    obj1 = {'foo': {'bar': 'baz'}}
    target = Target('foo:bar')
    obj2 = target.write(obj1, 'qux')
    assert target.read(obj1) == 'baz'
    assert target.read(obj2) == 'qux'
    obj3 = target.delete(obj1)
    assert 'baz' not in obj3['foo']


def test_write_3():
    obj1 = {'foo':  ['one', 'two']}
    target = Target('foo:-')
    obj2 = target.write(obj1, 'bar')
    assert obj2 == {'foo': ['one', 'two', 'bar']}
    obj3 = target.delete(obj1)
    assert obj3 == {'foo': ['one']}


def test_write_4():
    obj1 = {'foo': ['one', 'two']}
    target = Target('foo:1')
    obj2 = target.write(obj1, 'bar')
    assert obj2 == {'foo': ['one', 'bar']}
    obj3 = target.delete(obj1)
    assert obj3 == {'foo': ['one']}


def test_write_5():
    obj1 = {'foo':  [None, {'bar': 'baz'}]}
    target = Target('foo:1:bar')
    obj2 = target.write(obj1, 'qux')
    assert obj2 == {'foo': [None, {'bar': 'qux'}]}
    obj3 = target.delete(obj1)
    assert obj3 == {'foo': [None, {}]}


def test_write_6():
    obj1 = {'top': {'foo': 'bar'}}
    target = Target('top')
    obj2 = target.write(obj1, {'baz': 'qux'})
    assert obj2 == {'top': {'baz': 'qux'}}
    obj3 = target.write(obj1, {'baz': 'qux'}, merge=True)
    assert obj3 == {'top': {'foo': 'bar', 'baz': 'qux'}}
