import requests

def get_nodes_from_stellarbeat():
    return requests.get("https://api.stellarbeat.io/v1/nodes").json()
