"""Quorum slices tests"""
from .quorum_slices import get_dependencies_by_node

def test_get_dependencies_by_node():
    """Test get_dependencies_by_node()"""
    quorum_slices_by_node = {
        1: [[1, 2], [1, 3]],
        2: [[2, 3]],
        3: [[1, 3]],
        4: [[1, 4]]
    }
    dependencies_by_node = get_dependencies_by_node(quorum_slices_by_node)
    assert dependencies_by_node == {
        1: {2, 3},
        2: {3},
        3: {1},
        4: {1}
    }
