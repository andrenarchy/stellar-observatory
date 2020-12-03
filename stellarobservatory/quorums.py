"""Torstens's quorum enumeration"""

from typing import Callable, Generator, Tuple, Set, cast
from .utils.graph import Node, Nodes

# Allow for defining an FBAS as a function: (set<T>, T, set<T>) -> bool.
# This function returns True, iff the FBAS has a slice for the given node T in the given
# set.
def enumerate_quorums(fbas: Tuple[Callable[[Nodes, Node], bool], Nodes]):
    """Enumerate all quorums of FBAS F (given by the pair (function(set<T>, T) -> bool, set))."""
    (is_slice_contained, all_nodes) = fbas
    return traverse_quorums(is_slice_contained, set(), all_nodes)


def traverse_quorums(is_slice_contained: Callable[[Nodes, Node], bool],
                     committed: Nodes,
                     remaining: Nodes) -> Generator[Nodes, None, None]:
    """Given a FBAS F (by is_slice_contained) with set of nodes V
    and given the sets: committed ⊆ V; R ⊆ V\\committed,
    enumerate all quorums Q of F with committed ⊆ Q ⊆ committed ∪ remaining"""
    perimeter = committed.union(remaining)
    greatest_q = greatest_quorum(is_slice_contained, perimeter, committed)
    if greatest_q == set():
        return
    yield greatest_q.copy()

    current = greatest_q.difference(committed)
    while not current == set():
        # v ← pick from W = current
        # (note pylint complains:
        # Do not raise StopIteration in generator, use return statement instead
        # but this can't happen as current != set())
        # pylint: disable=R1708
        node = next(iter(current))
        yield from traverse_quorums(is_slice_contained,
                                    greatest_q.difference(current),
                                    current.difference({node}))
        current = current.difference({node})


def greatest_quorum(is_slice_contained: Callable[[Nodes, Node], bool],
                    nodes: Nodes,
                    lower_bound: Nodes):
    """
    Return greatest quorum contained in nodes if it is a super set of lower_bound
    or empty set (if there is no such quorum).
    """
    while True:
        next_u: Nodes = set()
        for node in nodes:
            if is_slice_contained(nodes, node):
                next_u.add(node)
            else:
                if node in lower_bound:
                    return cast(Nodes, set())
        if len(nodes) == len(next_u) or len(next_u) == 0:
            return next_u
        nodes = next_u


def contains_slice(nodes_subset: Set, slices_by_node, node):
    """Check if for the given node quorum slices there is a quorum slice
    contained in the subset of nodes.
    Input: FBAS(V,S) implicitly passed in via slices; nodes_subset ⊆ V; node ∈ V, a set D ⊆ V
    Output: whether node has a quorum slice in the FBAS (without D) contained in nodes_subset"""
    return any(quorum_slice.issubset(nodes_subset)
               for quorum_slice in slices_by_node[node])
