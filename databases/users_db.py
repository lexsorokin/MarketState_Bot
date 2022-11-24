from peewee import *

db = SqliteDatabase('MarketState.db')


class User(Model):
    user_id = IntegerField(null=True)
    username = CharField(null=True, max_length=100)
    first_name = CharField(null=True, max_length=100)

    class Meta:
        database = db


db.connect()
User.create_table()
