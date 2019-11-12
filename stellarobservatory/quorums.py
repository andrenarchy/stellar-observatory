"""Torstens's quorum enumeration"""
from .quorum_lachowski import greatest_quorum, next_split_node
from .quorum_slices import get_dependencies_by_node


def enumerate_quorums(slices_by_node):
    """Enumerate all quorums of FBAS F (given by slices_by_node)."""
    deps_by_node = get_dependencies_by_node(slices_by_node)
    fbas_info = {
        'deps_by_node': deps_by_node,
        'slices_by_node': slices_by_node
    }
    all_nodes = set(slices_by_node.keys())  # all nodes need to be present as keys here
    return traverse_quorums(fbas_info, set(), all_nodes)


def traverse_quorums(fbas_info, committed, remaining):
    """Given a FBAS F (by fbas_info) with set of nodes V
    and given the sets: committed ⊆ V; R ⊆ V\\committed,
    enumerate all quorums Q of F with committed ⊆ Q ⊆ committed ∪ remaining"""
    perimeter = committed.union(remaining)
    greatest_q = greatest_quorum(perimeter, fbas_info['slices_by_node'])
    if greatest_q == set() or not committed.issubset(greatest_q):
        return
    yield frozenset(greatest_q)

    current = greatest_q.difference(committed)
    while not current == set():
        # v ← pick from W:
        node = next_split_node(current, fbas_info['deps_by_node'])
        yield from traverse_quorums(fbas_info,
                                    greatest_q.difference(current),
                                    current.difference({node}))
        current = current.difference({node})
