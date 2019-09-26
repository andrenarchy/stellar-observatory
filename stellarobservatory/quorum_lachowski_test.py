from .quorum_lachowski import contract_to_maximal_quorum, has_quorum_intersection

def test_contract_to_maximal_quorum():
    """Test contract_to_maximal_quorum()"""
    quorum_slices_by_public_key = {
        'A': [{'A', 'B'}, {'A', 'C'}, {'A', 'B', 'C'}],
        'B': [{'A', 'B'}],
        'C': [{'A', 'B', 'C', 'D'}]
    }
    # Quorum (gets contracted):
    assert contract_to_maximal_quorum({'A', 'B', 'C'}, quorum_slices_by_public_key) == {'A', 'B'}
    # Quorum (already maximal):
    assert contract_to_maximal_quorum({'A', 'B'}, quorum_slices_by_public_key) == {'A', 'B'}
    # No quorum:
    assert contract_to_maximal_quorum({'B', 'C'}, quorum_slices_by_public_key) == set()
    assert contract_to_maximal_quorum({'A'}, quorum_slices_by_public_key) == set()
    assert contract_to_maximal_quorum({'B'}, quorum_slices_by_public_key) == set()
    assert contract_to_maximal_quorum({'C'}, quorum_slices_by_public_key) == set()

def test_has_quorum_intersection_false():
    """Test has_quorum_intersection()"""
    # Basically two disjoint quorums {A, B} and {D} (two SCCs)
    quorum_slices_by_node = {
        'A': [{'A', 'B'}, {'A', 'C'}, {'A', 'B', 'C'}],
        'B': [{'A', 'B'}],
        'C': [{'A', 'B', 'C', 'D'}],
        'D': [{'D'}]
    }

    assert has_quorum_intersection({'A', 'B', 'C', 'D'}, quorum_slices_by_node) is False

def test_has_quorum_intersection_false_in_scc():
    slices_by_node = {
        1: [{1, 2}, {1, 3}, {1, 4}],
        2: [{2, 1}, {2, 3}, {2, 4}],
        3: [{1, 3}, {2, 3}, {3, 4}],
        4: [{1, 4}, {2, 4}, {3, 4}]
    }
    assert has_quorum_intersection({1, 2, 3, 4}, slices_by_node) is False

def test_has_quorum_intersection_true():
    """Test has_quorum_intersection()"""
    # One SCC containing quorum {A, B}
    quorum_slices_by_node = {
        'A': [{'A', 'B'}, {'A', 'C'}, {'A', 'B', 'C'}],
        'B': [{'A', 'B'}],
        'C': [{'A', 'B', 'C'}]
    }

    assert has_quorum_intersection({'A', 'B', 'C', 'D'}, quorum_slices_by_node) is True
