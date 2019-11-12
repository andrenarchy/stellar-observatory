"""Torstens's quorum enumeration"""

from typing import Callable
from typing import AbstractSet
from typing import Type

# Allow for defining an FBAS as a function: (set<T>, T) -> bool.
# This function returns True, iff the FBAS has a slice for the given node T in the given
# set.
IsSliceContained = Callable[[AbstractSet[Type], Type], bool]
FBAS = (IsSliceContained, AbstractSet[Type])


def enumerate_quorums(fbas: FBAS):
    """Enumerate all quorums of FBAS F (given by the pair (function(set<T>, T) -> bool, set))."""
    (is_slice_contained, all_nodes) = fbas
    return traverse_quorums(is_slice_contained, set(), all_nodes)


def traverse_quorums(is_slice_contained: IsSliceContained, committed: set, remaining: set):
    """Given a FBAS F (by is_slice_contained) with set of nodes V
    and given the sets: committed ⊆ V; R ⊆ V\\committed,
    enumerate all quorums Q of F with committed ⊆ Q ⊆ committed ∪ remaining"""
    perimeter = committed.union(remaining)
    greatest_q = greatest_quorum(is_slice_contained, perimeter)
    if greatest_q == set() or not committed.issubset(greatest_q):
        return
    yield frozenset(greatest_q)

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


def greatest_quorum(is_slice_contained: IsSliceContained, nodes: set):
    """
    Return greatest quorum contained in nodes or empty set (if there is no such quorum).
    """
    while True:
        next_u = set()
        for node in nodes:
            if is_slice_contained(nodes, node):
                next_u.add(node)
        if len(nodes) == len(next_u):
            return next_u
        nodes = next_u
