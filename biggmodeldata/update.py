import os
import pkg_resources
import re
import requests
import sys

from .schema import ReactionNames, ReactionECs, ReactionMetabolites, ReactionAlternatives
from .schema import recreate_reaction_tables
from . import metabolites as m

reaction_file = pkg_resources.resource_filename(
    'biggmodeldata', 'data/bigg_models_reactions.txt'
)

def update_reactions(download = True):

    # Download updated reaction data
    if download:
        print("Downloading reaction data...")
        
        url = "http://bigg.ucsd.edu/static/namespace/bigg_models_reactions.txt"
        
        r = requests.get(url)
        
        with open(reaction_file, 'w') as f:
            f.write(r.text)
        
        print("Done.")

    # Dropping old tables
    recreate_reaction_tables()

    with open(reaction_file, 'r') as f:
        reaction_data = f.readlines()

    # Sets of reactions that share the same core reactants/products are
    # generated in a dictionary mapped by reactant/products sets.
    # Once the dictionary is generated, a separate loop adds all links.
    noncore = set(m.helpers())
    alternatives = {}

    re_ec = re.compile("EC Number: http:.*?(\\d+\.\\d+\.\\d+\.\\d+);")
    re_arrow = re.compile(" [<]-> ")

    n = len(reaction_data) - 1
    sys.stdout.write("\n")

    #test = [reaction_data[i] for i in [1955, 1579]]
    #for i, line in enumerate(test):
    
    for i, line in enumerate(reaction_data[1:]):

        sys.stdout.write("Processing reaction {:5n} of {:5n}\r".format(i+1, n))
        sys.stdout.flush()

        line = line.split('\t')

        rid = line[0]
        name = line[1]
        reaction = line[2]
        models = line[3]
        links = line[4]

        # Name and id
        entry = ReactionNames.create(rid = rid, name = name)
        entry.save()

        # ReactionECs
        ecs = re_ec.findall(links)
        
        for ec in ecs:
            entry = ReactionECs.create(rid = rid, ec = ec)
            entry.save()

        # ReactionMetabolites (and alternative pathways)
        reversible = True if " <-> " in reaction else False
        reactants, products = re_arrow.split(reaction)

        core_metabolites = []

        reactants = reactants.split("+")
        for reactant in reactants:
            reactant, stoichiometry = _parse_stoichiometry(reactant)

            entry = ReactionMetabolites.create(
                rid = rid, reversible = reversible, 
                mid = reactant, stoichiometry = -stoichiometry
            )
            entry.save()

            if reactant not in noncore:
                core_metabolites.append(reactant)
        
        products = products.split("+")
        for product in products:
            product, stoichiometry = _parse_stoichiometry(product)

            entry = ReactionMetabolites.create(
                rid = rid, reversible = reversible, 
                mid = product, stoichiometry = stoichiometry
            )
            entry.save()

            if product not in noncore:
                core_metabolites.append(product)

        # Adding to alternatives list
        key = '_'.join(sorted(core_metabolites))

        if key not in alternatives:
            alternatives[key] = [rid]
        else:
            alternatives[key].append(rid)

    sys.stdout.write("\n")
    print("Done.")

    # Generating alternative lists
    n = range(len(alternatives))
    for i, values in enumerate(alternatives.values()):
        
        sys.stdout.write("Linking common reaction {:5n} of {:5n}\r".format(i+1, n))
        sys.stdout.flush()
        
        for i in range(len(values)):
            for j in range(len(values)):
                if i != j:
                    entry = ReactionAlternatives.create(
                        rid = values[i], alternative = values[j]
                    )
                    entry.save()

    sys.stdout.write("\n")
    print("Done.")

re_stoichiometry = re.compile("^[0-9.]+ ")
re_metabolite = re.compile("^[0-9.]* (\\w+)")

def _parse_stoichiometry(entry):

    entry = entry.strip("\t ")
    match = re_stoichiometry.match(entry)
    
    if match:
        stoichiometry = float(match.group(0))
        match = re_metabolite.match(entry)
        entry = match.group(1)
    else:
        stoichiometry = 1.0

    return (entry, stoichiometry)



        


