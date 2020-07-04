"""Tests for Torstens's intactNode Algorithm"""
from stellarobservatory.intactness import intact_nodes
from stellarobservatory.quorums import contains_slice


def test_intact_nodes():
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

    assert intact_nodes((is_slice_contained, nodes), {'A'}) == set()
    assert intact_nodes((is_slice_contained, nodes), {'B'}) == set()
    assert intact_nodes((is_slice_contained, nodes), {'C', 'D'}) == set()

def test_intact_nodes_complex():
    """Test intact_nodes (Example centrality paper)"""
    nodes = {1, 2, 3, 4, 5}
    slices_by_node = {
        1: [{1, 2}, {1, 3}, {1, 4}, {1, 5}],
        2: [{1, 2}, {2, 3}],
        3: [{1, 3}],
        4: [{1, 4}],
        5: [{1, 5}]
    }

    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, slices_by_node, node)

    assert intact_nodes((is_slice_contained, nodes), {1}) == set()
    assert intact_nodes((is_slice_contained, nodes), {2}) == {1, 3, 4, 5}
    assert intact_nodes((is_slice_contained, nodes), {3}) == {1, 4, 5}
    assert intact_nodes((is_slice_contained, nodes), {4}) == {1, 2, 3, 5}
    assert intact_nodes((is_slice_contained, nodes), {5}) == {1, 2, 3, 4}
    assert intact_nodes((is_slice_contained, nodes), {2, 3}) == {1, 4, 5}
    assert intact_nodes((is_slice_contained, nodes), {4, 5}) == {1, 2, 3}
