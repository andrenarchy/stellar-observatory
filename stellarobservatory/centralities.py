from typing import Callable, List, Set
import numpy
from scipy.linalg import eig, expm

from .intactness import get_intact_nodes
from .quorum_slice_definition import Definitions, get_direct_dependencies, get_is_slice_contained
from .utils.graph import Node
from .utils.sets import powerset

def get_adjacency_matrix(nodes: List[Node], definitions: Definitions):
    node_to_index = { node: index for index, node in enumerate(nodes) }
    M = numpy.zeros((len(nodes), len(nodes)), dtype=int)
    for node in nodes:
        dependencies = get_direct_dependencies(definitions, node)
        for dependency in dependencies:
            if dependency != node:
                M[node_to_index[node], node_to_index[dependency]] = 1
    return M

def get_eigenvector_centralities(adjacency_matrix: numpy.array):
    eigenvalues, eigenvectors = eig(adjacency_matrix, left=True, right=False)
    index = numpy.argsort(numpy.real(eigenvalues))[-1]
    centralities = numpy.abs(eigenvectors[:, index])
    return centralities / numpy.max(centralities)

def get_subgraph_centralities(adjacency_matrix: numpy.array):
    expA = expm(adjacency_matrix)
    centralities = numpy.diag(expA)
    return centralities / numpy.max(centralities)

def get_befouling_centralities(nodes: List[Node], definitions: Definitions, get_ill_behaved_weight: Callable[[Set[Node]], float]) -> numpy.array:
    fbas = (get_is_slice_contained(definitions), set(nodes))
    node_to_index = { node: index for index, node in enumerate(nodes) }
    M = numpy.zeros((len(nodes), len(nodes)))
    for ill_behaved_nodes in powerset(nodes):
        if ill_behaved_nodes == set() or ill_behaved_nodes == set(nodes):
            continue
        intact_nodes = get_intact_nodes(fbas, ill_behaved_nodes)
        befouled_nodes = set(nodes).difference(intact_nodes)
        induced_befouled_nodes = befouled_nodes.difference(ill_behaved_nodes)
        ill_behaved_weight = get_ill_behaved_weight(ill_behaved_nodes)
        for ill_behaved_node in ill_behaved_nodes:
            for induced_befouled_node in induced_befouled_nodes:
                M[node_to_index[ill_behaved_node], node_to_index[induced_befouled_node]] += ill_behaved_weight
    eigenvalues, eigenvectors = eig(M)
    index = numpy.argsort(numpy.real(eigenvalues))[-1]
    centralities = numpy.abs(eigenvectors[:, index])
    return centralities / numpy.max(centralities)
