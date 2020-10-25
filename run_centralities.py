from stellarobservatory.utils.scc import get_strongly_connected_components
from stellarobservatory.quorums import enumerate_quorums
import numpy
from typing import Callable, Dict, Generic, List, Set, TypeVar, TypedDict, Union
from stellarobservatory import quorum_slice_definition, stellarbeat, centralities
from stellarobservatory.quorum_slice_definition import Definitions, get_is_slice_contained, get_trust_graph
from stellarobservatory.utils.graph import Node, Nodes

def get_from_seed_node(seed_node: str):
    stellarbeat_nodes = stellarbeat.get_nodes_from_stellarbeat()
    _, definitions_by_node, node_names = stellarbeat.convert_stellarbeat_to_observatory(stellarbeat_nodes)
    dependencies = quorum_slice_definition.get_transitive_dependencies(definitions_by_node, seed_node)
    dependencies.add(seed_node)
    reduced_definitions_by_node = {key: definitions_by_node[key] for key in dependencies}
    reduced_node_names = {key: node_names[key] for key in dependencies}
    return dependencies, reduced_definitions_by_node, reduced_node_names

def print_centralities(nodes: List[Node], centralities: numpy.array, node_names: Dict[Node,str]=None):
    for node_index in range(len(nodes)):
        node = nodes[node_index]
        print('{0}: {1}'.format(node_names[node] if node_names is not None else node, centralities[node_index]))

def print_sorted_centralities(nodes: List[Node], centralities: numpy.array, node_names: Dict[Node,str]=None):
    sorted_indexes = numpy.argsort(centralities)[::-1]
    for node_index in sorted_indexes:
        node = nodes[node_index]
        print('{0}: {1}'.format(node_names[node] if node_names is not None else node, centralities[node_index]))

Analyzer = List[Callable[[List[Node], Definitions, Union[Dict[Node,str],None]],None]]

def quorum_analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
    print()
    print('quorum analyzer')
    print('------------------------')
    fbas = (get_is_slice_contained(definitions), set(nodes))
    print('Quorums:')
    for quorum in enumerate_quorums(fbas):
        print({ node_names[node] if node_names is not None else node for node in quorum })
    print()

def scc_analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
    print()
    print('scc analyzer')
    print('------------------------')
    trust_graph = get_trust_graph(definitions)
    sccs, scc_graph = get_strongly_connected_components(trust_graph)
    print('sccs:')
    for index, scc in enumerate(sccs):
        print('scc {0}: {1}'.format(index, { node_names[node] if node_names is not None else node for node in scc }))
    print()
    print('scc graph:')
    for scc, edge_targets in scc_graph.items():
        print('scc {0}: {1}'.format(scc, edge_targets))
    print()

def eigenvector_analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
    print()
    print('eigenvector analyzer')
    print('------------------------')
    print('centralities:')
    print_centralities(nodes, centralities.get_eigenvector_centralities(nodes, definitions), node_names)
    print()

def subgraph_analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
    print()
    print('subgraph analyzer')
    print('-----------------')
    print('centralities:')
    print_centralities(nodes, centralities.get_subgraph_centralities(nodes, definitions), node_names)
    print()

def quorum_eigenvector_analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
    print()
    print('quorum eigenvector analyzer')
    print('--------------------------------------')
    print('centralities:')
    print_centralities(nodes, centralities.get_quorum_eigenvector_centralities(nodes, definitions), node_names)
    print()

def quorum_subgraph_analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
    print()
    print('quorum subgraph analyzer')
    print('--------------------------------------')
    print('centralities:')
    print_centralities(nodes, centralities.get_quorum_subgraph_centralities(nodes, definitions), node_names)
    print()


def quorum_intersection_eigenvector_analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
    print()
    print('quorum intersection eigenvector analyzer')
    print('--------------------------------------')
    print('centralities:')
    print_centralities(nodes, centralities.get_quorum_intersection_eigenvector_centralities(nodes, definitions), node_names)
    print()

def quorum_intersection_subgraph_analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
    print()
    print('quorum intersection subgraph analyzer')
    print('-------------------------------------')
    print('centralities:')
    print_centralities(nodes, centralities.get_quorum_intersection_subgraph_centralities(nodes, definitions), node_names)
    print()

def befouledness_eigenvector_analyzer(get_ill_behaved_weight: Callable[[Nodes], float]):
    def analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
        print()
        print('befouledness eigenvector analyzer')
        print('---------------------------------')
        print('centralities:')
        print_centralities(nodes, centralities.get_befouledness_eigenvector_centralities(nodes, definitions, get_ill_behaved_weight), node_names)
        print()
    return analyzer

