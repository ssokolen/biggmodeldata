from .schema import ReactionNames, ReactionECs, ReactionMetabolites, ReactionAlternatives

def ecs(rid):
    
    query = ReactionECs.select().where(ReactionECs.rid == rid)
    return [item.ec for item in query] 

def ids(ec):

    query = ReactionECs.select().where(ReactionECs.ec == ec)
    return [item.rid for item in query] 

def reactants(rid):

    query = ReactionMetabolites.select().where(
        (ReactionMetabolites.rid == rid) & (ReactionMetabolites.stoichiometry < 0)
    )
    return [(item.stoichiometry, item.mid) for item in query] 

def products(rid):

    query = ReactionMetabolites.select().where(
        (ReactionMetabolites.rid == rid) & (ReactionMetabolites.stoichiometry > 0)
    )
    return [(item.stoichiometry, item.mid) for item in query] 

def alternatives(rid, include_self = True):

    query = ReactionAlternatives.select().where(ReactionAlternatives.rid == rid)
    out = [rid] if include_self else []

    return out + [item.alternative for item in query] 


