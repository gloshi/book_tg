from random import randint

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.forms import Form
from app.keyboards import kb_main, kb_admin, kb_back
from app.models import Account, Author, Category, Book
from config import TEXTS, BOOKS_PHOTOS_PATH


book = {
    'photo': '',
    'author': None,
    'category': None,
    'name': None,
    'description': None,
    'price': None,
}


async def admin(message: types.Message):
    user_id = message.from_user.id
    command = message.text
    account = Account.get_or_none(Account.user_id == user_id)

    if command == TEXTS['kb_admin_1']:
        await message.reply(text=TEXTS['to_admin_book_photo'], reply_markup=kb_back)
        await Form.admin_book_photo.set()
    elif command == TEXTS['kb_admin_2']:
        await message.reply(text=TEXTS['to_admin_category'], reply_markup=kb_back)
        await Form.admin_category.set()
    elif command == TEXTS['kb_admin_3']:
        await message.reply(text=TEXTS['to_admin_author'], reply_markup=kb_back)
        await Form.admin_author.set()
    elif command == TEXTS['kb_back']:
        await message.reply(text=TEXTS['to_main'].format(account.firstname), reply_markup=kb_main)
        await Form.main.set()
    else:
        await message.reply(text=TEXTS['error_command'], reply_markup=kb_admin)


async def admin_author(message: types.Message):
    user_id = message.from_user.id
    command = message.text
    account = Account.get_or_none(Account.user_id == user_id)
    name = command.split()
    if command == TEXTS['kb_back']:
        await message.reply(text=TEXTS['to_admin'], reply_markup=kb_admin)
        await Form.admin.set()
    elif len(name) == 2:
        Author(name='{} {}'.format(name[0].capitalize(), name[1].capitalize())).save()
        await message.reply(text=TEXTS['suc_admin_author'].format(account.firstname), reply_markup=kb_admin)
        await Form.admin.set()
    else:
        await message.reply(text=TEXTS['error_command'], reply_markup=kb_back)


async def admin_category(message: types.Message):
    user_id = message.from_user.id
    command = message.text
    account = Account.get_or_none(Account.user_id == user_id)
    if command == TEXTS['kb_back']:
        await message.reply(text=TEXTS['to_admin'], reply_markup=kb_admin)
        await Form.admin.set()
    else:
        Category(name=command).save()
        await message.reply(text=TEXTS['suc_admin_category'].format(account.firstname), reply_markup=kb_admin)
        await Form.admin.set()


async def admin_book_photo(message: types.Message):
    user_id = message.from_user.id
    command = message.text
    account = Account.get_or_none(Account.user_id == user_id)
    if command == TEXTS['kb_back']:
        await message.reply(text=TEXTS['to_admin'], reply_markup=kb_admin)
        await Form.admin.set()
    else:
        image_name = '{}-{}.png'.format(message.from_user.id, randint(1, 99999))
        image_path = BOOKS_PHOTOS_PATH + image_name
        await message.photo[-1].download(destination_file=image_path)

        book['photo'] = image_name
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        [kb.add(KeyboardButton(author.name)) for author in Author.select()]
        kb.add(TEXTS['kb_back'])

        await message.reply(text=TEXTS['suc_admin_book_photo'], reply_markup=kb)
        await Form.admin_book.set()


async def admin_book(message: types.Message):
    global book
    user_id = message.from_user.id
    command = message.text
    account = Account.get_or_none(Account.user_id == user_id)
    if command == TEXTS['kb_back']:
        book = {
            'photo': '',
            'author': None,
            'category': None,
            'name': None,
            'description': None,
            'price': None,
        }
        await message.reply(text=TEXTS['to_admin'], reply_markup=kb_admin)
        await Form.admin.set()

    elif book['author'] is None:
        author = Author.get_or_none(Author.name == command)
        if author:
            book['author'] = author

            kb = ReplyKeyboardMarkup(resize_keyboard=True)
            [kb.add(KeyboardButton(category.name)) for category in Category.select()]
            kb.add(TEXTS['kb_back'])

            await message.reply(text=TEXTS['suc_admin_book_author'], reply_markup=kb)
            return
    elif book['category'] is None:
        category = Category.get_or_none(Category.name == command)
        if category:
            book['category'] = category
            await message.reply(text=TEXTS['suc_admin_book_category'], reply_markup=kb_back)
            return
    elif book['name'] is None:
        book['name'] = command
        await message.reply(text=TEXTS['suc_admin_book_name'], reply_markup=kb_back)
        return
    elif book['description'] is None:
        book['description'] = command
        await message.reply(text=TEXTS['suc_admin_book_description'], reply_markup=kb_back)
        return
    elif book['price'] is None:
        if command.isdigit():
            book['price'] = int(command)
            await message.reply(text=TEXTS['suc_admin_book_price'], reply_markup=kb_back)
            await message.reply(text=TEXTS['suc_admin_book'], reply_markup=kb_admin)
            await Form.admin.set()

            # Create book
            Book(photo=book['photo'],
                 author=book['author'],
                 category=book['category'],
                 name=book['name'],
                 description=book['description'],
                 price=book['price'],).save()
            book = {
                'photo': '',
                'author': None,
                'category': None,
                'name': None,
                'description': None,
                'price': None,
            }
            return

    await message.reply(text=TEXTS['error_command'])
