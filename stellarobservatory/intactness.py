"""Algorithm for determining B-intact nodes given a set B of nodes."""
from typing import Tuple, Callable, Set, Type


def intact_nodes(fbas: Tuple[Callable[[Set[Type], Type], bool], Set[Type]], b_nodes: Set[Type]):
    """
    Takes an FBAS F (having quorum intersection) with set of nodes V and B ⊆ V and
    returns the set of all B-intact nodes.
    """
