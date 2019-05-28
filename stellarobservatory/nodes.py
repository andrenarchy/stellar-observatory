"""Fetch and process nodes"""
import requests

def get_nodes_from_stellarbeat():
    """Fetch nodes from stellarport.io"""
    return requests.get('https://api.stellarbeat.io/v1/nodes').json()

def get_nodes_by_public_key(nodes):
    """Get nodes by public key as a dictionary"""
    return {node['publicKey']: node for node in nodes}

def convert_public_keys_to_names(nodes_by_public_key, public_keys):
    """Convert a set/list of node public keys to a set of names"""
    return set([nodes_by_public_key[public_key]['name'] for public_key in public_keys])

def get_node_dependencies(nodes_by_public_key, public_key, dependencies=None):
    """Get public keys of all nodes a node depends on (also transitively)"""
    if dependencies is None:
        dependencies = set([public_key])

    def traverse_quorum_set_definition(quorum_set_definition):
        """Traverses a qset definition and adds them to the dependencies"""
        for validator in quorum_set_definition['validators']:
            if validator not in dependencies:
                dependencies.add(validator)
                get_node_dependencies(nodes_by_public_key, validator, dependencies)
        for inner_quorum_set_definition in quorum_set_definition['innerQuorumSets']:
            traverse_quorum_set_definition(inner_quorum_set_definition)

    traverse_quorum_set_definition(nodes_by_public_key[public_key]['quorumSet'])
    return dependencies
