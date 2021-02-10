## About the project

The aim of this package is to enable offline lookups of BIGG model data (currently limited to reactions). The code basically serves as a thin wrapper for database creation and access.

### Disclaimer
This is a work in progress meant to fill a gap in our lab's workflow. Use at your own risk.

### Current status
Further updates may be added as required by ongoing work.

## Installation

Install directly from GitHub (or clone and install locally):

```sh
python3 -m pip install git+https://github.com/ssokolen/biggmodeldata
```
## Data source

Data distributed with this package was obtained from the [BIGG website]. Usage of the underlying data is governed by the following:

[BIGG website]: https://ccv-cvc.ca/indexresearcher-eng.frm


Copyright © 2019 The Regents of the University of California

All Rights Reserved

Permission to use, copy, modify and distribute any part of BiGG Models for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice, this paragraph and the following three paragraphs appear in all copies.

Those desiring to incorporate BiGG Models into commercial products or use for commercial purposes should contact the Technology Transfer & Intellectual Property Services, University of California, San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, Ph: (858) 534-5815, FAX: (858) 534-7345, e-mail: invent@ucsd.edu.

In no event shall the University of California be liable to any party for direct, indirect, special, incidental, or consequential damages, including lost profits, arising out of the use of this bigg database, even if the University of California has been advised of the possibility of such damage.

The BiGG Models provided herein is on an "as is" basis, and the University of California has no obligation to provide maintenance, support, updates, enhancements, or modifications. The University of California makes no representations and extends no warranties of any kind, either implied or express, including, but not limited to, the implied warranties of merchantability or fitness for a particular purpose, or that the use of the BiGG Models will not infringe any patent, trademark or other rights.

## Usage

There are currently 5 basic functions oriented around reaction IDs:

```python

from biggmodeldata import reactions as r

# Look-up reaction IDs based on EC number
r.ids("1.3.5.1")

# Look-up EC numbers corresponding to a reaction ID
r.ecs("SUCD1")

# Look-up reaction reactants as a list of (stoichiometry, id) tuples
# Note that reactant stoichiometric coefficients are negative
r.reactants("SUCD1")

# Look-up reaction products as a list of (stoichiometry, id) tuples
r.products("SUCD1")

# Look-up all alternatives to a reaction id, defined as reactions involving
# the same core metabolites (ignore cofactors and energetic compounds like ATP)
r.alternatives("SUCD1")
```

Metabolite IDs may be expanded in the future, but for now, the metabolites module only serves to define a set of "helpers", molecules like ATP and NADH that assist enzymatic function without carrying mass flux.

```python

from biggmodeldata import metabolites as m

# Note that helpers are defined across all possible compartments whether
# this makes biological sense or not, so the list is a bit long
m.helpers()
```

The package is distributed with data included, but you can use the `update_reactions` function to rebuild the databases based on the reaction lists provided by the [BIGG website]. Warning, this step hasn't been optimized and may take a couple of hours.

```python

import biggmodeldata as bigg

bigg.update_reactions()
```
