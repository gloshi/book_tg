from requests import post

from aiogram import types

from app.forms import Form
from app.keyboards import *
from app.models import Account, Book, Category, Author, Cart, Order
from config import TEXTS, ON_PAGE, BOOKS_PHOTOS_PATH, TG_TOKEN

accounts_catalogs = []


class AccountCatalog:
    account = None
    price_from = 0
    price_to = 0
    authors = []
    categories = []
    search = ''
    page = 1
    book_selected = None


'''
funcs
'''


async def send_photo(chat_id, img):
    img = open('{}{}'.format(BOOKS_PHOTOS_PATH, img), 'rb')
    url = f'https://api.telegram.org/bot{TG_TOKEN}/sendPhoto?chat_id={chat_id}'
    post(url, files={'photo': img})


def search(ac: AccountCatalog):
    result = []
    for book in Book.select():
        # Price
        is_correct_price = ac.price_from <= book.price <= ac.price_to
        if ac.price_to == 0:
            is_correct_price = True

        # Authors
        is_author = book.author in ac.authors
        if not ac.authors:
            is_author = True

        # Categories
        is_category = book.category in ac.categories
        if not ac.categories:
            is_category = True

        # Search
        is_search = True
        if ac.search:
            a_str = [s.lower() for s in ac.search.split()]
            n_str = [s.lower() for s in book.name.split()]
            b_str = [s.lower() for s in book.author.name.split()]

            is_search = len(list(set(a_str) & set(n_str))) > 0 or len(list(set(a_str) & set(b_str))) > 0

        # Result
        if is_correct_price and is_author and is_category and is_search:
            result.append(book)

    page = ac.page - 1
    index_from = ON_PAGE * page
    index_to = ON_PAGE * page + ON_PAGE
    result_page = result[index_from:index_to]
    return result_page


def texts(ac: AccountCatalog):
    text_categories = TEXTS['filter_categories_none'] if not ac.categories else TEXTS['filter_categories'].format(
        ac.categories[0].name, len(ac.categories) - 1)
    text_authors = TEXTS['filter_authors_none'] if not ac.authors else TEXTS['filter_authors'].format(
        ac.authors[0].name, len(ac.authors) - 1)
    text_price = TEXTS['filter_price'].format(ac.price_from, ac.price_to) if ac.price_to and ac.price_from else TEXTS[
        'filter_price_none']
    text_search = TEXTS['filter_search_none'] if not ac.search else TEXTS['filter_search'].format(ac.search)
    text_page = TEXTS['filter_page'].format(ac.page)
    return {
        'text_categories': text_categories,
        'text_authors': text_authors,
        'text_price': text_price,
        'text_search': text_search,
        'text_page': text_page,
    }


def result_kb(ac: AccountCatalog, result):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [str(i) for i in range(1, len(result) + 1)]
    kb.add(*buttons)

    t = texts(ac)

    kb.add(KeyboardButton(t['text_categories']), KeyboardButton(t['text_authors']), KeyboardButton(t['text_price']))
    kb.add(KeyboardButton(t['text_search']))
    kb.add(KeyboardButton(TEXTS['filter_page_previous']), KeyboardButton(t['text_page']),
           KeyboardButton(TEXTS['filter_page_next']))
    kb.add(KeyboardButton(TEXTS['kb_back']))
    return kb


async def result_send(message: types.Message, ac: AccountCatalog, param=False):
    # Change page if change any filters
    if param:
        ac.page = 1

    user_id = message.from_user.id
    command = message.text
    account = Account.get_or_none(Account.user_id == user_id)

    result = search(ac)

    kb = result_kb(ac, result)
    text = ''
    for i, r in enumerate(result):
        text += '{}. {} - {}\n'.format(i + 1, r.name, r.author.name)

    text = 'Результатов не найдено' if text == '' else text

    await message.reply(text, reply_markup=kb)


'''
handlers
'''


async def main(message: types.Message):
    user_id = message.from_user.id
    command = message.text
    account = Account.get_or_none(Account.user_id == user_id)
    if command == TEXTS['kb_main_1']:
        cart = [o.book.price for o in Cart.select().where(Cart.account == account)]
        orders = [o.book.price for o in Order.select().where(Order.account == account)]
        s = sum(orders)
        text = TEXTS['stats'].format(account.id, account.user_id,
                                     account.firstname, account.lastname,
                                     account.reg_datetime, 'Да' if account.is_admin else 'Нет',
                                     len(cart), len(orders), s)
        await message.reply(text=text,
                            reply_markup=kb_main)
        return text
    elif command == TEXTS['kb_main_2']:
        orders = [b for b in Order.select().where(Order.account == account)]
        s = sum([o.book.price for o in orders])
        orders_text = ['[{}] {} - {} RUB'.format(o.id, o.book.name, o.book.price) for o in orders]
        text = TEXTS['to_orders'].format('\n'.join(orders_text), len(orders), s)
        await message.reply(text=text, reply_markup=kb_main)
        return text
    elif command == TEXTS['kb_main_3']:
        cart = [b for b in Cart.select().where(Cart.account == account)]
        s = sum([c.book.price for c in cart])
        cart_text = ['{} - {} RUB'.format(o.book.name, o.book.price) for o in cart]
        text = TEXTS['to_cart'].format('\n'.join(cart_text), len(cart), s)
        await message.reply(text=text, reply_markup=kb_cart)
        await Form.main_cart.set()
        return text
    elif command == TEXTS['kb_main_4']:
        ac = AccountCatalog()
        ac.account = account
        accounts_catalogs.append(ac)

        text = TEXTS['to_catalog']
        try:
            await message.reply(text=text)
            await result_send(message, ac)
            await Form.main_catalog.set()
        except:
            return text
    elif command in ['/adm', '/admin'] and account.is_admin:
        text = TEXTS['to_admin']
        await message.reply(text=text,
                            reply_markup=kb_admin)
        await Form.admin.set()
        return text
    else:
        text = TEXTS['error_command']
        await message.reply(text=text,
                            reply_markup=kb_main)
        return text


