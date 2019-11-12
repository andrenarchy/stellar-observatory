"""Test for Torstens's quorum enumeration"""
from .quorums import enumerate_quorums

def test_enumerate_quorums():
    """Test enumerate_quorums()"""
    slices_by_node = {
        1: [{1, 2, 3, 7}],
        2: [{1, 2, 3, 7}],
        3: [{1, 2, 3, 7}],
        4: [{4, 5, 6, 7}],
        5: [{4, 5, 6, 7}],
        6: [{4, 5, 6, 7}],
        7: [{7}],
    }
    quorums = list(enumerate_quorums(slices_by_node))
    assert set(quorums) == set(
        [frozenset({7}),
         frozenset({4, 5, 6, 7}),
         frozenset({1, 2, 3, 7}),
         frozenset({1, 2, 3, 4, 5, 6, 7})]
    )
