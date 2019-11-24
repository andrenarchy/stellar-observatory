"""Quorum slices and quorums"""

from itertools import combinations

def quorum_intersection(quorums):
    """Returns whether the quorums have intersection, which intersect, and which do not"""
    intersecting_quorums = []
    split_quorums = []
    for (quorum_a, quorum_b) in combinations(quorums, 2):
        intersection = quorum_a.intersection(quorum_b)
        if intersection:
            intersecting_quorums.append((quorum_a, quorum_b, intersection))
        else:
            split_quorums.append((quorum_a, quorum_b))
    return len(split_quorums) == 0, intersecting_quorums, split_quorums

def get_minimal_quorum_intersection(quorums):
    """Returns a minimal quorum intersection (or None)"""
    minimal_intersection = None
    for (quorum_a, quorum_b) in combinations(quorums, 2):
        intersection = quorum_a.intersection(quorum_b)
        if not intersection:
            return None, quorum_a, quorum_b
        if minimal_intersection is None or len(intersection) < len(minimal_intersection[0]): #pylint: disable=unsubscriptable-object
            minimal_intersection = intersection, quorum_a, quorum_b
    return minimal_intersection
