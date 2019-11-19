"""Test for Torstens's quorum intersection checker (Lachowski variant)"""

from stellarobservatory.quorum_lachowski import contains_slice

from stellarobservatory.quorum_intersection import quorum_intersection


def test_has_quorum_intersection_false():
    """Test quorum_intersection() == False"""
    # Basically two disjoint quorums {A, B} and {D} (two SCCs)
    slices_by_node = {
        'A': [{'A', 'B'}, {'A', 'C'}, {'A', 'B', 'C'}],
        'B': [{'A', 'B'}],
        'C': [{'A', 'B', 'C', 'D'}],
        'D': [{'D'}]
    }

    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, slices_by_node, node)

    assert quorum_intersection((is_slice_contained, {'A', 'B', 'C', 'D'})) is False


def test_has_quorum_intersection_false_in_scc():
    """Test has_quorum_intersection() without intersection inside an scc.
    Disjoint SCCs:  {1, 2}, {3, 4}"""
    slices_by_node = {
        1: [{1, 2}, {1, 3}, {1, 4}],
        2: [{2, 1}, {2, 3}, {2, 4}],
        3: [{1, 3}, {2, 3}, {3, 4}],
        4: [{1, 4}, {2, 4}, {3, 4}]
    }

    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, slices_by_node, node)

    assert quorum_intersection((is_slice_contained, {1, 2, 3, 4})) is False

def test_has_quorum_intersection_false_two_max_scc():
    """Test has_quorum_intersection() without intersection with two max scc:
    Disjoint SCCs:  {2}, {3}"""
    slices_by_node = {
        1: [{1, 2, 3}],
        2: [{2}],
        3: [{3}]
    }

    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, slices_by_node, node)

    assert quorum_intersection((is_slice_contained, {1, 2, 3})) is False

def test_has_quorum_intersection_true():
    """Test has_quorum_intersection()"""
    # One SCC containing quorum {A, B}
    quorum_slices_by_node = {
        'A': [{'A', 'B'}, {'A', 'C'}, {'A', 'B', 'C'}],
        'B': [{'A', 'B'}],
        'C': [{'A', 'B', 'C'}]
    }

    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, quorum_slices_by_node, node)


    assert quorum_intersection((is_slice_contained, {'A', 'B', 'C'})) is True


def test_has_quorum_intersection_true_sccs():
    """Test has_quorum_intersection() with intersection with three sccs"""
    slices_by_node = {
        1: [{1, 2}, {1, 3}],
        2: [{2, 1}, {2, 3}],
        3: [{1, 3}, {2, 3}],
        4: [{1, 4}],
        5: [{2, 5}]
    }
    def is_slice_contained(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, slices_by_node, node)

    assert quorum_intersection((is_slice_contained, {1, 2, 3, 4, 5})) is True
