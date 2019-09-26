"""Test graph utilities"""
from .graph import compute_transpose_graph

def test_compute_transpose_graph():
    """Test compute_transpose_graph() with a graph"""
    graph = {
        1: {2, 3},
        2: {3},
        3: {2}
    }
    transpose = compute_transpose_graph(graph)
    assert transpose == {
        1: set(),
        2: {1, 3},
        3: {1, 2}
    }
