"""Test for Lachowski's quorum intersection function"""
from .quorum_lachowski import greatest_quorum, has_quorum_intersection

def test_greatest_quorum():
    """Test greatest_quorum()"""
    # pylint: disable=duplicate-code
    quorum_slices_by_public_key = {
        'A': [{'A', 'B'}, {'A', 'C'}, {'A', 'B', 'C'}],
        'B': [{'A', 'B'}],
        'C': [{'A', 'B', 'C', 'D'}]
    }
    # Quorum (gets contracted):
    assert greatest_quorum({'A', 'B', 'C'}, quorum_slices_by_public_key) == {'A', 'B'}
    # Quorum (already maximal):
    assert greatest_quorum({'A', 'B'}, quorum_slices_by_public_key) == {'A', 'B'}
    # No quorum:
    assert greatest_quorum({'B', 'C'}, quorum_slices_by_public_key) == set()
    assert greatest_quorum({'A'}, quorum_slices_by_public_key) == set()
    assert greatest_quorum({'B'}, quorum_slices_by_public_key) == set()
    assert greatest_quorum({'C'}, quorum_slices_by_public_key) == set()

def test_has_quorum_intersection_false():
    """Test failing has_quorum_intersection()"""
    # Basically two disjoint quorums {A, B} and {D} (two SCCs)
    quorum_slices_by_node = {
        'A': [{'A', 'B'}, {'A', 'C'}, {'A', 'B', 'C'}],
        'B': [{'A', 'B'}],
        'C': [{'A', 'B', 'C', 'D'}],
        'D': [{'D'}]
    }

    assert has_quorum_intersection(quorum_slices_by_node) is False

def test_has_quorum_intersection_false_in_scc():
    """Test has_quorum_intersection() without intersection inside an scc"""
    slices_by_node = {
        1: [{1, 2}, {1, 3}, {1, 4}],
        2: [{2, 1}, {2, 3}, {2, 4}],
        3: [{1, 3}, {2, 3}, {3, 4}],
        4: [{1, 4}, {2, 4}, {3, 4}]
    }
    assert has_quorum_intersection(slices_by_node) is False

def test_has_quorum_intersection_false_two_max_scc():
    """Test has_quorum_intersection() without intersection with two max scc"""
    slices_by_node = {
        1: [{1, 2, 3}],
        2: [{2}],
        3: [{3}]
    }
    assert has_quorum_intersection(slices_by_node) is False

def test_has_quorum_intersection_true():
    """Test has_quorum_intersection()"""
    # One SCC containing quorum {A, B}
    quorum_slices_by_node = {
        'A': [{'A', 'B'}, {'A', 'C'}, {'A', 'B', 'C'}],
        'B': [{'A', 'B'}],
        'C': [{'A', 'B', 'C'}]
    }

    assert has_quorum_intersection(quorum_slices_by_node) is True

def test_has_quorum_intersection_true_sccs():
    """Test has_quorum_intersection() with intersection with three sccs"""
    slices_by_node = {
        1: [{1, 2}, {1, 3}],
        2: [{2, 1}, {2, 3}],
        3: [{1, 3}, {2, 3}],
        4: [{1, 4}],
        5: [{2, 5}]
    }
    assert has_quorum_intersection(slices_by_node) is True
