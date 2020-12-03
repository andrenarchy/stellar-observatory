"""Utilities for hypergraphs"""
from typing import FrozenSet, List, Set, Tuple

import numpy

from .graph import Node, Nodes

Hyperedges = Set[FrozenSet[Node]]
Hypergraph = Tuple[Nodes, Hyperedges]
DirectedHyperedges = Set[Tuple[FrozenSet[Node], FrozenSet[Node]]]
DirectedHypergraph = Tuple[Nodes, DirectedHyperedges]

def get_hypergraph_incidence_matrix(node_list: List[Node],
                                    hyperedge_list: List[Set[Node]]
                                    ) -> numpy.array:
    """Get the incidence matrix of a hypergraph"""
    node_to_index = {node: index for index, node in enumerate(node_list)}
    incidence_matrix = numpy.zeros((len(node_list), len(hyperedge_list)),
                                   dtype=int)
    for hyperedge_index, hyperedge in enumerate(hyperedge_list):
        for node in hyperedge:
            incidence_matrix[node_to_index[node], hyperedge_index] = 1
    return incidence_matrix

def get_hypergraph_adjacency_matrix(node_list: List[Node],
                                    hyperedge_list: List[Set[Node]]
                                    ) -> numpy.array:
    """Get the adjacency matrix of a hypergraph"""
    incidence_matrix = get_hypergraph_incidence_matrix(node_list, hyperedge_list)
    mmt = incidence_matrix.dot(incidence_matrix.T)
    return mmt - numpy.diag(numpy.diag(mmt))
