import pkg_resources
from peewee import *

db_file = pkg_resources.resource_filename(
    'biggmodeldata', 'data/biggmodeldata.db'
)
db = SqliteDatabase(db_file)

class Names(Model):
    rid = CharField()
    name = TextField()

    class Meta:
        database = db

class ECs(Model):
    rid = CharField()
    ec = CharField()

    class Meta:
        database = db

class Metabolites(Model):
    rid = CharField()
    reversible = BooleanField()
    mid = CharField()
    stoichiometry = FloatField()

    class Meta:
        database = db

class Alternatives(Model):
    rid = CharField()
    alternative = CharField()

    class Meta:
        database = db

tables = [Names, ECs, Metabolites, Alternatives]

db.connect()
db.create_tables(tables)

def recreate_tables():
    db.drop_tables(tables)
    db.create_tables(tables)
