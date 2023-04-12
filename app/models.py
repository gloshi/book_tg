from peewee import *

from config import *


db = SqliteDatabase('db.db')


def models_create():
    Account.create_table()
    Author.create_table()
    Category.create_table()
    Book.create_table()
    Cart.create_table()
    Order.create_table()


class BaseModel(Model):
    class Meta:
        database = db


class Account(BaseModel):
    id = PrimaryKeyField()
    user_id = IntegerField()
    firstname = CharField()
    lastname = CharField()
    reg_datetime = DateTimeField()
    is_admin = BooleanField(default=False)

    class Meta:
        db_table = "account"


class Author(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=256)

    class Meta:
        db_table = "authors"


class Category(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=256)

    class Meta:
        db_table = "categories"


class Book(BaseModel):
    id = PrimaryKeyField()
    author = ForeignKeyField(Author, to_field='id', on_delete='cascade')
    category = ForeignKeyField(Category, to_field='id', on_delete='cascade')
    photo = CharField()
    name = CharField(max_length=256)
    description = CharField(max_length=512)
    price = IntegerField()

    class Meta:
        db_table = "books"


class Cart(BaseModel):
    id = PrimaryKeyField()
    account = ForeignKeyField(Account, to_field='id', on_delete='cascade')
    book = ForeignKeyField(Book, to_field='id', on_delete='cascade')

    class Meta:
        db_table = "carts"


class Order(BaseModel):
    id = PrimaryKeyField()
    account = ForeignKeyField(Account, to_field='id', on_delete='cascade')
    book = ForeignKeyField(Book, to_field='id', on_delete='cascade')

    class Meta:
        db_table = "orders"
