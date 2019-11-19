"""Torstens's quorum intersection checker (a Lachowski variant)"""
import logging
from typing import Callable, Set, Type, Tuple

from stellarobservatory.quorums import greatest_quorum


def quorum_intersection(fbas: Tuple[Callable[[Set[Type], Type], bool], Set[Type]]):
    """Takes an FBAS with set of nodes V and returns True iff F has quorum intersection.
    It prints two disjoint quorums otherwise."""
    (is_slice_contained, all_nodes) = fbas
    for quorum in traverse_min_quorums(fbas, set(), all_nodes):
        greatest_q = greatest_quorum(is_slice_contained, all_nodes.difference(quorum), set())
        if greatest_q != set():
            logging.info("Found two disjoint quorums: %s, %s", quorum, greatest_q)
            return False
    return True


def contains_proper_sub_quorum(fbas: Tuple[Callable[[Set[Type], Type], bool], Set[Type]],
                               subset_nodes: set):
    """Takes an FBAS with set of nodes V; and a subset U of V and
    returns whether there is a quorum Q not fully contained U"""
    (is_slice_contained, _) = fbas
    for node in subset_nodes:
        if greatest_quorum(is_slice_contained, subset_nodes.difference({node}), set()) != set():
            return True
    return False


def traverse_min_quorums(fbas: Tuple[Callable[[Set[Type], Type], bool], Set[Type]],
                         committed: set,  # U
                         remaining: set):  # R
    """Enumerate all min quorums Q with U ⊆ Q ⊆ U∪R and |Q|≤|V|/2"""
    # TODO shouldn't this be len(remaining) / 2 + 1? The paper says U|>|V|/2
    (is_slice_contained, all_nodes) = fbas
    if len(committed) > len(all_nodes) / 2:
        logging.debug("len(committed) > len(all_nodes) / 2: %s; with committed: %s, remaining: %s, all: %s,  len(all_nodes) / 2 =%s", len(committed) > len(all_nodes) / 2, committed, remaining, all_nodes,  len(all_nodes) / 2)
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
            yield from traverse_min_quorums(fbas,
                                            committed,
                                            remaining_without_v)
            yield from traverse_min_quorums(fbas,
                                            committed.union({node}),
                                            remaining_without_v)
