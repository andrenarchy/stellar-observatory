import logging

from stellarobservatory.quorum_lachowski import contains_slice

from stellarobservatory.quorum_intersection import quorum_intersection


def test_has_quorum_intersection_false():
    """Test failing has_quorum_intersection()"""
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
