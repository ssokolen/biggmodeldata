import logging
from unittest import TestCase

import biggmodeldata 
from biggmodeldata import update, Names, ECs
from biggmodeldata import ecs, ids, reactants, products, alternatives

class TestUpdate(TestCase):

    def test_db(self):
        #update(download = False)
        
        entry = Names.select().where(Names.rid == "SUCD1").get()
        assert entry.name == "Succinate dehydrogenase"

        entry = ECs.select().where(ECs.rid == "SUCD1").get()
        assert entry.ec == "1.3.5.1"

class TestAccess(TestCase):

    def test_all(self):
        assert ecs("SUCD1") == ["1.3.5.1"]
        assert "SUCD1" in ids("1.3.5.1") 
        assert reactants("SUCD1") == [(-1.0, "fad_c"), (-1.0, "succ_c")]
        assert products("SUCD1") == [(1.0, "fadh2_c"), (1.0, "fum_c")]
        assert alternatives("SUCD1") == ["SUCD1", "FRD", "FRDx"]
