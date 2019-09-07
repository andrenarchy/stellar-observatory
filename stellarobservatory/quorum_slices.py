"""Methods for quorum slices"""

from itertools import chain

def get_dependencies_by_node(quorum_slices_by_node):
    """Get the dependency graph from quorum slices"""
    return {
        node: frozenset(chain(*quorum_slices)).difference([node])
        for node, quorum_slices in quorum_slices_by_node.items()
    }
