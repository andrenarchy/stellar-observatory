"""Dsets"""
from typing import Callable, Generator, Tuple, Set, Type, cast
from .utils.graph import Node, Nodes
from .quorums import enumerate_quorums
from .quorum_intersection import quorum_intersection

def enumerate_dsets(fbas: Tuple[Callable[[Nodes, Node], bool], Nodes]):
    """Enumerate all dsets of FBAS F (given by the pair (function(set<T>, T) -> bool, set))."""
    (is_slice_contained, all_nodes) = fbas
    yield all_nodes
    for quorum in enumerate_quorums(fbas):
        dset_candidate = all_nodes.difference(quorum)

        # define F^{V\D}
        def cur_is_slice_contained(candidate, node):
            if node in dset_candidate:
                raise ValueError('node not defined in FBAS')
            return is_slice_contained(candidate.union(dset_candidate), node)
        cur_fbas = (cur_is_slice_contained, quorum)

        # determine whether F^{V\Q} has quorum intersection:
        result = quorum_intersection(cur_fbas)

        if result is True:
            yield dset_candidate
