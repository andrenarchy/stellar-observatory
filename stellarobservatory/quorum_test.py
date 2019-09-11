"""Tests for quorum functions"""
import pytest
from .utils.sets import deepfreezesets
from .quorum import remove_from_qset_definition, get_normalized_qset_definition, \
    get_minimal_quorum_intersection, generate_quorum_slices, is_quorum, quorum_intersection, \
    contract_to_maximal_quorum, has_quorum_intersection

QSET_DEFINITION = {'threshold': 2, 'validators': ['A', 'B', 'C'], 'innerQuorumSets': []}
QSET_DEFINITION_WITHOUT_B = {'threshold': 1, 'validators': ['A', 'C'], 'innerQuorumSets': []}

@pytest.mark.parametrize('qset_definition,node,expected', [
    (QSET_DEFINITION, 'B', QSET_DEFINITION_WITHOUT_B),
    (
        {'threshold': 2, 'validators': ['D', 'E'], 'innerQuorumSets': [QSET_DEFINITION]},
        'B',
        {'threshold': 2, 'validators': ['D', 'E'], 'innerQuorumSets': [QSET_DEFINITION_WITHOUT_B]}
    )
])
def test_removal(qset_definition, node, expected):
    """Test remove_from_qset_definition()"""
    result = remove_from_qset_definition(qset_definition, node)
    assert result == expected


def test_normalization():
    """Test get_normalized_qset_definition()"""
    node = {
        'publicKey': 'B',
        'quorumSet': QSET_DEFINITION
    }
    normalized_qset_definition = get_normalized_qset_definition(node)
    expected_qset_definition = {
        'threshold': 2,
        'validators': ['B'],
        'innerQuorumSets': [QSET_DEFINITION_WITHOUT_B]
    }
    assert normalized_qset_definition == expected_qset_definition

def test_qslice_generation():
    """Test generate_quorum_slices()"""
    expected_sets_economic = deepfreezesets([{'A', 'B'}, {'A', 'C'}, {'B', 'C'}])
    result_economic = generate_quorum_slices(QSET_DEFINITION)
    assert deepfreezesets(result_economic) == expected_sets_economic
    expected_sets_full = set(expected_sets_economic)
    expected_sets_full.add(frozenset(['A', 'B', 'C']))
    result_full = generate_quorum_slices(QSET_DEFINITION, mode='full')
    assert deepfreezesets(result_full) == expected_sets_full

def test_is_quorum():
    """Test is_quorum()"""
    quorum_slices_by_public_key = {
        'A': [{'A', 'B'}, {'A', 'C'}, {'A', 'B', 'C'}],
        'B': [{'A', 'B'}],
        'C': [{'A', 'B', 'C', 'D'}]
    }
    assert is_quorum(quorum_slices_by_public_key, {'A', 'B'}) is True
    assert is_quorum(quorum_slices_by_public_key, {'A', 'B', 'C'}) is False

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

def test_has_quorum_intersection_false():
    """Test has_quorum_intersection()"""
    # Basically two disjoint quorums {A, B} and {D} (two SCCs)
    quorum_slices_by_node = {
        'A': [{'A', 'B'}, {'A', 'C'}, {'A', 'B', 'C'}],
        'B': [{'A', 'B'}],
        'C': [{'A', 'B', 'C', 'D'}],
        'D': [{'D'}]
    }

    assert has_quorum_intersection({1, 2, 3, 4}, quorum_slices_by_node) is False

def test_has_quorum_intersection_true():
    """Test has_quorum_intersection()"""
    # One SCC containing quorum {A, B}
    quorum_slices_by_node = {
        'A': [{'A', 'B'}, {'A', 'C'}, {'A', 'B', 'C'}],
        'B': [{'A', 'B'}],
        'C': [{'A', 'B', 'C'}]
    }

    assert has_quorum_intersection({'A', 'B', 'C', 'D'}, quorum_slices_by_node) is True


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
