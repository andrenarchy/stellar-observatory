"""Fetch and process nodes"""
import requests

from stellarobservatory.quorum_slice_definition import get_normalized_definition

def get_nodes_from_stellarbeat():
    """Fetch nodes from stellarbeat.io"""
    return requests.get('https://api.stellarbeat.io/v1/nodes').json()

def get_definition_from_stellarbeat_quorum_set(quorum_set):
    """Turn a stellarbeat quorum set into a quorum slice definition"""
    return {
        'threshold': quorum_set['threshold'],
        'nodes': set(quorum_set['validators']) if 'validators' in quorum_set else set(),
        'children_definitions': [
            get_definition_from_stellarbeat_quorum_set(inner_quorum_set)
            for inner_quorum_set in quorum_set['innerQuorumSets']
        ] if 'innerQuorumSets' in quorum_set else set()
    }

def get_nodes_by_public_key(stellarbeat_nodes):
    """Get nodes by public key as a dictionary"""
    return {node['publicKey']: node for node in stellarbeat_nodes}

def convert_stellarbeat_to_observatory(stellarbeat_nodes):
    """Get nodes, definitions by node, node names from stellarbeat nodes"""
    stellarbeat_nodes_by_public_key = get_nodes_by_public_key(stellarbeat_nodes)
    nodes = stellarbeat_nodes_by_public_key.keys()
    definitions_by_node = {
        key: get_normalized_definition(
            get_definition_from_stellarbeat_quorum_set(node['quorumSet']),
            key
            )
        for key, node in stellarbeat_nodes_by_public_key.items()
        }
    node_names = {
        key: (node['name'] if 'name' in node else key)
        for key, node in stellarbeat_nodes_by_public_key.items()
        }
    return nodes, definitions_by_node, node_names
