from functools import lru_cache
import itertools as it

"""
A non-exhaustive list of metabolites that serve to assist enzymatic function
rather than carry flux in the traditional sence of a metabolite flux model.
"""
@lru_cache(maxsize=2)
def helpers():

    # Rough grouping by category
    cofactors = [
        'q', 'dopaqn', 'thf', 'amet', 'pqq', 'thdp', 'pydx5p', 'pan4p',
        'pq', 'mpt', 'micit', 'b12', 'hemoglobin','CE6242','fmnRD',
        'f430', 'dianethal', 'com', 'cob', 'coa', 'btn', 'dhptn',
    ]
    inorganic = ['h', 'h2o', 'k', 'o2', 'co2', 'nh3', 'h2o2', 'cu2', 'ca2', 'fe2']
    energetic = ['atp', 'adp', 'nadh', 'nad', 'nadph', 'nadp', 'fad', 'fadh2']
    oters = ['dtmp', 'dump', 'dcmp', 'dgmp', 'damp'] 

    prefixes = cofactors + inorganic + energetic

    suffixes = [
        'c', 'e', 'm', 'r', 'n', 'g', 'f', 'x', 'v', 'l', 'p', 'h',
        'cx', 'w', 'u', 's', 'um', 'im', 'i', 'cm', 'mm'
    ]

    out = [i[0] + "_" + i[1] for i in it.product(prefixes, suffixes)]

    return out
