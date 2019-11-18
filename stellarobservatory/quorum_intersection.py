import logging
from typing import Callable, Set, Type, Tuple

from stellarobservatory.quorums import greatest_quorum

def quorum_intersection(fbas: Tuple[Callable[[Set[Type], Type], bool], Set[Type]]):
    (is_slice_contained, all_nodes) = fbas
    for quorum in traverse_min_quorums(is_slice_contained, set(), all_nodes):
        greatest_q = greatest_quorum(is_slice_contained, all_nodes.difference(quorum), set())
        if greatest_q != set():
            logging.info("Found two disjoint quorums: %s, %s", quorum, greatest_q)
            return False
    return True

def contains_proper_sub_quorum(is_slice_contained: Callable[[Set[Type], Type], bool],
                               subset_nodes: set):
    """Takes an FBAS with set of nodes V; and a subset U of V and
    returns whether there is a quorum Q not fully contained U"""
    for node in subset_nodes:
        if greatest_quorum(is_slice_contained, subset_nodes.difference({node}), set()) != set():
            return True
    return False


def traverse_min_quorums(is_slice_contained: Callable[[Set[Type], Type], bool],
                         committed: set,   # U
                         remaining: set):  # R
    """Enumerate all min quorums Q with U ⊆ Q ⊆ U∪R and |Q|≤|V|/2"""
    if len(committed) > len(remaining)/2:
        return
    # TODO figure out if set() is the best "lower bound" here for greatest_quorum
    greatest_q = greatest_quorum(is_slice_contained, committed, set())
    if greatest_q != set():
        if committed == greatest_q and not contains_proper_sub_quorum(is_slice_contained,
                                                                      committed):
            yield committed
    else:
        perimeter = committed.union(remaining)
        # TODO figure out if set() is the best "lower bound" here for greatest_quorum
        if remaining != set() and committed.issubset(greatest_quorum(is_slice_contained,
                                                                         perimeter,
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
                                            remaining_without_v)
            yield from traverse_min_quorums(is_slice_contained,
                                            committed.union({node}),
                                            remaining_without_v)
