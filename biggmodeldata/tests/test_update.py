import logging
from unittest import TestCase

import biggmodeldata 
from biggmodeldata import update_reactions, ReactionNames, ReactionECs
from biggmodeldata import reactions as r
from biggmodeldata import metabolites as m

class TestUpdate(TestCase):

    def test_reactions(self):

        # Don't redownload to avoid needless traffic while testing
        update_reactions(download = False)
        
        entry = ReactionNames.select().where(ReactionNames.rid == "SUCD1").get()
        assert entry.name == "Succinate dehydrogenase"

        entry = ReactionECs.select().where(ReactionECs.rid == "SUCD1").get()
        assert entry.ec == "1.3.5.1"

        # TODO: add a couple more tests

class TestAccess(TestCase):

    def test_reactions(self):

        assert r.ecs("SUCD1") == ["1.3.5.1"]
        assert "SUCD1" in r.ids("1.3.5.1") 
        assert r.reactants("SUCD1") == [(-1.0, "fad_c"), (-1.0, "succ_c")]
        assert r.products("SUCD1") == [(1.0, "fadh2_c"), (1.0, "fum_c")]
        assert r.alternatives("SUCD1") == ["SUCD1", "FRDcm", "FRD", "FRDx"]
