from .schema import Names, ECs, Metabolites, Alternatives

def _similar():
    pass

def ecs(rid):
    
    query = ECs.select().where(ECs.rid == rid)
    return [item.ec for item in query] 

def ids(ec):

    query = ECs.select().where(ECs.ec == ec)
    return [item.rid for item in query] 

def reactants(rid):

    query = Metabolites.select().where(
        (Metabolites.rid == rid) & (Metabolites.stoichiometry < 0)
    )
    return [(item.stoichiometry, item.mid) for item in query] 

def products(rid):

    query = Metabolites.select().where(
        (Metabolites.rid == rid) & (Metabolites.stoichiometry > 0)
    )
    return [(item.stoichiometry, item.mid) for item in query] 

def alternatives(rid, include_self = True):

    query = Alternatives.select().where(Alternatives.rid == rid)
    out = [rid] if include_self else []

    return out + [item.alternative for item in query] 


