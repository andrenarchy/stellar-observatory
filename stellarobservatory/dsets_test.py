"""Tests for enumerate dsets algorithm"""
from stellarobservatory.dsets import enumerate_dsets
from stellarobservatory.quorums import contains_slice


def test_enumerate_dsets():
    """Test enmumerate_dsets"""
    nodes = set(range(1, 9))
    slices_by_node = {
        1: [{1,2,3,7}],
        2: [{1,2,3,7}],
        3: [{1,2,3,7}],
        4: [{4,5,6,7}],
        5: [{4,5,6,7}],
        6: [{4,5,6,7,8}],
        7: [{7}],
        8: [{8}]
    }

    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, slices_by_node, node)

    dsets = set(frozenset(dset) for dset in enumerate_dsets((is_slice_contained, nodes)))

    assert dsets == {
        frozenset({1, 2, 3, 4, 5, 6, 7, 8}),
        frozenset({1, 2, 3, 4, 5, 6, 8}),
        frozenset({1, 2, 3, 4, 5, 6, 7}),
        frozenset({8, 4, 5, 6})
    }
