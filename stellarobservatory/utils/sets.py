from itertools import chain, combinations

def deepfreezesets(sets_iterable):
    """Deep-freeze a list of sets"""
    return frozenset([frozenset(list(el)) for el in sets_iterable])

def powerset(iterable):
    """Return the power set of the input iterable"""
    frozen_iterable_set = frozenset(iterable)
    all_combinations = [combinations(frozen_iterable_set, size) for size in range(len(frozen_iterable_set) + 1)]
    return [frozenset(combination) for combination in chain(*all_combinations)]
