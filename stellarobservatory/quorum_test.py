"""Tests for quorum functions"""
from .quorum import remove_from_qset_definition, get_normalized_qset_definition
import pytest

qset_definition = {'threshold': 2, 'validators': ['A', 'B', 'C'], 'innerQuorumSets': []}
qset_definition_without_B = {'threshold': 1, 'validators': ['A', 'C'], 'innerQuorumSets': []}
@pytest.mark.parametrize('qset_definition,node,expected', [
  (qset_definition, 'B', qset_definition_without_B),
  (
    {'threshold': 2, 'validators': ['D', 'E'], 'innerQuorumSets': [qset_definition]},
    'B',
    {'threshold': 2, 'validators': ['D', 'E'], 'innerQuorumSets': [qset_definition_without_B]}
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
      'quorumSet': qset_definition
    }
    normalized_qset_definition = get_normalized_qset_definition(node)
    expected_qset_definition = {
      'threshold': 2,
      'validators': ['B'],
      'innerQuorumSets': [qset_definition_without_B]
    }
    assert normalized_qset_definition == expected_qset_definition
