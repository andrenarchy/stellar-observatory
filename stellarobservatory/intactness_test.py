"""Tests for Torstens's intactNode Algorithm"""
from stellarobservatory.intactness import intact_nodes
from stellarobservatory.quorums import contains_slice


def test_intact_nodes():
    """Test intact_nodes (Example 4.13)"""
    slices_by_node = {
        'A': [{'A', 'B'}],
        'B': [{'A', 'B', 'C', 'D'}],
        'C': [{'B', 'C'}, {'C', 'D'}],
        'D': [{'B', 'D'}, {'C', 'D'}]
    }

    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, slices_by_node, node)

    res = intact_nodes((is_slice_contained, {'A', 'B', 'C', 'D'}), {'A'})
    assert res == {'C', 'D'}
