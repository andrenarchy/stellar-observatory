"""Tests for quorum functions"""
import pytest
from .utils.sets import deepfreezesets
from .quorum import remove_from_qset_definition, get_normalized_qset_definition, \
    generate_quorum_slices

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
