"""Utilities for graphs"""

def get_transpose_graph(graph):
    """Get the transpose graph"""
    transpose = {node: set() for node in graph.keys()}
    for node, target_nodes in graph.items():
        for target_node in target_nodes:
            transpose[target_node].add(node)
    return transpose

def get_indegrees(graph):
    """Get a dict with indegrees for all nodes"""
    transpose = get_transpose_graph(graph)
    return {node: len(target_nodes) for node, target_nodes in transpose.items()}

def get_induced_subgraph(graph, nodes):
    """Get the nodes-induced subgraph G[S] for a graph G and a subset of nodes S"""
    return {node: graph[node].intersection(nodes) for node in nodes}

def get_dependencies(graph, node):
    """Get the dependencies of a node"""
    dependencies = set()
    def traverse_nodes(nodes):
        for candidate in nodes:
            if candidate not in dependencies:
                dependencies.add(candidate)
                traverse_nodes(graph[candidate])
    traverse_nodes(graph[node])
    dependencies.discard(node)
    return dependencies
