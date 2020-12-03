"""Tests for enumerate dsets algorithm"""
from stellarobservatory.utils.graph import Node, Nodes
from typing import Dict, List, Set
import numpy
from stellarobservatory.centralities import get_eigenvector_centralities, get_hierarchical_intactness_lgs_centralities, get_intactness_lgs_centralities, get_quorum_eigenvector_centralities, get_quorum_subgraph_centralities, get_subgraph_centralities
from stellarobservatory.quorum_slice_definition import quorum_slices_to_definitions
from stellarobservatory.dsets import enumerate_dsets
from stellarobservatory.quorums import contains_slice

from numpy.testing import assert_allclose

NODES = [1, 2, 3, 4, 5]
QUORUM_SLICES = {
    1: [{1,2}, {1,3}, {1,4}, {1,5}],
    2: [{1,2}, {2,3}],
    3: [{1,3}],
    4: [{1,4}],
    5: [{1,5}]
}
DEFINITIONS = quorum_slices_to_definitions(QUORUM_SLICES)

def get_ill_behaved_weight(ill_behaved_nodes: Set[Node]) -> float:
    return 1/2**len(ill_behaved_nodes)

def get_mu(matrix: numpy.array) -> float:
    return 0.5 / numpy.linalg.norm(matrix, 2)

def test_get_eigenvector_centralities():
    """Test get_eigenvector_centralities()"""
    centralities = get_eigenvector_centralities(NODES, DEFINITIONS)
    desired_centralities = [1., 0.472834, 0.696406, 0.472834, 0.472834]
    assert_allclose(centralities, desired_centralities, rtol=1e-5)

def test_get_subgraph_centralities():
    """Test get_subgraph_centralities()"""
    centralities = get_subgraph_centralities(NODES, DEFINITIONS)
    desired_centralities = [1., 0.475507, 0.475507, 0.424363, 0.424363]
    assert_allclose(centralities, desired_centralities, rtol=1e-5)

def test_get_quorum_eigenvector_centralities():
    """Test get_quorum_eigenvector_centralities()"""
    centralities = get_quorum_eigenvector_centralities(NODES, DEFINITIONS)
    desired_centralities = [1., 0.584192, 0.584192, 0.584192, 0.584192]
    assert_allclose(centralities, desired_centralities, rtol=1e-5)

def test_get_quorum_subgraph_centralities():
    """Test get_quorum_subgraph_centralities()"""
    centralities = get_quorum_subgraph_centralities(NODES, DEFINITIONS)
    desired_centralities = [1., 0.520563, 0.520563, 0.520563, 0.520563]
    assert_allclose(centralities, desired_centralities, rtol=1e-5)

def test_get_intactness_lgs_centralities():
    """Test get_intactness_lgs_centralities()"""
    centralities = get_intactness_lgs_centralities(NODES, DEFINITIONS, get_ill_behaved_weight, get_mu)
    desired_centralities = [1., 0.606552, 0.699301, 0.647041, 0.647041]
    assert_allclose(centralities, desired_centralities, rtol=1e-5)

def test_get_hierarchical_intactness_lgs_centralities():
    """Test get_hierarchical_intactness_lgs_centralities()"""
    centralities = get_hierarchical_intactness_lgs_centralities(NODES, DEFINITIONS, get_ill_behaved_weight, get_mu)
    desired_centralities = [1., 0.606552, 0.699301, 0.647041, 0.647041]
    assert_allclose(centralities, desired_centralities, rtol=1e-5)
