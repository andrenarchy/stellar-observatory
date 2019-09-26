"""Lachowski's quorum intersection checker"""
import logging
import operator

from .utils import graph
from .utils import scc
from .quorum_slices import get_dependencies_by_node

def has_quorum_intersection(slices_by_node):
    """Checks if the given FBAS enjoys quorum intersection.

    This implementation is a python port of what was integrated into stellar-core via
    https://github.com/stellar/stellar-core/pull/2127

    The algorithm was presented by Łukasz Lachowski <l.lachowski@gmail.com> in
    https://arxiv.org/pdf/1902.06493.pdf
    and https://github.com/fixxxedpoint/quorum_intersection.git

    Returns True if the given FBAS enjoys quorum intersection
    and False if there are any two disjoint quorums.
    """
    # compute all components
    deps_by_node = get_dependencies_by_node(slices_by_node)
    sccs = scc.get_strongly_connected_components(deps_by_node)

    # make sure only one SCC contains all minimal quorums
    non_intersection_quorums_counter = 0
    for component in sccs:
        contains_quorum = len(contract_to_maximal_quorum(component, slices_by_node)) != 0
        logging.debug("SCC: %s contains a quorum: %s", component,
                      contract_to_maximal_quorum(component, slices_by_node))
        if contains_quorum:
            non_intersection_quorums_counter += 1

    if non_intersection_quorums_counter != 1:
        logging.debug("Found more than one SCC containing quorums. No intersection.")
        return False

    max_scc = sccs[0]
    logging.debug("max scc: %s", max_scc)
    max_scc_max_quorum = contract_to_maximal_quorum(max_scc, slices_by_node)
    if not max_scc_max_quorum:
        logging.debug("No quorum found in transitive closure.")
        return False

    logging.debug("Maximal main scc: %s", max_scc_max_quorum)
    max_commit_size = (len(max_scc_max_quorum) / 2) + 1

    committed, remaining = set(), max_scc_max_quorum
    fbas_info = {
        'deps_by_node': deps_by_node,
        'max_scc': max_scc,
        'slices_by_node': slices_by_node
    }

    return all_min_quorums_intersect(committed, remaining, max_commit_size, fbas_info)

def all_min_quorums_intersect(committed, remaining, max_commit_size, fbas_info):
    """Test whether all min quorums intersect.

    Main recursion that cleverly splits checking if all quorums intersect.
    It only checks necessary recursion branches and exits early where possible.
    """
    deps_by_node, max_scc, slices_by_node = \
        fbas_info['deps_by_node'], fbas_info['max_scc'], fbas_info['slices_by_node']
    if len(committed) > max_commit_size:
        return True

    committed_quorum = contract_to_maximal_quorum(committed, slices_by_node)
    if committed_quorum != set():
        return not (is_minimal_quorum(committed_quorum, slices_by_node) and \
                has_disjoint_quorum(committed_quorum, max_scc, slices_by_node))

    if remaining == set():
        return True

    perimeter = committed.union(remaining)
    extension_quorum = contract_to_maximal_quorum(perimeter, slices_by_node)
    if extension_quorum != set():
        if not committed.issubset(extension_quorum):
            return True
    else:
        logging.debug('early exit 2.1: no extension quorum in perimeter=%s', perimeter)
        return True

    split_node = next_split_node(remaining, deps_by_node)
    logging.debug('Remaining: %s', remaining)
    logging.debug('Split node: %s', split_node)
    remaining_without_split = remaining.difference({split_node})
    return all_min_quorums_intersect(committed, remaining_without_split,
                                     max_commit_size, fbas_info) and \
        all_min_quorums_intersect(committed.union({split_node}), remaining_without_split,
                                  max_commit_size, fbas_info)

def is_quorum(nodes, slices_by_node):
    """Test whether the given nodes are a quorum"""
    return contract_to_maximal_quorum(nodes, slices_by_node) != set()

def has_disjoint_quorum(nodes, max_scc, slices_by_node):
    """Test if there is a quorum disjoint from nodes (with max scc given)"""
    return is_quorum(max_scc.difference(nodes), slices_by_node)

def is_minimal_quorum(nodes, slices_by_node):
    """Test if a contracted to maximal quorum is minimal"""
    for node in nodes:
        test_nodes = nodes.difference({node})
        if contract_to_maximal_quorum(test_nodes, slices_by_node) != set():
            return False
    return True

def contract_to_maximal_quorum(nodes, slices_by_node):
    """Contract nodes to a maximal quorum.

    Find greatest fixpoint of f(X) = {n ∈ X | containsQuorumSliceForNode(X, n)}.
    A simple (and non-optimized) implementation of:
    https://github.com/stellar/stellar-core/blob/27576172e99d89cbacfe6571f807a5e85746f618/src/herder/QuorumIntersectionCheckerImpl.cpp#L459-L460

    Returns either a maximal quorum contained within
    the given set of nodes or an empty set if it didn't contain any quorums.
    In both cases this is the fixpoint of f(X) = {n ∈ X | containsQuorumSliceForNode(X, n)}.
    """
    while True:
        filtered = set()
        for node in nodes:
            if contains_quorum_slice(nodes, slices_by_node, node):
                filtered.add(node)
        if filtered in (nodes, {}):
            return filtered
        nodes = filtered

def contains_quorum_slice(nodes_subset, slices, node):
    """Check if for the given nodes and quorum slices there is a quorum slice
    contained in the set of given nodes."""
    return any(quorum_slice.issubset(nodes_subset) for quorum_slice in slices[node])

def next_split_node(nodes_subset, deps_by_node):
    """Choose the next split node to process: uniformly at random pick a node with max in-degree"""
    induced_subgraph = graph.get_induced_subgraph(deps_by_node, nodes_subset)
    indegrees = graph.get_indegrees(induced_subgraph)
    return max(indegrees.items(), key=operator.itemgetter(1))[0]
