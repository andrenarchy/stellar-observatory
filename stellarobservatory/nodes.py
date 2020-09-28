"""Nodes"""

def convert_public_keys_to_names(nodes_by_public_key, public_keys):
    """Convert a set/list of node public keys to a set of names"""
    return {
        nodes_by_public_key[public_key]['name'] if 'name' in nodes_by_public_key[public_key] \
        else public_key \
        for public_key in public_keys
    }
