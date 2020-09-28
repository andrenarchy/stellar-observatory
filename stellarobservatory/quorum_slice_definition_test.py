"""Tests for quorum functions"""
import pytest
from .utils.sets import deepfreezesets
from .quorum_slice_definition import get_direct_dependencies, get_transitive_dependencies, \
    get_trust_graph, generate_quorum_slices, get_normalized_definition, \
    remove_from_definition, satisfies_definition


DEFINITIONS_BY_NODE_ABCDE = {
    'A': {'threshold': 2, 'nodes': ['A', 'B'], 'children_definitions': []},
    'B': {'threshold': 2, 'nodes': ['B'], 'children_definitions': [
        {'threshold': 1, 'nodes': ['A', 'C'], 'children_definitions': []}
    ]},
    'C': {'threshold': 2, 'nodes': ['A', 'C'], 'children_definitions': []},
    'D': {'threshold': 2, 'nodes': ['A', 'B', 'C', 'D'], 'children_definitions': []},
    'E': {'threshold': 2, 'nodes': ['A'], 'children_definitions': [
        {'threshold': 1, 'nodes': ['A', 'D'], 'children_definitions': []},
    ]},
}

@pytest.mark.parametrize('definitions_by_node,node,expected', [
    (DEFINITIONS_BY_NODE_ABCDE, 'A', set(['B'])),
    (DEFINITIONS_BY_NODE_ABCDE, 'B', set(['A', 'C'])),
    (DEFINITIONS_BY_NODE_ABCDE, 'C', set(['A'])),
    (DEFINITIONS_BY_NODE_ABCDE, 'D', set(['A', 'B', 'C'])),
    (DEFINITIONS_BY_NODE_ABCDE, 'E', set(['A', 'D']))
])
def test_get_direct_dependencies(definitions_by_node, node, expected):
    """Test get_direct_dependencies()"""
    assert get_direct_dependencies(definitions_by_node, node) == expected

@pytest.mark.parametrize('definitions_by_node,node,expected', [
    (DEFINITIONS_BY_NODE_ABCDE, 'A', set(['B', 'C'])),
    (DEFINITIONS_BY_NODE_ABCDE, 'B', set(['A', 'C'])),
    (DEFINITIONS_BY_NODE_ABCDE, 'C', set(['A', 'B'])),
    (DEFINITIONS_BY_NODE_ABCDE, 'D', set(['A', 'B', 'C'])),
    (DEFINITIONS_BY_NODE_ABCDE, 'E', set(['A', 'B', 'C', 'D']))
])
def test_get_transitive_dependencies(definitions_by_node, node, expected):
    """Test get_transitive_dependencies()"""
    assert get_transitive_dependencies(definitions_by_node, node) == expected

def test_get_trust_graph():
    """Test get_trust_graph()"""
    assert get_trust_graph(DEFINITIONS_BY_NODE_ABCDE) == {
        'A': {'B'},
        'B': {'A', 'C'},
        'C': {'A'},
        'D': {'A', 'B', 'C'},
        'E': {'A', 'D'}
    }

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
