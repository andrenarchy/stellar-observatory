import numpy
from typing import Callable, Dict, Generic, List, Set, TypeVar, TypedDict, Union
from stellarobservatory import quorum_slice_definition, stellarbeat, centralities
from stellarobservatory.quorum_slice_definition import Definitions
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
    sorted_indexes = numpy.argsort(centralities)[::-1]
    for node_index in sorted_indexes:
        node = nodes[node_index]
        print('{0}: {1}'.format(node_names[node] if node_names is not None else node, centralities[node_index]))

Analyzer = List[Callable[[List[Node], Definitions, Union[Dict[Node,str],None]],None]]

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

def befouling_analyzer(nodes: List[Node], definitions: Definitions, node_names: Dict[Node, str]=None):
    def get_ill_behaved_weight(ill_behaved_nodes):
        return 1/len(ill_behaved_nodes)
    print()
    print('befouling analyzer')
    print('------------------------')
    print('centralities:')
    print_centralities(nodes, centralities.get_befouling_centralities(nodes, definitions, get_ill_behaved_weight), node_names)
    print()

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
      'name': 'Example 3.4',
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
        eigenvector_analyzer,
        subgraph_analyzer,
        befouling_analyzer,
        quorum_eigenvector_analyzer,
        quorum_subgraph_analyzer,
        quorum_intersection_eigenvector_analyzer
      ]
    },
    {
      'name': 'Stellar Network',
      'nodes': list(stellar_network[0]),
      'node_names': stellar_network[2],
      'quorum_slice_definitions': stellar_network[1],
      'analyzers': [eigenvector_analyzer, subgraph_analyzer]
    },
    # {
    #     'name': 'Example 1',
    #     'nodes': [1, 2, 3, 4],
    #     'quorum_slices': {
    #         1: [{1,2}],
    #         2: [{1,2}],
    #         3: [{1,3,4}],
    #         4: [{1,3,4}]
    #     }
    # }
]

for example in examples:
    print()
    print('Running {0}'.format(example['name']))
    for analyzer in example['analyzers']:
        analyzer(example['nodes'], example['quorum_slice_definitions'], example['node_names'])

