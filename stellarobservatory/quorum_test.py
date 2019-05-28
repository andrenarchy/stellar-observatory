"""Tests for quorum functions"""
import pytest
from .quorum import remove_from_qset_definition, get_normalized_qset_definition

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
