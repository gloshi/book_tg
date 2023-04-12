from datetime import datetime

from aiogram import Dispatcher, Bot, types
from aiogram.bot import api
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from app.handlers.admin import *
from app.handlers.main import *
from app.keyboards import kb_main
from app.models import models_create, Account
from config import TG_TOKEN, TEXTS

PATCHED_URL = 'https://telegg.ru/orig/bot{token}/{method}'
setattr(api, 'API_URL', PATCHED_URL)
bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


HANDLERS = [
    {'handler': main, 'state': Form.main, 'content_types': ['text']},
    {'handler': main_catalog, 'state': Form.main_catalog, 'content_types': ['text']},
    {'handler': main_cart, 'state': Form.main_cart, 'content_types': ['text']},
    {'handler': admin, 'state': Form.admin, 'content_types': ['text']},
    {'handler': admin_category, 'state': Form.admin_category, 'content_types': ['text']},
    {'handler': admin_author, 'state': Form.admin_author, 'content_types': ['text']},
    {'handler': admin_book_photo, 'state': Form.admin_book_photo, 'content_types': ['photo']},
    {'handler': admin_book, 'state': Form.admin_book, 'content_types': ['text']},

]


def init_message_handlers():
    [dp.register_message_handler(h['handler'], state=h['state'], content_types=h['content_types']) for h in HANDLERS]


@dp.message_handler()
async def start(message: types.Message):
    user_id = message.from_user.id
    account = Account.get_or_none(Account.user_id == user_id)
    if not account:
        account = Account(user_id=user_id, firstname=message.from_user.first_name,
                          lastname=message.from_user.last_name, reg_datetime=datetime.now())
        account.save()
        await message.reply(text=TEXTS['reg'].format(account.firstname),
                            reply_markup=kb_main)
    else:
        await message.reply(text=TEXTS['to_main'].format(account.firstname),
                            reply_markup=kb_main)
    await Form.main.set()


if __name__ == '__main__':
    init_message_handlers()
    models_create()
    executor.start_polling(dispatcher=dp)
