"""Tests for quorum functions"""
from .utils.sets import deepfreezesets
from .quorum import get_minimal_quorum_intersection, quorum_intersection

QSET_DEFINITION = {'threshold': 2, 'nodes': {'A', 'B', 'C'}, 'children_definitions': []}
QSET_DEFINITION_WITHOUT_B = {'threshold': 1, 'nodes': {'A', 'C'}, 'children_definitions': []}

def test_quorum_intersection():
    """Test quorum_intersection()"""
    quorums = deepfreezesets([{'A', 'B'}, {'A', 'C'}, {'B', 'C'}])
    has_intersection, intersection_quorums, split_quorums = \
        quorum_intersection(quorums)
    assert has_intersection is True
    assert len(intersection_quorums) == 3
    assert not split_quorums

def test_quorum_intersection_fail():
    """Test quorum_intersection()"""
    quorums = deepfreezesets([{'A', 'B'}, {'B', 'C'}, {'C', 'D'}])
    has_intersection, intersection_quorums, split_quorums = \
        quorum_intersection(quorums)
    assert has_intersection is False
    assert len(intersection_quorums) == 2
    assert len(split_quorums) == 1
    assert frozenset(split_quorums[0]) == deepfreezesets([{'A', 'B'}, {'C', 'D'}])

def test_minimal_intersection():
    """Test get_minimal_quorum_intersection()"""
    quorums = deepfreezesets([{'A', 'B'}, {'A', 'C'}, {'B', 'C'}])
    intersection, quorum_a, quorum_b = get_minimal_quorum_intersection(quorums)
    assert len(intersection) == 1
    assert len(quorum_a.intersection(quorum_b)) == 1

def test_minimal_intersection_fail():
    """Test get_minimal_quorum_intersection()"""
    quorums = deepfreezesets([{'A', 'B'}, {'B', 'C'}, {'C', 'D'}])
    intersection, quorum_a, quorum_b = get_minimal_quorum_intersection(quorums)
    assert intersection is None
    assert quorum_a.intersection(quorum_b) == set()
