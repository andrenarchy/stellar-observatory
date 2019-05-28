"""Nodes tests"""
from .nodes import get_nodes_from_stellarbeat

def test_get_nodes_from_stellarbeat():
    """Test stellarbeat response"""
    nodes = get_nodes_from_stellarbeat()
    assert isinstance(nodes, list)
    for node in nodes:
        assert isinstance(node, dict)
        assert 'publicKey' in node
