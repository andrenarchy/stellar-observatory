"""Fetch and process nodes"""
import requests

def get_nodes_from_stellarbeat():
    """Fetch nodes from stellarbeat.io"""
    return requests.get('https://api.stellarbeat.io/v1/nodes').json()

def get_nodes_by_public_key(nodes):
    """Get nodes by public key as a dictionary"""
    return {node['publicKey']: node for node in nodes}

def convert_public_keys_to_names(nodes_by_public_key, public_keys):
    """Convert a set/list of node public keys to a set of names"""
    return {
        nodes_by_public_key[public_key]['name'] if 'name' in nodes_by_public_key[public_key] \
        else public_key \
        for public_key in public_keys
    }

def get_node_dependencies(nodes_by_public_key, public_key, dependencies=None, transitive=True):
    """Get public keys of all nodes a node depends on (also transitively)"""
    if dependencies is None:
        dependencies = set([public_key])

    def traverse_quorum_set_definition(quorum_set_definition):
        """Traverses a qset definition and adds them to the dependencies"""
        for validator in quorum_set_definition['validators']:
            if validator not in dependencies:
                dependencies.add(validator)
                if transitive:
                    get_node_dependencies(nodes_by_public_key, validator, dependencies)
        for inner_quorum_set_definition in quorum_set_definition['innerQuorumSets']:
            traverse_quorum_set_definition(inner_quorum_set_definition)

    traverse_quorum_set_definition(nodes_by_public_key[public_key]['quorumSet'])
    return dependencies

def get_trust_graph(nodes_by_public_key):
    """Map each node's public key to its trust graph (the set of nodes it references in its quorum slices). The node itself is excluded."""
    graph={}
    for key in nodes_by_public_key:
        nodes_intrans = get_node_dependencies(nodes_by_public_key, key, dependencies=set(), transitive=False)
        graph[key] = set(nodes_intrans)
        graph[key].discard(key)
    return graph
