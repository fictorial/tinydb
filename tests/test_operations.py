from tinydb import where
from tinydb.operations import delete, increment, decrement, \
    add_to_set, remove_from_set, append, prepend, slice

import pytest


def test_delete(db):
    db.update(delete('int'), where('char') == 'a')
    assert 'int' not in db.get(where('char') == 'a')


def test_increment(db):
    db.update(increment('int'), where('char') == 'a')
    assert db.get(where('char') == 'a')['int'] == 2


def test_decrement(db):
    db.update(decrement('int'), where('char') == 'a')
    assert db.get(where('char') == 'a')['int'] == 0


def test_increment_with_delta(db):
    db.update(increment('int', 9), where('char') == 'a')
    assert db.get(where('char') == 'a')['int'] == 10


def test_decrement_with_delta(db):
    db.update(decrement('int', 2), where('char') == 'a')
    assert db.get(where('char') == 'a')['int'] == -1


def test_decrement_with_delta_raise(db):
    with pytest.raises(ValueError):
        db.update(decrement('int', 2, raise_if_negative=True), where('char') == 'a')


def test_add_to_set(db):
    db.update(add_to_set('set', 'x'), where('char') == 'a')
    assert db.get(where('char') == 'a')['set'] == ['x']

    db.update(add_to_set('set', 'x'), where('char') == 'a')
    assert db.get(where('char') == 'a')['set'] == ['x']

    db.update(add_to_set('set', 'y'), where('char') == 'a')
    assert sorted(db.get(where('char') == 'a')['set']) == ['x','y']


def test_remove_from_set(db):
    db.update(add_to_set('set', 'x'), where('char') == 'a')
    assert db.get(where('char') == 'a')['set'] == ['x']

    db.update(remove_from_set('set', 'x'), where('char') == 'a')
    assert db.get(where('char') == 'a')['set'] == []

    db.update(add_to_set('set', 'x'), where('char') == 'a')
    assert db.get(where('char') == 'a')['set'] == ['x']

    db.update(add_to_set('set', 'y'), where('char') == 'a')
    assert sorted(db.get(where('char') == 'a')['set']) == ['x','y']

    db.update(remove_from_set('set', 'y'), where('char') == 'a')
    assert db.get(where('char') == 'a')['set'] == ['x']


def test_append(db):
    db.update(append('list', 'x'), where('char') == 'a')
    assert db.get(where('char') == 'a')['list'] == ['x']

    db.update(append('list', 'x'), where('char') == 'a')
    assert db.get(where('char') == 'a')['list'] == ['x','x']

    db.update(append('list', 'y'), where('char') == 'a')
    assert db.get(where('char') == 'a')['list'] == ['x','x','y']


def test_prepend(db):
    db.update(prepend('list', 'x'), where('char') == 'a')
    assert db.get(where('char') == 'a')['list'] == ['x']

    db.update(prepend('list', 'y'), where('char') == 'a')
    assert db.get(where('char') == 'a')['list'] == ['y','x']

    db.update(prepend('list', 'z'), where('char') == 'a')
    assert db.get(where('char') == 'a')['list'] == ['z','y','x']


def test_slice(db):
    db.update(prepend('list', 'x'), where('char') == 'a')
    assert db.get(where('char') == 'a')['list'] == ['x']

    db.update(prepend('list', 'y'), where('char') == 'a')
    assert db.get(where('char') == 'a')['list'] == ['y','x']

    db.update(prepend('list', 'z'), where('char') == 'a')
    assert db.get(where('char') == 'a')['list'] == ['z','y','x']

    db.update(slice('list', 0, 2), where('char') == 'a')
    assert db.get(where('char') == 'a')['list'] == ['z','y']

