"""Tests for enumerate dsets algorithm"""
from .dsets import enumerate_dsets
from .quorums import contains_slice
from .quorums_test import SLICES_BY_NODE

NODES = set(range(1, 9))
SLICES_BY_NODE = SLICES_BY_NODE.copy()
SLICES_BY_NODE[6] = [{4, 5, 6, 7, 8}]
SLICES_BY_NODE[8] = [{8}]

def test_enumerate_dsets():
    """Test enmumerate_dsets"""
    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, SLICES_BY_NODE, node)

    dsets = set(frozenset(dset) for dset in enumerate_dsets((is_slice_contained, NODES)))

    assert dsets == {
        frozenset({1, 2, 3, 4, 5, 6, 7, 8}),
        frozenset({1, 2, 3, 4, 5, 6, 8}),
        frozenset({1, 2, 3, 4, 5, 6, 7}),
        frozenset({8, 4, 5, 6})
    }
