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
