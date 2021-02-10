import pkg_resources
from peewee import *

db_file = pkg_resources.resource_filename(
    'biggmodeldata', 'data/biggmodeldata.db'
)
db = SqliteDatabase(db_file)

class ReactionNames(Model):
    rid = CharField()
    name = TextField()

    class Meta:
        database = db

class ReactionECs(Model):
    rid = CharField()
    ec = CharField()

    class Meta:
        database = db

class ReactionMetabolites(Model):
    rid = CharField()
    reversible = BooleanField()
    mid = CharField()
    stoichiometry = FloatField()

    class Meta:
        database = db

class ReactionAlternatives(Model):
    rid = CharField()
    alternative = CharField()

    class Meta:
        database = db

reaction_tables = [ReactionNames, ReactionECs, ReactionMetabolites, ReactionAlternatives]

db.connect()
db.create_tables(reaction_tables)

def recreate_reaction_tables():
    db.drop_tables(reaction_tables)
    db.create_tables(reaction_tables)
