"""Utilities for graphs"""

def compute_transpose_graph(graph):
    """Compute the transpose graph"""
    transpose = {node: set() for node in graph.keys()}
    for node, target_nodes in graph.items():
        for target_node in target_nodes:
            transpose[target_node].add(node)
    return transpose
