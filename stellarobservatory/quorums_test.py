"""Test for Torstens's quorum enumeration"""
from .quorums import enumerate_quorums, contains_slice


def test_enumerate_quorums():
    """Test enumerate_quorums() with simple example"""
    slices_by_node = {
        1: [{1, 2, 3, 7}],
        2: [{1, 2, 3, 7}],
        3: [{1, 2, 3, 7}],
        4: [{4, 5, 6, 7}],
        5: [{4, 5, 6, 7}],
        6: [{4, 5, 6, 7}],
        7: [{7}],
    }

    def ex28_fbas(nodes_subset, node) -> bool:
        return contains_slice(nodes_subset, slices_by_node, node, set())

    quorums = list(enumerate_quorums((ex28_fbas, {1, 2, 3, 4, 5, 6, 7})))
    assert set(quorums) == {frozenset({7}),
                            frozenset({4, 5, 6, 7}),
                            frozenset({1, 2, 3, 7}),
                            frozenset({1, 2, 3, 4, 5, 6, 7})
                            }


def test_enumerate_quorums_stellar_core():
    """Test enumerate_quorums() with stellar core style fbas"""
    # init test:
    stellar_core_orgs = [
        {'name': "B", 'nodes': ["1", "2", "3"], 'limit': 2},
        {'name': "A", 'nodes': ["1", "2", "3"], 'limit': 2},
        {'name': "C", 'nodes': ["1", "2", "3"], 'limit': 2},
        {'name': "D", 'nodes': ["1", "2", "3"], 'limit': 2},
        {'name': "E", 'nodes': ["1", "2", "3"], 'limit': 2},
        {'name': "F", 'nodes': ["1", "2", "3", "4", "5"], 'limit': 3}
    ]
    stellar_core_nodes = set()
    for org in stellar_core_orgs:
        name, nodes = org['name'], org['nodes']
        for node in nodes:
            stellar_core_nodes.add(name + node)

    threshold = 5

    def stellar_core(subset: set, _: str) -> bool:
        sufficient_orgs = 0
        for org in stellar_core_orgs:
            name, nodes, limit = org['name'], org['nodes'], org['limit']
            sufficient_nodes = 0
            for org_node in nodes:
                node = str(name + org_node)
                if node in subset:
                    sufficient_nodes += 1
            if sufficient_nodes >= limit:
                sufficient_orgs += 1
        return sufficient_orgs >= threshold

    quorums = list(enumerate_quorums((stellar_core, stellar_core_nodes)))
    assert len(quorums) == 114688
