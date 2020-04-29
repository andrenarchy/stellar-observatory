"""Nodes tests"""
from .nodes import get_nodes_from_stellarbeat, get_nodes_by_public_key, \
    get_node_dependencies, get_trust_graph

def test_stellarbeat_nodes():
    """Test get_nodes_from_stellarbeat()"""
    nodes = get_nodes_from_stellarbeat()
    assert isinstance(nodes, list)
    for node in nodes:
        assert isinstance(node, dict)
        assert 'publicKey' in node

nodes_ABCDE = [
    {
        'publicKey': 'A',
        'quorumSet': {'threshold': 2, 'validators': ['A', 'B'], 'innerQuorumSets': []}
    },
    {
        'publicKey': 'B',
        'quorumSet': {
            'threshold': 2,
            'validators': ['B'],
            'innerQuorumSets':[
                {'threshold': 1, 'validators': ['A', 'C'], 'innerQuorumSets': []}
            ]
        }
    },
    {
        'publicKey': 'C',
        'quorumSet': {'threshold': 2, 'validators': ['A', 'C'], 'innerQuorumSets': []}
    },
    {
        'publicKey': 'D',
        'quorumSet': {'threshold': 2, 'validators': ['A', 'B', 'C', 'D'], 'innerQuorumSets': []}
    },
    {
        'publicKey': 'E',
        'quorumSet':{
            'threshold': 2,
            'validators': ['A'],
            'innerQuorumSets':[
                {'threshold': 1, 'validators': ['A', 'D'], 'innerQuorumSets': []}
            ]
        }
    },
]

def test_node_dependencies():
    """Test get_node_dependencies()"""
    nodes_by_public_key = get_nodes_by_public_key(nodes_ABCDE)
    dependencies_a = get_node_dependencies(nodes_by_public_key, 'A')
    assert frozenset(dependencies_a) == frozenset(['A', 'B', 'C'])
    dependencies_a_int = get_node_dependencies(nodes_by_public_key, 'A', transitive=False)
    assert frozenset(dependencies_a_int) == frozenset(['A', 'B'])
    dependencies_d = get_node_dependencies(nodes_by_public_key, 'D')
    assert frozenset(dependencies_d) == frozenset(['A', 'B', 'C', 'D'])
    dependencies_e_int = get_node_dependencies(nodes_by_public_key, 'E', transitive=False)
    assert frozenset(dependencies_e_int) == frozenset(['A', 'D', 'E'])

def test_get_trust_graph():
    """Test get_trust_graph()"""
    nodes_by_public_key = get_nodes_by_public_key(nodes_ABCDE)
    trust_graphs = get_trust_graph(nodes_by_public_key)
    assert isinstance(trust_graphs, dict)
    assert len(trust_graphs) == 5
    assert trust_graphs['A'] == frozenset(['B'])
    assert trust_graphs['B'] == frozenset(['A', 'C'])
    assert trust_graphs['C'] == frozenset(['A'])
    assert trust_graphs['D'] == frozenset(['A', 'B', 'C'])
    assert trust_graphs['E'] == frozenset(['A', 'D'])
