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
