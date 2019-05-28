from .sets import deepfreezesets, powerset

def test_powerset_list():
    result = powerset(['a', 'b'])
    expected = deepfreezesets([{}, {'a'}, {'b'}, {'a', "b"}])
    assert frozenset(result) == expected

def test_powerset_set():
    result = powerset({'a', 'b'})
    expected = deepfreezesets([{}, {'a'}, {'b'}, {'a', "b"}])
    assert frozenset(result) == expected
