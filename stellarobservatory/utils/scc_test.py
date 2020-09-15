"""Test scc utilities"""
from .scc import get_strongly_connected_components

def test_get_strongly_connected_components():
    """Test get_strongly_connected_components() with a graph"""
    graph = {
        # SCC 1
        1: {2, 3, 4},
        2: {1, 3, 4},
        3: {1, 2, 4},
        4: {1, 2, 3},
        # SCC 2
        5: {1, 6},
        6: {7},
        7: {8},
        8: {9},
        9: {5}
    }
    sccs, scc_graph = get_strongly_connected_components(graph)
    assert sccs == [{1, 2, 3, 4}, {5, 6, 7, 8, 9}]
    assert scc_graph == {0: set(), 1: {0}}
