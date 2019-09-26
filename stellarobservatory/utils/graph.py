"""Utilities for graphs"""

def compute_transpose_graph(graph):
    """Compute the transpose graph"""
    transpose = {node: set() for node in graph.keys()}
    for node, target_nodes in graph.items():
        for target_node in target_nodes:
            transpose[target_node].add(node)
    return transpose

def get_induced_subgraph(graph, nodes):
    """Get the nodes-induced subgraph G[S] for a graph G and a subset of nodes S"""
    return {node: graph[node].intersection(nodes) for node in nodes}
