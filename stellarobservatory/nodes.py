"""Fetch and process nodes"""
import requests

def get_nodes_from_stellarbeat():
    """Fetch nodes from stellarport.io"""
    return requests.get("https://api.stellarbeat.io/v1/nodes").json()
