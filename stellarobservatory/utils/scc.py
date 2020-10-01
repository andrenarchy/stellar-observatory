"""Utilities for strongly connected components"""
from typing import Dict, List, Tuple
import numpy
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

from .graph import Node, Nodes, Graph

NodeIndexes = Dict[Node, int]

def get_graph_csr_matrix(graph: Graph, nodes: List[Node], node_index_by_node: NodeIndexes):
    """
    Get CSR matrix representation of graph
    """
    row_indexes = []
    col_indexes = []
    for node, targets in graph.items():
        row_indexes += [node_index_by_node[node]] * len(targets)
        col_indexes += [node_index_by_node[target] for target in targets]
    data = numpy.ones((len(row_indexes)), dtype=int)
    n_nodes = len(nodes)
    return csr_matrix((data, (row_indexes, col_indexes)), shape=(n_nodes, n_nodes))

def get_scc_graph(graph: Graph, nodes: List[Node], node_index_by_node: NodeIndexes,
                  labels: List[int], n_components: int):
    """
    Get SCCs as graph
    """
    sccs: List[Nodes] = [set() for i in range(n_components)]
    scc_graph: Graph = dict()
    for index, label in enumerate(labels):
        node = nodes[index]
        sccs[label].add(node)
        if label not in scc_graph:
            scc_graph[label] = set()
        for target_node in graph[node]:
            target_index = node_index_by_node[target_node]
            target_label = labels[target_index]
            if target_label != label:
                scc_graph[label].add(labels[target_index])
    return sccs, scc_graph


def get_strongly_connected_components(graph: Graph) -> Tuple[List[Nodes], Graph]:
    """
    Get strongly connected components for a directed graph

    The returned list of components is in reverse topological order, i.e.,
    such that the nodes in the first component have no dependencies on
    other components.
    """
    nodes = list(graph.keys())
    node_index_by_node = {node: index for index, node in enumerate(nodes)}
    csgraph = get_graph_csr_matrix(graph, nodes, node_index_by_node)
    n_components, labels = connected_components(csgraph, directed=True, connection='strong')
    sccs, scc_graph = get_scc_graph(graph, nodes, node_index_by_node, labels, n_components)
    return sccs, scc_graph
