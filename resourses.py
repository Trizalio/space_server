import peewee
# import sqlite3
# import psycopg2
# import PyMySQL
from peewee import *

print "connect db"
# db = MySQLDatabase('space_team', user='root',passwd='3421')
db = SqliteDatabase('space_team.db')


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



tables_list = [ShipModel, Ship, ShipModuleTask]

def create_table_if_necessary(table):
    if not table.table_exists():
        print(table.__name__, "does not exist, creating...")
        db.create_table(table)
        print(table.__name__, "created")
    else:
        print(table.__name__, "found")

print("checking db tables existence")
for table in tables_list:
    create_table_if_necessary(table)

print("db tables are ready")