def befouledness_lgs_analyzer(get_ill_behaved_weight: Callable[[Nodes], float], get_mu: Callable[[numpy.array], float]):
    def analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
        print()
        print('befouledness lgs analyzer')
        print('-------------------------')
        print('centralities:')
        print_centralities(nodes, centralities.get_befouledness_lgs_centralities(nodes, definitions, get_ill_behaved_weight, get_mu), node_names)
        print()
    return analyzer

def hierarchical_befouledness_eigenvector_analyzer(get_ill_behaved_weight: Callable[[Nodes], float]):
    def analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
        print()
        print('hierarchical befouledness eigenvector analyzer')
        print('----------------------------------------------')
        print('centralities:')
        print_centralities(nodes, centralities.get_hierarchical_befouledness_eigenvector_centralities(nodes, definitions, get_ill_behaved_weight), node_names)
        print()
    return analyzer

def hierarchical_befouledness_lgs_analyzer(get_ill_behaved_weight: Callable[[Nodes], float], get_mu: Callable[[numpy.array], float]):
    def analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
        print()
        print('hierarchical befouledness lgs analyzer')
        print('--------------------------------------')
        print('centralities:')
        print_centralities(nodes, centralities.get_hierarchical_befouledness_lgs_centralities(nodes, definitions, get_ill_behaved_weight, get_mu), node_names)
        print()
    return analyzer

def minimal_befouledness_eigenvector_analyzer(get_ill_behaved_weight: Callable[[Nodes], float]):
    def analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
        print()
        print('minimal befouledness eigenvector analyzer')
        print('-----------------------------------------')
        print('centralities:')
        print_centralities(nodes, centralities.get_minimal_befouledness_eigenvector_centralities(nodes, definitions, get_ill_behaved_weight), node_names)
        print()
    return analyzer

def minimal_befouledness_lgs_analyzer(get_ill_behaved_weight: Callable[[Nodes], float], get_mu: Callable[[numpy.array], float]):
    def analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
        print()
        print('minimal befouledness lgs analyzer')
        print('---------------------------------')
        print('centralities:')
        print_centralities(nodes, centralities.get_minimal_befouledness_lgs_centralities(nodes, definitions, get_ill_behaved_weight, get_mu), node_names)
        print()
    return analyzer

NodesList = List[Node]
class Example(Generic[Node], TypedDict):
    name: str
    nodes: NodesList
    node_names: Union[Dict[Node, str], None]
    quorum_slice_definitions: Definitions
    analyzers: Analyzer

satoshipay_de_fra = 'GC5SXLNAM3C4NMGK2PXK4R34B5GNZ47FYQ24ZIBFDFOCU6D4KBN4POAE'
stellar_network = get_from_seed_node(satoshipay_de_fra)

def slices_to_definitions(slices_by_node: Dict[Node, List[Nodes]]):
    return {
        node: quorum_slice_definition.quorum_slices_to_definition(quorum_slices)
        for node, quorum_slices in slices_by_node.items()
    }

