from itertools import chain, combinations
from stellarobservatory.quorums import enumerate_quorums, traverse_quorums
from typing import Callable, Dict, FrozenSet, List, Set
import numpy
from scipy.linalg import eig, expm

from .intactness import get_intact_nodes
from .quorum_slice_definition import Definitions, get_direct_dependencies, get_is_slice_contained, get_trust_graph
from .utils.graph import get_adjacency_matrix, get_dependencies, get_transpose_graph, Node, Nodes
from .utils.hypergraph import Hypergraph, get_hypergraph_adjacency_matrix, get_hypergraph_incidence_matrix
from .utils.scc import get_strongly_connected_components
from .utils.sets import powerset

def get_eigenvector_centralities(nodes: List[Node], definitions: Definitions) -> numpy.array:
    trust_graph = get_trust_graph(definitions)
    adjacency_matrix = get_adjacency_matrix(nodes, trust_graph)
    eigenvalues, eigenvectors = eig(adjacency_matrix, left=True, right=False)
    index = numpy.argsort(numpy.real(eigenvalues))[-1]
    centralities = numpy.abs(eigenvectors[:, index])
    return centralities / numpy.max(centralities)

def get_subgraph_centralities(nodes: List[Node], definitions: Definitions) -> numpy.array:
    trust_graph = get_trust_graph(definitions)
    adjacency_matrix = get_adjacency_matrix(nodes, trust_graph)
    expA = expm(adjacency_matrix)
    centralities = numpy.diag(expA)
    return centralities / numpy.max(centralities)

def get_quorum_eigenvector_centralities(nodes: List[Node], definitions: Definitions) -> numpy.array:
    fbas = (get_is_slice_contained(definitions), set(nodes))
    hyperedge_list = list(enumerate_quorums(fbas))
    incidence_matrix = get_hypergraph_incidence_matrix(nodes, hyperedge_list)
    MMT = incidence_matrix.dot(incidence_matrix.T)
    eigenvalues, eigenvectors = eig(MMT)
    index = numpy.argsort(numpy.real(eigenvalues))[-1]
    centralities = numpy.abs(eigenvectors[:, index])
    return centralities / numpy.max(centralities)

def get_quorum_subgraph_centralities(nodes: List[Node], definitions: Definitions) -> numpy.array:
    fbas = (get_is_slice_contained(definitions), set(nodes))
    hyperedge_list = list(enumerate_quorums(fbas))
    adjacency_matrix = get_hypergraph_adjacency_matrix(nodes, hyperedge_list)
    expA = expm(adjacency_matrix)
    centralities = numpy.diag(expA)
    return centralities / numpy.max(centralities)

def get_quorum_intersection_eigenvector_centralities(nodes: List[Node], definitions: Definitions) -> numpy.array:
    fbas = (get_is_slice_contained(definitions), set(nodes))
    quorums = list(enumerate_quorums(fbas))
    hyperedge_list = list([a.intersection(b) for a, b in combinations(quorums, 2)])
    incidence_matrix = get_hypergraph_incidence_matrix(nodes, hyperedge_list)
    MMT = incidence_matrix.dot(incidence_matrix.T)
    eigenvalues, eigenvectors = eig(MMT)
    index = numpy.argsort(numpy.real(eigenvalues))[-1]
    centralities = numpy.abs(eigenvectors[:, index])
    return centralities / numpy.max(centralities)

def get_quorum_intersection_subgraph_centralities(nodes: List[Node], definitions: Definitions) -> numpy.array:
    fbas = (get_is_slice_contained(definitions), set(nodes))
    quorums = list(enumerate_quorums(fbas))
    hyperedge_list = list([a.intersection(b) for a, b in combinations(quorums, 2)])
    adjacency_matrix = get_hypergraph_adjacency_matrix(nodes, hyperedge_list)
    expA = expm(adjacency_matrix)
    centralities = numpy.diag(expA)
    return centralities / numpy.max(centralities)

def get_befouledness_matrix(nodes: List[Node], definitions: Definitions, get_ill_behaved_weight: Callable[[Set[Node]], float]) -> numpy.array:
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
    return M

def get_befouledness_eigenvector_centralities(nodes: List[Node], definitions: Definitions, get_ill_behaved_weight: Callable[[Set[Node]], float]) -> numpy.array:
    M = get_befouledness_matrix(nodes, definitions, get_ill_behaved_weight)
    eigenvalues, eigenvectors = eig(M)
    index = numpy.argsort(numpy.real(eigenvalues))[-1]
    centralities = numpy.abs(eigenvectors[:, index])
    return centralities / numpy.max(centralities)

def get_befouledness_lgs_centralities(nodes: List[Node], definitions: Definitions, get_ill_behaved_weight: Callable[[Set[Node]], float], get_mu: Callable[[numpy.array], float]) -> numpy.array:
    M = get_befouledness_matrix(nodes, definitions, get_ill_behaved_weight)
    A = numpy.eye(len(nodes)) - get_mu(M) * M
    centralities = numpy.linalg.solve(A, numpy.ones(len(nodes)))

    return centralities / numpy.max(centralities)

