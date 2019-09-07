"""Utilities for strongly connected components"""
import numpy
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

def get_strongly_connected_components(graph):
    """
    Get strongly connected components for a directed graph

    The returned list of components is ordered by dependency, i.e.,
    such that the nodes in the first component have no dependencies on
    other components.
    """
    nodes = list(graph.keys())
    node_index_by_node = {node: index for index, node in enumerate(nodes)}
    row_indexes = []
    col_indexes = []
    for node, targets in graph.items():
        row_indexes += [node_index_by_node[node]] * len(targets)
        col_indexes += [node_index_by_node[target] for target in targets]
    data = numpy.ones((len(row_indexes)), dtype=int)
    csgraph = csr_matrix((data, (row_indexes, col_indexes)))
    n_components, labels = connected_components(csgraph, directed=True, connection='strong')
    sccs = [[] for i in range(n_components)]
    for index, label in enumerate(labels):
        sccs[label] += [nodes[index]]
    return [frozenset(scc) for scc in sccs]
