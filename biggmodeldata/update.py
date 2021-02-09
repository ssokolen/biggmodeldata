import os
import pkg_resources
import re
import sys

from .schema import Names, ECs, Metabolites, Alternatives
from .schema import recreate_tables

reaction_file = pkg_resources.resource_filename(
    'biggmodeldata', 'data/bigg_models_reactions.txt'
)

def update(download = True):

    # Download updated reaction data
    if download:
        print("Downloading reaction data...")
        pass
        print("Done.")

    # Dropping old tables
    recreate_tables()

    with open(reaction_file, 'r') as f:
        reaction_data = f.readlines()

    # Sets of reactions that share the same core reactants/products are
    # generated in a dictionary mapped by reactant/products sets.
    # Once the dictionary is generated, a separate loop adds all links.
    exclude = set([
        'q_c', 'dopaqn_c', 'thf_c', 'amet_c', 'pqq_c', 'thdp_c', 'pydx5p_c',
        'pan4p_c', 'pq_c', 'nad_c', 'mpt_c', 'micit_c', 'b12_e', 'hemoglobin_e',
        'CE6242_c', 'fmnRD_c', 'fadh2_c', 'fad_c', 'f430_c', 'dianethal_c', 'com_c',
        'cob_c', 'coa_c', 'btn_c', 'dhptn_c', 'h_c', 'h2o_c', 'k_c','o2_c', 'co2_c', 
        'nh3_c', 'amp_c', 'h2o2_c', 'gtp_c', 'cmp_c', 'utp_c', 'ump_c', 'cmp_c', 'cu2_c',
        'ca2_c', 'atp_c', 'nadh_c', 'nadp_c', 'nadph_c',
    ])

    alternatives = {}

    re_ec = re.compile("EC Number: http:.*?(\\d+\.\\d+\.\\d\.\\d+);")
    re_arrow = re.compile(" [<]-> ")

    n = len(reaction_data) - 1
    sys.stdout.write("\n")

    #for i, line in enumerate(reaction_data[1955:1956]):
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
        entry = Names.create(rid = rid, name = name)
        entry.save()

        # ECs
        ecs = re_ec.findall(links)
        
        for ec in ecs:
            entry = ECs.create(rid = rid, ec = ec)
            entry.save()

        # Metabolites (and alternative pathways)
        reversible = True if " <-> " in reaction else False
        reactants, products = re_arrow.split(reaction)

        core_metabolites = []

        reactants = reactants.split("+")
        for reactant in reactants:
            reactant, stoichiometry = _parse_stoichiometry(reactant)

            entry = Metabolites.create(
                rid = rid, reversible = reversible, 
                mid = reactant, stoichiometry = -stoichiometry
            )
            entry.save()

            if reactant not in exclude:
                core_metabolites.append(reactant)
        
        products = products.split("+")
        for product in products:
            product, stoichiometry = _parse_stoichiometry(product)

            entry = Metabolites.create(
                rid = rid, reversible = reversible, 
                mid = product, stoichiometry = stoichiometry
            )
            entry.save()

            if product not in exclude:
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
    for values in alternatives.values():
        
        for i in range(len(values)):
            for j in range(len(values)):
                if i != j:
                    entry = Alternatives.create(rid = values[i], alternative = values[j])
                    entry.save()

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



        


