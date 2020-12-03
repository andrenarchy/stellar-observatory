"""Algorithm for determining B-intact nodes given a set B of nodes."""
from typing import Tuple, Callable, cast

from stellarobservatory.quorum_intersection import quorum_intersection
from stellarobservatory.quorums import greatest_quorum
from .utils.graph import Node, Nodes

def get_intact_nodes(fbas: Tuple[Callable[[Nodes, Node], bool], Nodes],
                     b_nodes: Nodes):
    """
    Takes an FBAS F (having quorum intersection) with set of nodes V and B ⊆ V and
    returns the set of all B-intact nodes.
    """
    is_slice_contained, all_nodes = fbas
    current = all_nodes.difference(b_nodes)
    while True:
        greatest_q = greatest_quorum(is_slice_contained, current, cast(Nodes, set()))

        # define F^{V\Q}
        deleted_nodes = all_nodes.difference(greatest_q)
        def cur_is_slice_contained(candidate, node):
            if node in deleted_nodes:
                raise ValueError('node not defined in FBAS')
            return is_slice_contained(candidate.union(deleted_nodes), node)
        cur_fbas = (cur_is_slice_contained, greatest_q)

        # determine whether F^{V\Q} has quorum intersection:
        result = quorum_intersection(cur_fbas)

        if result is True:
            return greatest_q

        _, quorum1, quorum2 = result
        current_w1 = greatest_quorum(is_slice_contained, greatest_q.difference(quorum1),
                                     set())
        current_w2 = greatest_quorum(is_slice_contained, greatest_q.difference(quorum2),
                                     set())

        if current_w1 == set():
            current = current_w2
        elif current_w2 == set():
            current = current_w1
        else:
            current = current_w1.intersection(current_w2)
