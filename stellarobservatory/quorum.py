"""Quorum slices and quorums"""

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
