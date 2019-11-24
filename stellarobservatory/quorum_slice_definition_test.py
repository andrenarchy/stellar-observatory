"""Tests for quorum functions"""
import pytest
from .utils.sets import deepfreezesets
from .quorum_slice_definition import generate_quorum_slices, get_normalized_definition, \
    remove_from_definition, satisfies_definition

DEFINITION = {'threshold': 2, 'nodes': {'A', 'B', 'C'}, 'children_definitions': []}
DEFINITION_WITHOUT_B = {'threshold': 1, 'nodes': {'A', 'C'}, 'children_definitions': []}

@pytest.mark.parametrize('definition,node,expected', [
    (DEFINITION, 'B', DEFINITION_WITHOUT_B),
    (
        {'threshold': 2, 'nodes': {'D', 'E'}, 'children_definitions': [DEFINITION]},
        'B',
        {'threshold': 2, 'nodes': {'D', 'E'}, 'children_definitions': [DEFINITION_WITHOUT_B]}
    )
])
def test_removal(definition, node, expected):
    """Test remove_from_definition()"""
    result = remove_from_definition(definition, node)
    assert result == expected


def test_normalization():
    """Test get_normalized_definition()"""
    normalized_definition = get_normalized_definition(DEFINITION, 'B')
    expected_definition = {
        'threshold': 2,
        'nodes': {'B'},
        'children_definitions': [DEFINITION_WITHOUT_B]
    }
    assert normalized_definition == expected_definition

def test_qslice_generation():
    """Test generate_quorum_slices()"""
    expected_sets_economic = deepfreezesets([{'A', 'B'}, {'A', 'C'}, {'B', 'C'}])
    result_economic = generate_quorum_slices(DEFINITION)
    assert deepfreezesets(result_economic) == expected_sets_economic
    expected_sets_full = set(expected_sets_economic)
    expected_sets_full.add(frozenset(['A', 'B', 'C']))
    result_full = generate_quorum_slices(DEFINITION, mode='full')
    assert deepfreezesets(result_full) == expected_sets_full

def test_satisfies_definition():
    """Test satisfies_definition()"""
    assert satisfies_definition({'A', 'C'}, DEFINITION) is True
    assert satisfies_definition({'A'}, DEFINITION) is False
    nested_definition = {'threshold': 2, 'nodes': {'D'}, 'children_definitions': [DEFINITION]}
    assert satisfies_definition({'A', 'C', 'D'}, nested_definition) is True
    assert satisfies_definition({'A', 'C'}, nested_definition) is False
