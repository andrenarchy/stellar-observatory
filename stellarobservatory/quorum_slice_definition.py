"""Quorum slice definitions"""

from itertools import chain, combinations, product

def get_direct_dependencies(definitions_by_node, node):
    """Get direct dependencies of a node"""
    dependencies = set([node])

    def traverse_definition(definition):
        """Traverses a definition and adds them to the dependencies"""
        for dependency in definition['nodes']:
            if dependency not in dependencies:
                dependencies.add(dependency)
        for children_definition in definition['children_definitions']:
            traverse_definition(children_definition)
    traverse_definition(definitions_by_node[node])

    dependencies.discard(node)
    return dependencies

def get_transitive_dependencies(definitions_by_node, node):
    """Get transitive dependencies of a node"""
    dependencies = set()
    pending_dependencies = set([node])
    while len(pending_dependencies) > 0:
        dependencies.update(pending_dependencies)
        new_pending_dependencies = set()
        for dependency in pending_dependencies:
            new_pending_dependencies.update(
                get_direct_dependencies(definitions_by_node, dependency)
            )
        pending_dependencies = new_pending_dependencies.difference(dependencies)
    dependencies.discard(node)
    return dependencies

def get_trust_graph(definitions_by_node):
    """
    Map each node's public key to its trust graph (the set of nodes it
    references in its quorum slice definitionss). The node itself is excluded.
    """
    return {node: get_direct_dependencies(definitions_by_node, node) \
        for node in definitions_by_node.keys()}

def remove_from_definition(definition, node):
    """Return quorum slice definition with the given node removed and the threshold reduced by 1"""
    threshold = definition['threshold']
    nodes = definition['nodes']
    if node in nodes:
        nodes = nodes.copy()
        nodes.remove(node)
        threshold = max(0, threshold - 1)
    children_definitions = [
        remove_from_definition(children_definition, node)
        for children_definition in definition['children_definitions']
        ]
    return {
        'threshold': threshold,
        'nodes': nodes,
        'children_definitions': children_definitions
    }

def get_normalized_definition(definition, node):
    """Returns the node's quorum slice definition as Stellar Core preprocesses it

    The node is required on root level and removed from rest of quorum slice definition"""
    return {
        'threshold': 2,
        'nodes': {node},
        'children_definitions': [remove_from_definition(definition, node)]
    }

def generate_quorum_slices(definition, mode='economic'):
    """Generate all quorum slices for a quorum slice definition

    'economic' mode only returns quorum slices of size equal to the threshold,
    use 'full' to obtain all quorum slices"""
    threshold = definition['threshold']
    nodes = definition['nodes']
    children_definitions = definition['children_definitions']
    max_size = threshold \
        if mode == 'economic' \
        else len(nodes) + len(children_definitions)

    quorum_slice_pools = [[[node]] for node in nodes] + \
        [generate_quorum_slices(children_definition, mode)
         for children_definition in children_definitions]

    quorum_slice_combinations = list(chain(*[
        combinations(quorum_slice_pools, size)
        for size in range(threshold, max_size + 1)
        ]))

    quorum_slice_products = list(chain(*[
        product(*quorum_slice_combination)
        for quorum_slice_combination in quorum_slice_combinations
        ]))

    return [frozenset(chain(*quorum_slice_product))
            for quorum_slice_product in quorum_slice_products]


def satisfies_definition(candidate, definition):
    '''Checks if the candidate set contains a slice for the provided definition'''
    satisfied = len(definition['nodes'].intersection(candidate))
    for children_definition in definition['children_definitions']:
        if satisfies_definition(candidate, children_definition):
            satisfied += 1
    return satisfied >= definition['threshold']
