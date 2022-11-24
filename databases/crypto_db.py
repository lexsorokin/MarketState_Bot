from peewee import *
from databases.users_db import User

db = SqliteDatabase('MarketState.db')


class CryptoFavorites(Model):
    user = ForeignKeyField(model=User, null=True)
    token_ticker = CharField(null=True)

    class Meta:
        database = db


db.connect()
CryptoFavorites.create_table()
