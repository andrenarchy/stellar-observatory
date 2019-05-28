"""Test sets utilities"""
from .sets import deepfreezesets, powerset

def test_powerset_list():
    """Test powerset() with a list"""
    result = powerset(['a', 'b'])
    expected = deepfreezesets([{}, {'a'}, {'b'}, {'a', "b"}])
    assert frozenset(result) == expected

def test_powerset_set():
    """Test powerset() with a set"""
    result = powerset({'a', 'b'})
    expected = deepfreezesets([{}, {'a'}, {'b'}, {'a', "b"}])
    assert frozenset(result) == expected
