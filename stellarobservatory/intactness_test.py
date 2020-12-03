"""Tests for Torstens's intactNode Algorithm"""
from stellarobservatory.dsets_test import NODES, SLICES_BY_NODE
from .intactness import get_intact_nodes
from .quorums import contains_slice
from .centralities_test import NODES, SLICES_BY_NODE


def test_get_intact_nodes():
    """Test intact_nodes (Example 4.13)"""
    nodes = {'A', 'B', 'C', 'D'}
    slices_by_node = {
        'A': [{'A', 'B'}],
        'B': [{'A', 'B', 'C', 'D'}],
        'C': [{'B', 'C'}, {'C', 'D'}],
        'D': [{'B', 'D'}, {'C', 'D'}]
    }

    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, slices_by_node, node)

    assert get_intact_nodes((is_slice_contained, nodes), {'A'}) == set()
    assert get_intact_nodes((is_slice_contained, nodes), {'B'}) == set()
    assert get_intact_nodes((is_slice_contained, nodes), {'C', 'D'}) == set()

def test_get_intact_nodes_complex():
    """Test intact_nodes (Example centrality paper)"""
    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, SLICES_BY_NODE, node)

    assert get_intact_nodes((is_slice_contained, NODES), {1}) == set()
    assert get_intact_nodes((is_slice_contained, NODES), {2}) == {1, 3, 4, 5}
    assert get_intact_nodes((is_slice_contained, NODES), {3}) == {1, 4, 5}
    assert get_intact_nodes((is_slice_contained, NODES), {4}) == {1, 2, 3, 5}
    assert get_intact_nodes((is_slice_contained, NODES), {5}) == {1, 2, 3, 4}
    assert get_intact_nodes((is_slice_contained, NODES), {2, 3}) == {1, 4, 5}
    assert get_intact_nodes((is_slice_contained, NODES), {4, 5}) == {1, 2, 3}
