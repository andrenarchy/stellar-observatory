"""Tests for Torstens's intactNode Algorithm"""
from stellarobservatory.intactness import intact_nodes
from stellarobservatory.quorums import contains_slice
from stellarobservatory.utils.sets import powerset


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

    res_A = intact_nodes((is_slice_contained, nodes), {'A'})
    assert res_A == set()

    res_B = intact_nodes((is_slice_contained, nodes), {'B'})
    assert res_B == set()

    res_CD = intact_nodes((is_slice_contained, nodes), {'C', 'D'})
    assert res_CD == set()

def test_intact_nodes_complex():
    """Test intact_nodes (Example centrality paper)"""
    nodes = {1, 2, 3, 4, 5}
    slices_by_node = {
        1: [{1, 2}, {1, 3}, {1, 4}, {1,5}],
        2: [{1, 2}, {2, 3}],
        3: [{1, 3}],
        4: [{1, 4}],
        5: [{1, 5}]
    }

    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, slices_by_node, node)

    for ill_behaved in powerset(nodes):
        print(ill_behaved)
        intact = intact_nodes((is_slice_contained, nodes), ill_behaved)
        print('{0}-intact: {1}'.format(ill_behaved, intact))

    res_1 = intact_nodes((is_slice_contained, nodes), {1})
    assert res_1 == set()

    res_3 = intact_nodes((is_slice_contained, nodes), {3})
    assert res_3 == {1, 4, 5}

    res_45 = intact_nodes((is_slice_contained, nodes), {4, 5})
    assert res_45 == {1, 2, 3}
