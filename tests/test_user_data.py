import pytest
from facts.user_data import UserFacts


def test_user(tmpdir):
    filename = str(tmpdir.join('user.yml'))
    obj = UserFacts(filename)
    assert obj.data == {}
    obj.write('foo', 'bar')
    assert obj.data == {'foo': 'bar'}
    assert obj.read('foo') == 'bar'
    obj.delete('foo')
    assert obj.data == {}
