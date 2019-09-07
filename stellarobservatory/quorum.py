"""Quorum slices and quorums"""
from itertools import chain, combinations, product

def remove_from_qset_definition(qset_definition, node):
    """Return quorum set definition with the given node removed and the threshold reduced by 1"""
    threshold = qset_definition['threshold']
    validators = qset_definition['validators']
    if node in validators:
        validators = validators.copy()
        validators.remove(node)
        threshold -= 1
    inner_quorum_sets = [
        remove_from_qset_definition(inner_qset_definition, node)
        for inner_qset_definition in qset_definition['innerQuorumSets']
        ]
    return {
        'threshold': threshold,
        'validators': validators,
        'innerQuorumSets': inner_quorum_sets
    }

def get_normalized_qset_definition(node):
    """Returns the node's quorum set definition as Stellar Core preprocesses it

    The node is required on root level and removed from rest of quorum set"""
    public_key = node['publicKey']
    return {
        'threshold': 2,
        'validators': [public_key],
        'innerQuorumSets': [remove_from_qset_definition(node['quorumSet'], public_key)]
    }

def generate_quorum_slices(quorum_set_definition, mode='economic'):
    """Generate all quorum slices for a quorum set definition

    'economic' mode only returns quorum slices of size equal to the threshold,
    use 'full' to obtain all quorum slices"""
    threshold = quorum_set_definition['threshold']
    validators = quorum_set_definition['validators']
    inner_quorum_set_definitions = quorum_set_definition['innerQuorumSets']
    max_size = threshold \
        if mode == 'economic' \
        else len(validators) + len(inner_quorum_set_definitions)

    quorum_slice_pools = [[[validator]] for validator in validators] + \
        [generate_quorum_slices(inner_quorum_set_definition, mode)
         for inner_quorum_set_definition in inner_quorum_set_definitions]

    quorum_slice_combinations = list(chain(*[
        combinations(quorum_slice_pools, size)
        for size in range(threshold, max_size + 1)
        ]))

    quorum_slice_products = list(chain(*[
        product(*quorum_slice_combination)
        for quorum_slice_combination in quorum_slice_combinations
        ]))

    return [frozenset(chain(*quorum_slice_product))
            for quorum_slice_product in quorum_slice_products]

def is_quorum(quorum_slices_by_public_key, quorum_candidate):
    """Given quorum slices , determine whether a quorum candidate is a quorum"""
    return all([
        any(quorum_slice.issubset(quorum_candidate)
            for quorum_slice in quorum_slices_by_public_key[public_key])
        for public_key in quorum_candidate
    ])

def quorum_intersection(quorums):
    """Returns whether the quorums have intersection, which intersect, and which do not"""
    intersecting_quorums = []
    split_quorums = []
    for (quorum_a, quorum_b) in combinations(quorums, 2):
        intersection = quorum_a.intersection(quorum_b)
        if intersection:
            intersecting_quorums.append((quorum_a, quorum_b, intersection))
        else:
            split_quorums.append((quorum_a, quorum_b))
    return len(split_quorums) == 0, intersecting_quorums, split_quorums

def get_minimal_quorum_intersection(quorums):
    """Returns a minimal quorum intersection (or None)"""
    minimal_intersection = None
    for (quorum_a, quorum_b) in combinations(quorums, 2):
        intersection = quorum_a.intersection(quorum_b)
        if not intersection:
            return None, quorum_a, quorum_b
        if minimal_intersection is None or len(intersection) < len(minimal_intersection[0]): #pylint: disable=unsubscriptable-object
            minimal_intersection = intersection, quorum_a, quorum_b
    return minimal_intersection

def has_quorum_intersection(nodes, slices): #pylint: disable=unused-argument
    """
    Checks if the given FBAS enjoys quorum intersection. This implementation
    is a python port of what was integrated into stellar-core via
    https://github.com/stellar/stellar-core/pull/2127

    The algorithm was presented by Łukasz Lachowski <l.lachowski@gmail.com> in
    https://arxiv.org/pdf/1902.06493.pdf
    and https://github.com/fixxxedpoint/quorum_intersection.git

    :param nodes: The nodes of the FBAS.
    :param slices: The quorum slices belonging to each node
    (len(nodes) == len(slices) needs to be true otherwise
    an exception will be raised=.
    :return: True if the given FBAS enjoys quorum intersection
    and False if there are any two disjoint quorums.
    """
    # TODO: #pylint: disable=fixme
    #  - re-enable some linters
    #  - write all sorts of tests (for everything below)
    #  - implement "fix-point quorum checker":
    #     - copy & paste: for each node Nᵢ ∈ S, remove Nᵢ from S if S
    #       does not satisfy QSᵢ, and keep iterating this procedure until it reaches a
    #       fixpoint. The fixpoint will either be empty (in which case S contained no
    #       quorum) or the largest quorum contained within S.
    #  - compute all SCCs
    #     - check if any SCC which is not the largest has any quorums,
    #       then we are done -> no intersection
    #  - iterate over all nodes which are in the largest SCC only
    #    (instead of the powerset of all the nodes) and use this as a search space for disjoint
    #    quorums
    #


def contract_to_maximal_quorum(nodes, slices_by_node):
    """
    Find greatest fixpoint of f(X) = {n ∈ X | containsQuorumSliceForNode(X, n)}.
    A simple (and non-optimized) implementation of:
    https://github.com/stellar/stellar-core/blob/27576172e99d89cbacfe6571f807a5e85746f618/src/herder/QuorumIntersectionCheckerImpl.cpp#L459-L460

    :param nodes: The nodes to contract to a maximal quorum.
    :param slices_by_node: The quorum slices of the FBAS as a
    dictionary (nodes as key, slices as value).
    :return: Either a set that represents the maximal quorum contained within
    the given set of nodes or an empty set if it didn't contain any quorums.
    In both cases this is the fixpoint of
    f(X) = {n ∈ X | containsQuorumSliceForNode(X, n)}.
    """

    while True:
        filtered = set()
        for node in nodes:
            if contains_quorum_slice(nodes, slices_by_node[node]):
                filtered.add(node)
        if filtered in (nodes, {}):
            return filtered
        nodes = filtered


def contains_quorum_slice(nodes_subset, slices):
    """Check if for the given nodes and slices there is a quorum"""
    return any(quorum_slice.issubset(nodes_subset) for quorum_slice in slices)
