"""Utilities for graphs"""

import numpy
from typing import Dict, List, Set, TypeVar

Node = TypeVar('Node')
Nodes = Set[Node]
Graph = Dict[Node, Nodes]

def get_transpose_graph(graph: Graph):
    """Get the transpose graph"""
    transpose: Graph = {node: set() for node in graph.keys()}
    for node, target_nodes in graph.items():
        for target_node in target_nodes:
            transpose[target_node].add(node)
    return transpose

def get_indegrees(graph: Graph):
    """Get a dict with indegrees for all nodes"""
    transpose = get_transpose_graph(graph)
    return {node: len(target_nodes) for node, target_nodes in transpose.items()}

def get_induced_subgraph(graph: Graph, nodes: Nodes):
    """Get the nodes-induced subgraph G[S] for a graph G and a subset of nodes S"""
    return {node: graph[node].intersection(nodes) for node in nodes}

def get_dependencies(graph: Graph, node: Node):
    """Get the dependencies of a node"""
    dependencies: Set[Node] = set()
    def traverse_nodes(nodes):
        for candidate in nodes:
            if candidate not in dependencies:
                dependencies.add(candidate)
                traverse_nodes(graph[candidate])
    traverse_nodes(graph[node])
    dependencies.discard(node)
    return dependencies

def get_adjacency_matrix(node_list: List[Node], graph: Graph):
    """Get the adjacency matrix of a graph"""
    node_to_index = { node: index for index, node in enumerate(node_list) }
    M = numpy.zeros((len(node_list), len(node_list)), dtype=int)
    for node in node_list:
        for dependency in graph[node]:
            if dependency != node:
                M[node_to_index[node], node_to_index[dependency]] = 1
    return M
