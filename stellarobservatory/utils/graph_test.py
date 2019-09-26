"""Test graph utilities"""
from .graph import compute_transpose_graph, get_induced_subgraph

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

def test_get_induced_subgraph():
    """Test get_induced_subgraph() with a graph"""
    graph = {
        1: {2, 3},
        2: {3},
        3: {2}
    }
    assert get_induced_subgraph(graph, {1, 2, 3}) == graph
    assert get_induced_subgraph(graph, {1}) == {1: set()}
    assert get_induced_subgraph(graph, {1, 2}) == {1: {2}, 2: set()}
    assert get_induced_subgraph(graph, {2, 3}) == {2: {3}, 3: {2}}
    assert get_induced_subgraph(graph, set()) == dict()
