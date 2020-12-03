from stellarobservatory.quorum_intersection import quorum_intersection
from stellarobservatory.dsets import enumerate_dsets
from stellarobservatory.utils.scc import get_strongly_connected_components
from stellarobservatory.quorums import enumerate_quorums
import numpy
from typing import Callable, Dict, Generic, List, Set, TypeVar, TypedDict, Union
from stellarobservatory import quorum_slice_definition, stellarbeat, centralities
from stellarobservatory.quorum_slice_definition import Definitions, get_is_slice_contained, get_normalized_definition, get_trust_graph
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
    n_quorums = 0
    for quorum in enumerate_quorums(fbas):
        n_quorums += 1
        print(sorted({ node_names[node] if node_names is not None else node for node in quorum }))
    print('({0} quorums in total)'.format(n_quorums))
    has_quorum_intersection = quorum_intersection(fbas)
    print(f'Quorum intersection: {has_quorum_intersection == True}')
    print()
    print('Dsets:')
    n_dsets = 0
    for dset in enumerate_dsets(fbas):
        n_dsets += 1
        print(sorted({ node_names[node] if node_names is not None else node for node in dset }))
    print('({0} Dsets in total)'.format(n_dsets))
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
      'name': 'ex:1scc-mod',
      'nodes': list(range(1,6)),
      'node_names': None,
      'quorum_slice_definitions': slices_to_definitions({
            1: [{1,2}, {1,3}, {1,4}, {1,5}],
            2: [{1,2, 3}],
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
      'name': 'ex:FBAS_fig7',
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
      'name': 'ex:FBAS_fig7-mod',
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
        'name': 'ex:stellar-old',
        'nodes': ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'C'],
        'node_names': None,
        'quorum_slice_definitions': {
            **{
                node: {
                    'nodes': {'A1', 'A2', 'A3', 'A4'},
                    'threshold': 3,
                    'children_definitions': []
                } for node in ['A1', 'A2', 'A3', 'A4']
            },
            **{
                node: {
                    'nodes': set(),
                    'threshold': 2,
                    'children_definitions': [
                        {
                            'nodes': {'A1', 'A2', 'A3', 'A4'},
                            'threshold': 3,
                            'children_definitions': []
                        },
                        {
                            'nodes': {'B1', 'B2', 'B3'},
                            'threshold': 2,
                            'children_definitions': []
                        }
                    ]
                } for node in ['B1', 'B2', 'B3']
            },
            'C': {
                'nodes': {'C'},
                'threshold': 2,
                'children_definitions': [
                    {
                        'nodes': {'A1', 'A2', 'A3', 'A4'},
                        'threshold': 3,
                        'children_definitions': []
                    }
                ]
            }
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
    },
    {
        'name': 'ex:stellar-new',
        'nodes': ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'C'],
        'node_names': None,
        'quorum_slice_definitions': {
            node: {
                'nodes': set(),
                'threshold': 3,
                'children_definitions': [
                    {
                        'nodes': {'A1', 'A2', 'A3', 'A4'},
                        'threshold': 3,
                        'children_definitions': []
                    },
                    {
                        'nodes': {'B1', 'B2', 'B3'},
                        'threshold': 2,
                        'children_definitions': []
                    },
                    {
                        'nodes': {'C'},
                        'threshold': 1,
                        'children_definitions': []
                    }
                ]
            } for node in ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'C']
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
    },
    {
        'name': 'ex:stellar-new-2',
        'nodes': ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'C4', 'C5'],
        'node_names': None,
        'quorum_slice_definitions': {
            node: {
                'nodes': set(),
                'threshold': 2,
                'children_definitions': [
                    {
                        'nodes': {'A1', 'A2', 'A3'},
                        'threshold': 2,
                        'children_definitions': []
                    },
                    {
                        'nodes': {'B1', 'B2', 'B3'},
                        'threshold': 2,
                        'children_definitions': []
                    },
                    {
                        'nodes': {'C1', 'C2', 'C3', 'C4', 'C5'},
                        'threshold': 3,
                        'children_definitions': []
                    },
                ]
             } for node in ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'C4', 'C5']
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
    },
    {
        'name': 'ex:stellar-new-3',
        'nodes': ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'C4', 'C5'],
        'node_names': None,
        'quorum_slice_definitions': {
            node: {
                'nodes': set(),
                'threshold': 2,
                'children_definitions': [
                    {
                        'nodes': {'A1', 'A2', 'A3'},
                        'threshold': 2,
                        'children_definitions': []
                    },
                    {
                        'nodes': {'B1', 'B2', 'B3'},
                        'threshold': 2,
                        'children_definitions': []
                    },
                    {
                        'nodes': {'C1', 'C2', 'C3', 'C4', 'C5'},
                        'threshold': 4,
                        'children_definitions': []
                    },
                ]
            } for node in ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'C4', 'C5']
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
    },
    {
      'name': 'Stellar Network',
      'nodes': list(stellar_network[0]),
      'node_names': stellar_network[2],
      'quorum_slice_definitions': stellar_network[1],
      'analyzers': [eigenvector_analyzer, subgraph_analyzer]
    }
]

for example in examples:
    print()
    print('Running {0}'.format(example['name']))
    for analyzer in example['analyzers']:
        quorum_slice_definitions = {
            node: get_normalized_definition(definition, node) for node, definition in example['quorum_slice_definitions'].items()
        }
        analyzer(example['nodes'], quorum_slice_definitions, example['node_names'])