def get_hierarchical_befouledness_matrix(nodes: List[Node], definitions: Definitions, get_ill_behaved_weight: Callable[[Set[Node]], float]) -> numpy.array:
    fbas = (get_is_slice_contained(definitions), set(nodes))
    node_to_index = { node: index for index, node in enumerate(nodes) }
    M = numpy.zeros((len(nodes), len(nodes)))

    trust_graph = get_trust_graph(definitions)
    sccs, scc_graph = get_strongly_connected_components(trust_graph)
    scc_graph_transpose = get_transpose_graph(scc_graph)

    for scc_index in scc_graph.keys():
        scc_dependencies = get_dependencies(scc_graph, scc_index)
        dependencies: Set[Node] = set()
        [dependencies.update(sccs[dependency]) for dependency in scc_dependencies]
        scc_dependents = get_dependencies(scc_graph_transpose, scc_index)
        dependents: Set[Node] = set()
        [dependents.update(sccs[dependent]) for dependent in scc_dependents]

        for ill_behaved_nodes in powerset(dependencies.union(sccs[scc_index])):
            if ill_behaved_nodes == set() or ill_behaved_nodes == set(nodes):
                continue
            intact_nodes = get_intact_nodes(fbas, ill_behaved_nodes)
            befouled_nodes = set(nodes).difference(intact_nodes)
            induced_befouled_nodes = befouled_nodes.difference(ill_behaved_nodes)
            affected_befouled_nodes = induced_befouled_nodes.intersection(sccs[scc_index].union(dependents))
            ill_behaved_weight = get_ill_behaved_weight(ill_behaved_nodes)
            for ill_behaved_node in ill_behaved_nodes:
                for affected_befouled_node in affected_befouled_nodes:
                    M[node_to_index[ill_behaved_node], node_to_index[affected_befouled_node]] += ill_behaved_weight
    return M

def get_hierarchical_befouledness_eigenvector_centralities(nodes: List[Node], definitions: Definitions, get_ill_behaved_weight: Callable[[Set[Node]], float]) -> numpy.array:
    M = get_hierarchical_befouledness_matrix(nodes, definitions, get_ill_behaved_weight)
    eigenvalues, eigenvectors = eig(M)
    index = numpy.argsort(numpy.real(eigenvalues))[-1]
    centralities = numpy.abs(eigenvectors[:, index])
    return centralities / numpy.max(centralities)

def get_hierarchical_befouledness_lgs_centralities(nodes: List[Node], definitions: Definitions, get_ill_behaved_weight: Callable[[Set[Node]], float], get_mu: Callable[[numpy.array], float]) -> numpy.array:
    M = get_hierarchical_befouledness_matrix(nodes, definitions, get_ill_behaved_weight)
    A = numpy.eye(len(nodes)) - get_mu(M) * M
    centralities = numpy.linalg.solve(A, numpy.ones(len(nodes)))
    return centralities / numpy.max(centralities)

def get_minimal_befouledness_matrix(nodes: List[Node], definitions: Definitions, get_ill_behaved_weight: Callable[[Set[Node]], float]) -> numpy.array:
    fbas = (get_is_slice_contained(definitions), set(nodes))
    node_to_index = { node: index for index, node in enumerate(nodes) }
    M = numpy.zeros((len(nodes), len(nodes)))

    # note: this assumes that powerset() iterates from smallest to largest subset
    def get_induced_befouled_nodes(ill_behaved_nodes: Nodes):
        if ill_behaved_nodes == set() or ill_behaved_nodes == set(nodes):
            return set()
        intact_nodes = get_intact_nodes(fbas, ill_behaved_nodes)
        befouled_nodes = set(nodes).difference(intact_nodes)
        return befouled_nodes.difference(ill_behaved_nodes)

    ill_behaved_to_induced_befouled: Dict[FrozenSet[Node], Set[Node]] = {}

    def is_minimal_befouling(ill_behaved_nodes: Nodes, induced_befouled_nodes: Nodes):
        for ill_behaved_node in ill_behaved_nodes:
            smaller_induced_befouled_nodes = ill_behaved_to_induced_befouled[
                frozenset(ill_behaved_nodes.difference({ill_behaved_node}))
            ]
            if smaller_induced_befouled_nodes.difference({ill_behaved_node}) >= induced_befouled_nodes:
                return False
        return True

    for ill_behaved_nodes in powerset(nodes):
        induced_befouled_nodes = get_induced_befouled_nodes(ill_behaved_nodes)
        ill_behaved_to_induced_befouled[frozenset(ill_behaved_nodes)] = induced_befouled_nodes

        if not is_minimal_befouling(ill_behaved_nodes, induced_befouled_nodes):
            continue

        ill_behaved_weight = get_ill_behaved_weight(ill_behaved_nodes)
        for ill_behaved_node in ill_behaved_nodes:
            for induced_befouled_node in induced_befouled_nodes:
                M[node_to_index[ill_behaved_node], node_to_index[induced_befouled_node]] += ill_behaved_weight
    return M

def get_minimal_befouledness_eigenvector_centralities(nodes: List[Node], definitions: Definitions, get_ill_behaved_weight: Callable[[Set[Node]], float]) -> numpy.array:
    M = get_minimal_befouledness_matrix(nodes, definitions, get_ill_behaved_weight)
    eigenvalues, eigenvectors = eig(M)
    index = numpy.argsort(numpy.real(eigenvalues))[-1]
    centralities = numpy.abs(eigenvectors[:, index])
    return centralities / numpy.max(centralities)

def get_minimal_befouledness_lgs_centralities(nodes: List[Node], definitions: Definitions, get_ill_behaved_weight: Callable[[Set[Node]], float], get_mu: Callable[[numpy.array], float]) -> numpy.array:
    M = get_minimal_befouledness_matrix(nodes, definitions, get_ill_behaved_weight)
    A = numpy.eye(len(nodes)) - get_mu(M) * M
    centralities = numpy.linalg.solve(A, numpy.ones(len(nodes)))
    return centralities / numpy.max(centralities)
