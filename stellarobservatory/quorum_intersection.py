"""Torstens's quorum intersection checker (a Lachowski variant)"""
from typing import Callable, Set, Type, Tuple

from stellarobservatory.quorums import greatest_quorum


def quorum_intersection(fbas: Tuple[Callable[[Set[Type], Type, Set[Type]], bool], Set[Type]],
                        without_d: set):
    """Takes an FBAS with set of nodes V and returns True iff F has quorum intersection.
    It prints two disjoint quorums otherwise."""
    is_slice_contained, all_nodes = fbas
    len_all_nodes = len(all_nodes)
    for quorum in traverse_min_quorums(is_slice_contained, set(), all_nodes, len_all_nodes):
        greatest_q = greatest_quorum(is_slice_contained,
                                     all_nodes.difference(quorum), set(), without_d)
        if greatest_q != set():
            return False, quorum, greatest_q
    return True


def contains_proper_sub_quorum(is_slice_contained: Callable[[Set[Type], Type], bool],
                               subset_nodes: set):
    """Takes an FBAS with set of nodes V; and a subset U of V and
    returns whether there is a quorum Q not fully contained U"""
    for node in subset_nodes:
        if greatest_quorum(is_slice_contained,
                           subset_nodes.difference({node}), set(), set()) != set():
            return True
    return False


def traverse_min_quorums(is_slice_contained: Callable[[Set[Type], Type], bool],
                         committed: set,  # U
                         remaining: set,  # R
                         len_all_nodes: int):  # |V|
    """Enumerate all min quorums Q with U ⊆ Q ⊆ U∪R and |Q|≤|V|/2"""
    if len(committed) > len_all_nodes / 2:  # if |U|>|V|/2 return
        return
    greatest_q = greatest_quorum(is_slice_contained, committed, set(), set())
    if greatest_q != set():
        if committed == greatest_q and not contains_proper_sub_quorum(is_slice_contained,
                                                                      committed):
            yield committed
    else:
        perimeter = committed.union(remaining)
        if remaining != set() and committed.issubset(greatest_quorum(is_slice_contained,
                                                                     perimeter,
                                                                     remaining,
                                                                     set())):
            # v ← pick from R:
            # (note pylint complains:
            # Do not raise StopIteration in generator, use return statement instead
            # but this can't happen as current != set())
            # pylint: disable=R1708
            node = next(iter(remaining))
            remaining_without_v = remaining.difference({node})
            yield from traverse_min_quorums(is_slice_contained,
                                            committed,
                                            remaining_without_v,
                                            len_all_nodes)
            yield from traverse_min_quorums(is_slice_contained,
                                            committed.union({node}),
                                            remaining_without_v,
                                            len_all_nodes)


def is_quorum(is_slice_contained: Callable[[Set[Type], Type], bool], nodes_subset: set):
    """
    Check whether nodes_subset is a quorum in FBAS F (implicitly is_slice_contained method).
    """
    return all([
        is_slice_contained(nodes_subset, v)
        for v in nodes_subset
    ])