async def main_cart(message: types.Message):
    user_id = message.from_user.id
    command = message.text
    account = Account.get_or_none(Account.user_id == user_id)
    if command == TEXTS['kb_back']:
        await message.reply(text=TEXTS['to_main'].format(account.firstname), reply_markup=kb_main)
        await Form.main.set()
    elif command == TEXTS['kb_cart_1']:

        cart = [b for b in Cart.select().where(Cart.account == account)]
        [Order(book=b.book, account=account).save() for b in cart]
        [b.delete_instance() for b in cart]

        text = TEXTS['suc_buy']
        await message.reply(text=text.format(account.firstname), reply_markup=kb_main)
        try:
            await Form.main.set()
        except:
            return text
    else:
        await message.reply(text=TEXTS['error_command'],
                            reply_markup=kb_cart)


async def main_catalog(message: types.Message):
    user_id = message.from_user.id
    command = message.text
    account = Account.get_or_none(Account.user_id == user_id)
    ac: AccountCatalog = AccountCatalog()
    for c in accounts_catalogs:
        if c.account == account:
            ac = c

    if ac.book_selected:
        if command == TEXTS['kb_back']:
            ac.book_selected = None
            await result_send(message, ac)
        elif command == TEXTS['kb_book_1']:
            Cart(account=account, book=ac.book_selected).save()
            await message.reply(text=TEXTS['suc_add_cart'].format(ac.book_selected.name))
            ac.book_selected = None
            await result_send(message, ac)
        return

    if -1 in ac.categories:
        text = ''
        if command == TEXTS['kb_back']:
            ac.categories.remove(-1)
            await result_send(message, ac, True)
            return
        for category in Category.select():
            if category.name == command:
                if category not in ac.categories:
                    ac.categories.append(category)
                else:
                    ac.categories.remove(category)

        for c in ac.categories:
            if c == -1:
                continue
            text += '{}\n'.format(c.name)

        await message.reply(text=TEXTS['suc_filter_categories'].format(text))
        return
    elif -1 in ac.authors:
        text = ''
        if command == TEXTS['kb_back']:
            ac.authors.remove(-1)
            await result_send(message, ac, True)
            return
        for author in Author.select():
            if author.name == command:
                if author not in ac.authors:
                    ac.authors.append(author)
                else:
                    ac.authors.remove(author)

        for c in ac.authors:
            if c == -1:
                continue
            text += '{}\n'.format(c.name)

        await message.reply(text=TEXTS['suc_filter_authors'].format(text))
        return
    elif ac.price_to == -1:
        if command == TEXTS['kb_back']:
            ac.price_to = 0
            ac.price_from = 0
            await result_send(message, ac)
            return
        prices = command.split('-')
        if len(prices) == 2:
            if prices[0].isdigit() and prices[1].isdigit():
                ac.price_from = int(prices[0])
                ac.price_to = int(prices[1])
                await result_send(message, ac, True)
                return
        await message.reply(text=TEXTS['error_command'])
        return
    elif ac.search == -1:
        if command == TEXTS['kb_back']:
            ac.search = None
            await result_send(message, ac)
            return

        ac.search = command
        await result_send(message, ac, True)
        return

    if command.isdigit():
        num = int(command)
        if num in range(1, ON_PAGE+1):
            try:
                result = search(ac)[num-1]
                book = result
                ac.book_selected = book

                await send_photo(user_id, book.photo)
                await message.reply(text=TEXTS['filter_result_book'].format(
                    book.name, book.category.name, book.author.name, book.price, book.description
                ), reply_markup=kb_book)
                return
            except IndexError:
                pass

    t = texts(ac)

    if command == t['text_categories']:
        ac.categories.append(-1)
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        [kb.add(KeyboardButton(c.name)) for c in Category.select()]
        kb.add(KeyboardButton(TEXTS['kb_back']))
        await message.reply(text=TEXTS['to_categories'], reply_markup=kb)
        return
    elif command == t['text_authors']:
        ac.authors.append(-1)
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        [kb.add(KeyboardButton(a.name)) for a in Author.select()]
        kb.add(KeyboardButton(TEXTS['kb_back']))
        await message.reply(text=TEXTS['to_authors'], reply_markup=kb)
        return
    elif command == t['text_price']:
        ac.price_from = -1
        ac.price_to = -1
        await message.reply(text=TEXTS['to_price'], reply_markup=kb_back)
        return
    elif command == t['text_search']:
        ac.search = -1
        await message.reply(text=TEXTS['to_search'], reply_markup=kb_back)
        return
    elif command == TEXTS['filter_page_next']:
        ac.page += 1
        await result_send(message, ac)
        return
    elif command == TEXTS['filter_page_previous']:
        if ac.page - 1 > 0:
            ac.page -= 1
            await result_send(message, ac)
            return
    if command == TEXTS['kb_back']:
        accounts_catalogs.remove(ac)
        await message.reply(text=TEXTS['to_main'].format(account.firstname), reply_markup=kb_main)
        await Form.main.set()
        return

    await message.reply(text=TEXTS['error_command'])
