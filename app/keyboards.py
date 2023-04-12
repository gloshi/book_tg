from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import TEXTS

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cart = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_book = ReplyKeyboardMarkup(resize_keyboard=True)
kb_back = ReplyKeyboardMarkup(resize_keyboard=True)

kb_main.add(KeyboardButton(TEXTS['kb_main_1']), KeyboardButton(TEXTS['kb_main_2']))
kb_main.add(KeyboardButton(TEXTS['kb_main_3']), KeyboardButton(TEXTS['kb_main_4']))

kb_admin.add(KeyboardButton(TEXTS['kb_admin_1']))
kb_admin.add(KeyboardButton(TEXTS['kb_admin_2']), KeyboardButton(TEXTS['kb_admin_3']))
kb_admin.add(KeyboardButton(TEXTS['kb_back']))

kb_cart.add(KeyboardButton(TEXTS['kb_cart_1']), KeyboardButton(TEXTS['kb_back']))
kb_book.add(KeyboardButton(TEXTS['kb_book_1']), KeyboardButton(TEXTS['kb_back']))

kb_back.add(KeyboardButton(TEXTS['kb_back']))
