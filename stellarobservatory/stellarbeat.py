"""Fetch and process nodes"""
from typing import Any, Dict, List, Optional, Set, TypedDict, cast
import requests

from .utils.graph import Nodes
from .quorum_slice_definition import get_normalized_definition, Definition, Definitions

def get_nodes_from_stellarbeat():
    """Fetch nodes from stellarbeat.io"""
    return requests.get('https://api.stellarbeat.io/v1/nodes').json()

QuorumSet = TypedDict('QuorumSet', {
    'threshold': int,
    'validators': List[str],
    # NOTE: use List['QuorumSet] when  https://github.com/python/mypy/issues/731 is fixed
    'innerQuorumSets': Any
})

def get_definition_from_stellarbeat_quorum_set(quorum_set: QuorumSet) -> Definition:
    """Turn a stellarbeat quorum set into a quorum slice definition"""
    return {
        'threshold': quorum_set['threshold'],
        'nodes': set(quorum_set['validators']) if 'validators' in quorum_set else set(),
        'children_definitions': [
            get_definition_from_stellarbeat_quorum_set(inner_quorum_set)
            for inner_quorum_set in quorum_set['innerQuorumSets']
        ] if 'innerQuorumSets' in quorum_set else set()
    }

StellarbeatNode = TypedDict('StellarbeatNode', {
    # https://github.com/PyCQA/pylint/issues/3882
    # pylint: disable=unsubscriptable-object
    'publicKey': str,
    'quorumSet': QuorumSet,
    'name': Optional[str]
})
def get_nodes_by_public_key(stellarbeat_nodes: List[StellarbeatNode]) -> Dict[str, StellarbeatNode]:
    """Get nodes by public key as a dictionary"""
    return {node['publicKey']: node for node in stellarbeat_nodes}

def convert_stellarbeat_to_observatory(stellarbeat_nodes: List[StellarbeatNode]):
    """Get nodes, definitions by node, node names from stellarbeat nodes"""
    stellarbeat_nodes_by_public_key = get_nodes_by_public_key(stellarbeat_nodes)
    nodes: Nodes = set(stellarbeat_nodes_by_public_key.keys())
    definitions_by_node: Definitions = {
        key: get_normalized_definition(
            get_definition_from_stellarbeat_quorum_set(node['quorumSet']),
            key
            )
        for key, node in stellarbeat_nodes_by_public_key.items()
        }
    node_names: Dict[str, str] = {
        key: cast(str, node['name'] if 'name' in node else key)
        for key, node in stellarbeat_nodes_by_public_key.items()
        }
    return nodes, definitions_by_node, node_names

def convert_public_keys_to_names(nodes_by_public_key: Dict[str, StellarbeatNode],
                                 public_keys: Set[str]):
    """Convert a set of node public keys to a set of names"""
    return {
        nodes_by_public_key[public_key]['name'] if 'name' in nodes_by_public_key[public_key] \
        else public_key \
        for public_key in public_keys
    }
