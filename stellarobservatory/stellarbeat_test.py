"""Stellarbeat tests"""

from stellarobservatory.stellarbeat import get_nodes_from_stellarbeat

def test_stellarbeat_nodes():
    """Test get_nodes_from_stellarbeat()"""
    nodes = get_nodes_from_stellarbeat()
    assert isinstance(nodes, list)
    for node in nodes:
        assert isinstance(node, dict)
        assert 'publicKey' in node
