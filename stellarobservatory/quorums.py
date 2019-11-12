"""Torstens's quorum enumeration"""


from typing import Callable
from typing import AbstractSet
from typing import Type

# Allow for defining an FBAS as a function: (set<T>, T) -> bool.
# This function returns True, iff the FBAS has a slice for the given node T in the given
# set.
FBAS = Callable[[AbstractSet[Type], Type], bool]

def enumerate_quorums(fbas: FBAS, all_nodes):
    """Enumerate all quorums of FBAS F (given by the FBAS function(set<T>, T) -> bool)."""
    return traverse_quorums(fbas, set(), all_nodes)


def traverse_quorums(fbas, committed, remaining):
    """Given a FBAS F (by fbas_info) with set of nodes V
    and given the sets: committed ⊆ V; R ⊆ V\\committed,
    enumerate all quorums Q of F with committed ⊆ Q ⊆ committed ∪ remaining"""
    perimeter = committed.union(remaining)
    greatest_q = greatest_quorum(fbas, perimeter)
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
        yield from traverse_quorums(fbas,
                                    greatest_q.difference(current),
                                    current.difference({node}))
        current = current.difference({node})


def greatest_quorum(fbas, nodes):
    """
    Return greatest quorum contained in nodes or empty set (if there is no such quorum).
    """
    while True:
        next_u = set()
        for node in nodes:
            if fbas(nodes, node):
                next_u.add(node)
        if len(nodes) == len(next_u):
            return next_u
        nodes = next_u