examples: List[Example] = [
    {
      'name': 'ex:1scc',
      'nodes': list(range(1,6)),
      'node_names': None,
      'quorum_slice_definitions': slices_to_definitions({
            1: [{1,2}, {1,3}, {1,4}, {1,5}],
            2: [{1,2}, {2,3}],
            3: [{1,3}],
            4: [{1,4}],
            5: [{1,5}]
      }),
      'analyzers': [
            scc_analyzer,
            quorum_analyzer,
            eigenvector_analyzer,
            subgraph_analyzer,
            quorum_eigenvector_analyzer,
            quorum_subgraph_analyzer,
            befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
            hierarchical_befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
      ]
    },
    {
      'name': '3 SCCs, quorum intersection',
      'nodes': list(range(1,8)),
      'node_names': None,
      'quorum_slice_definitions': slices_to_definitions({
            1: [{1,2,3,7}],
            2: [{1,2,3,7}],
            3: [{1,2,3,7}],
            4: [{4,5,6,7}],
            5: [{4,5,6,7}],
            6: [{4,5,6,7}],
            7: [{7}]
      }),
      'analyzers': [
            scc_analyzer,
            quorum_analyzer,
            subgraph_analyzer,
            quorum_eigenvector_analyzer,
            quorum_subgraph_analyzer,
            befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
            hierarchical_befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
      ]
    },
    {
      'name': '4 SCCs, 2 maximal SCCs',
      'nodes': list(range(1,9)),
      'node_names': None,
      'quorum_slice_definitions': slices_to_definitions({
            1: [{1,2,3,7}],
            2: [{1,2,3,7}],
            3: [{1,2,3,7}],
            4: [{4,5,6,7}],
            5: [{4,5,6,7}],
            6: [{4,5,6,7,8}],
            7: [{7}],
            8: [{8}]
      }),
      'analyzers': [
            scc_analyzer,
            quorum_analyzer,
            subgraph_analyzer,
            quorum_eigenvector_analyzer,
            quorum_subgraph_analyzer,
            befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
            hierarchical_befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
      ]
    },
    {
      'name': 'Stellar Network',
      'nodes': list(stellar_network[0]),
      'node_names': stellar_network[2],
      'quorum_slice_definitions': stellar_network[1],
      'analyzers': [eigenvector_analyzer, subgraph_analyzer]
    },
    {
        'name': 'Example X: two SCCs',
        'nodes': [1, 2, 3, 4],
        'node_names': None,
        'quorum_slice_definitions': slices_to_definitions({
            1: [{1,2}],
            2: [{1,2}],
            3: [{1,3,4}],
            4: [{1,3,4}]
        }),
        'analyzers': [
            scc_analyzer,
            quorum_analyzer,
            subgraph_analyzer,
            quorum_eigenvector_analyzer,
            quorum_subgraph_analyzer,
            befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
            hierarchical_befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
        ]
    },
    {
        'name': 'Example X: two SCCs v2',
        'nodes': [1, 2, 3, 4],
        'node_names': None,
        'quorum_slice_definitions': slices_to_definitions({
            1: [{1,2}],
            2: [{1,2}],
            3: [{1,3},{3,4}],
            4: [{1,3,4}]
        }),
        'analyzers': [
            scc_analyzer,
            quorum_analyzer,
            subgraph_analyzer,
            quorum_eigenvector_analyzer,
            quorum_subgraph_analyzer,
            befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
            hierarchical_befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
        ]
    },
    {
        'name': 'Example X: three SCCs',
        'nodes': [1, 2, 3, 4, 5],
        'node_names': None,
        'quorum_slice_definitions': slices_to_definitions({
            1: [{1,2}],
            2: [{1,2}],
            3: [{1,3,4}],
            4: [{1,3,4}],
            5: [{3,5}]
        }),
        'analyzers': [
            scc_analyzer,
            quorum_analyzer,
            subgraph_analyzer,
            quorum_eigenvector_analyzer,
            quorum_subgraph_analyzer,
            befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
            hierarchical_befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
        ]
    },
    {
        'name': 'Example X: 2 complex SCCs',
        'nodes': [1, 2, 3, 4, 5, 6],
        'node_names': None,
        'quorum_slice_definitions': {
            1: {
                'nodes': {1, 2},
                'threshold': 2,
                'children_definitions': [{
                    'nodes': {3, 4, 5},
                    'threshold': 2,
                    'children_definitions': []
                }]
            },
            2: {
                'nodes': {1, 2, 3},
                'threshold': 2,
                'children_definitions': []
            },
            3: {
                'nodes': {1, 2},
                'threshold': 2,
                'children_definitions': [{
                    'nodes': {3, 4, 5},
                    'threshold': 2,
                    'children_definitions': []
                }]
            },
            4: {
                'nodes': {1, 2},
                'threshold': 2,
                'children_definitions': [{
                    'nodes': {3, 4, 5},
                    'threshold': 2,
                    'children_definitions': []
                }]
            },
            5: {
                'nodes': {1, 2},
                'threshold': 2,
                'children_definitions': [{
                    'nodes': {3, 4, 5},
                    'threshold': 2,
                    'children_definitions': []
                }]
            },
            6: {
                'nodes': {3, 4, 6},
                'threshold': 2,
                'children_definitions': []
            },
        },
        'analyzers': [
            scc_analyzer,
            quorum_analyzer,
            subgraph_analyzer,
            quorum_eigenvector_analyzer,
            quorum_subgraph_analyzer,
            befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
            hierarchical_befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
            minimal_befouledness_lgs_analyzer(lambda ill_behaved_nodes: 1/2**len(ill_behaved_nodes), lambda M: 0.5 / numpy.linalg.norm(M, 2)),
        ]
    }
]

for example in examples:
    print()
    print('Running {0}'.format(example['name']))
    for analyzer in example['analyzers']:
        analyzer(example['nodes'], example['quorum_slice_definitions'], example['node_names'])

