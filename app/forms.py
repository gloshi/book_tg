from aiogram.dispatcher.filters.state import State, StatesGroup


# States
class Form(StatesGroup):
    main = State()
    main_catalog = State()
    main_cart = State()

    catalog_filters = State()
    catalog_filter = State()
    catalog_search = State()

    admin = State()
    admin_book = State()
    admin_book_photo = State()
    admin_category = State()
    admin_author = State()
