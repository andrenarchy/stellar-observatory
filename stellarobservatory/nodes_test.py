"""Nodes tests"""
from .nodes import get_nodes_from_stellarbeat, get_nodes_by_public_key, \
    get_node_dependencies

def test_stellarbeat_nodes():
    """Test get_nodes_from_stellarbeat()"""
    nodes = get_nodes_from_stellarbeat()
    assert isinstance(nodes, list)
    for node in nodes:
        assert isinstance(node, dict)
        assert 'publicKey' in node

def test_node_dependencies():
    """Test get_node_dependencies()"""
    nodes = [
        {
            'publicKey': 'A',
            'quorumSet': {'threshold': 2, 'validators': ['A', 'B'], 'innerQuorumSets': []}
        },
        {
            'publicKey': 'B',
            'quorumSet': {
                'threshold': 2,
                'validators': ['B'],
                'innerQuorumSets':[{'threshold': 1, 'validators': ['A', 'C'], 'innerQuorumSets': []}]
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
    ]
    nodes_by_public_key = get_nodes_by_public_key(nodes)
    dependencies_A = get_node_dependencies(nodes_by_public_key, 'A')
    assert frozenset(dependencies_A) == frozenset(['A', 'B', 'C'])
    dependencies_D = get_node_dependencies(nodes_by_public_key, 'D')
    assert frozenset(dependencies_D) == frozenset(['A', 'B', 'C', 'D'])
