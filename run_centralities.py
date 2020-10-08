import numpy
from typing import Dict, List, Set, TypeVar, TypedDict
from stellarobservatory import quorum_slice_definition, stellarbeat, centralities
from stellarobservatory.quorum_slice_definition import Definitions
from stellarobservatory.utils.graph import Node, Nodes

def get_from_seed_node(seed_node: str):
    stellarbeat_nodes = stellarbeat.get_nodes_from_stellarbeat()
    _, definitions_by_node, node_names = stellarbeat.convert_stellarbeat_to_observatory(stellarbeat_nodes)
    dependencies = quorum_slice_definition.get_transitive_dependencies(definitions_by_node, seed_node)
    reduced_definitions_by_node = {key: definitions_by_node[key] for key in dependencies}
    reduced_node_names = {key: node_names[key] for key in dependencies}
    return dependencies, reduced_definitions_by_node, reduced_node_names

def print_centralities(nodes: List[Node], centralities: numpy.array, node_names: Dict[str,str]=None):
    sorted_indexes = numpy.argsort(centralities)[::-1]
    for node_index in sorted_indexes:
        node = nodes[node_index]
        print('{0}: {1}'.format(node_names[node] if node_names is not None else node, centralities[node_index]))

def analyze_centralities(nodes: List[Node], definitions: Definitions, node_names: Dict[str, str]=None):
    nodes_list = sorted(nodes)
    A = centralities.get_adjacency_matrix(nodes_list, definitions)
    print('adjacency matrix')
    print('----------------')
    print(A)

    print()
    print('eigenvector centralities')
    print('------------------------')
    print_centralities(nodes, centralities.get_eigenvector_centralities(A), node_names)
    print()

    print()
    print('subgraph centralities')
    print('---------------------')
    print_centralities(nodes, centralities.get_subgraph_centralities(A), node_names)
    print()


    def get_ill_behaved_weight(ill_behaved_nodes):
        return 1/len(ill_behaved_nodes)

    print('befouling centralities')
    print('----------------------')
    print_centralities(nodes, centralities.get_befouling_centralities(nodes, definitions, get_ill_behaved_weight), node_names)
    print()

NodesList = List[Node]
class Example(TypedDict):
    name: str
    nodes: NodesList
    quorum_slices: Dict[Node, List[Nodes]]

examples: List[Example] = [
    {
        'name': 'Example 1',
        'nodes': [1, 2, 3, 4],
        'quorum_slices': {
            1: [{1,2}],
            2: [{1,2}],
            3: [{1,3,4}],
            4: [{1,3,4}]
        }
    }
]

for example in examples:
    print('Running {0}'.format(example['name']))
    definitions = {
        key: quorum_slice_definition.quorum_slices_to_definition(quorum_slices)
        for key, quorum_slices in example['quorum_slices'].items()
    }
    analyze_centralities(example['nodes'], definitions)
