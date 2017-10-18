import peewee
from peewee import *

print "connect db"
db = MySQLDatabase('space_team', user='root',passwd='3421')


class ShipModel(peewee.Model):
    name = CharField()
    json = TextField()

    class Meta:
        database = db

class Ship(peewee.Model):
    name = CharField()
    json = TextField()
    manufacture_date = DateField()
    model = ForeignKeyField(ShipModel, related_name='instances')

    class Meta:
        database = db

class ShipModuleTask(peewee.Model):
    module = CharField()
    task = TextField()
    ship = ForeignKeyField(Ship, related_name='modules')

    class Meta:
        database = db

print "create_tables"
# db.create_tables([ShipModel, Ship])
# db.create_tables([ShipModuleTask])