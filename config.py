TG_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'
BOOKS_PHOTOS_PATH = 'C:/Users/Сергей/Desktop/book_tg/books_photos/'
ON_PAGE = 3

TEXTS = {
    'reg': '{}, Вы успешно зарегистрировались!\n\n'
           'Что умеет этот бот?\n'
           '-\n'
           '-\n'
           '-\n\n'
           'Вы перемещены в главное меню!',
    'to_main':  '{}, Вы успешно перешли в главое меню!',
    'to_catalog': 'Вы успешно перешли в каталог книг. Вы можете использовать фильтры.',
    'to_admin':  'Вы успешно перешли в панель администратора!',
    'to_admin_book_photo': 'Загрузите фотографию товара',
    'to_admin_category': 'Введите название категории',
    'to_admin_author': 'Введите ИФ автора',

    'error_command': 'Неправильный ввод, повторите попытку.',

    'stats': 'Статистика аккаунта №{}:\n'
             '- ID пользователя: {}\n'
             '- Имя: {}\n'
             '- Фамилия: {}\n'
             '- Дата регистрации: {}\n'
             '- Администратор: {}\n\n'
             '- Книг в корзине: {}\n'
             '- Заказов: {} (на сумму {} RUB)',

    'filter_categories_none': 'Все категории',
    'filter_categories': '{} и еще {} категории(й)',
    'filter_authors_none': 'Все авторы',
    'filter_authors': '{} и еще {} автора(ов)',
    'filter_price': '{} - {} RUB',
    'filter_price_none': 'Любая цена',
    'filter_page': 'Страница {}',
    'filter_page_previous': '<<',
    'filter_page_next': '>>',
    'filter_search': '🔎 {}',
    'filter_search_none': '🔎 Поиск по слову',
    'filter_result_book': '{} ({})\n'
                          'Автор: {}\n\n'
                          'Цена: {} RUB\n\n'
                          '{}\n\n',

    'to_categories': 'Выберите категории книг для поиска',
    'to_authors': 'Выберите авторов книг для поиска',
    'to_price': 'Напишите диапозон цен для поиска (к примеру 100-7000)',
    'to_page': 'Вы перешли на {} страницу',
    'to_search': 'Введите книгу или автора книг',
    'to_cart': 'Ваша корзина:\n\n{}\n\nВсего {} позиций на сумму {} RUB.\nДля покупки нажмите "Купить".',
    'to_orders': 'Ваши заказы:\n\n{}\n\nВсего {} заказов на сумму {} RUB.',

    'suc_add_cart': 'Книга "{}" успешно добавлена в корзину!',
    'suc_filter_authors': 'Вам будут показаны книги следующих авторов:\n\n{}\nВы можете продолжить выбор,'
                          'или нажать "Вернуться назад".',
    'suc_filter_categories': 'Вам будут показаны книги следующих жанров:\n\n{}\nВы можете продолжить выбор,'
                          'или нажать "Вернуться назад".',

    'suc_admin_author': 'Автор успешно добавлен, вы возвращены в панель администратора.',
    'suc_admin_category': 'Категория успешно добавлена, вы возвращены в панель администратора.',
    'suc_admin_book_photo': 'Фотография добавлена. Выберите автора из списка.',
    'suc_admin_book_author': 'Автор добавлен. Выберите категорию из списка.',
    'suc_admin_book_category': 'Категория добавлена.\n\nВведите название книги (до 256 символов).',
    'suc_admin_book_name': 'Название добавлено.\n\nВведите описание книги (до 512 символов).',
    'suc_admin_book_description': 'Описание добавлено.\n\nВведите название цену.',
    'suc_admin_book_price': 'Цена добавлена.',
    'suc_admin_book': 'Книга успешно создана! Вы возвращены в панель администратора',
    'suc_buy': 'Покупка совершена! Свои заказы можно посмотреть в главном меню.',

    'kb_back': 'Вернуться назад',

    'kb_main_1': 'Статистика',
    'kb_main_2': 'Заказы',
    'kb_main_3': 'Корзина',
    'kb_main_4': 'Каталог',

    'kb_cart_1': 'Купить',
    'kb_book_1': 'Добавить в корзину',

    'kb_admin_1': '+ книга',
    'kb_admin_2': '+ категория',
    'kb_admin_3': '+ автор',

}
