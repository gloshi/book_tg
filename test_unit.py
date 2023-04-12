import asyncio
import unittest

from app.handlers.main import main, main_cart


class MessageFromUser(object):
    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])


class Message(object):
    async def reply(self, text, reply_markup):
        pass

    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])


class TestCalc(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_message_error(self):
        message = Message({"from_user": MessageFromUser({'id': 5139217847}),
                           "text": "hi"})
        result = self.loop.run_until_complete(main(message=message))

        self.assertEqual(result, 'Неправильный ввод, повторите попытку.')

    def test_message_add_cart(self):
        message = Message({"from_user": MessageFromUser({'id': 5139217847}),
                           "text": "Каталог"})
        result = self.loop.run_until_complete(main(message=message))

        self.assertEqual(result, 'Вы успешно перешли в каталог книг. Вы можете использовать фильтры.')

    def test_buy(self):
        message = Message({"from_user": MessageFromUser({'id': 5139217847}),
                           "text": "Купить"})
        result = self.loop.run_until_complete(main_cart(message=message))

        self.assertEqual(result, 'Покупка совершена! Свои заказы можно посмотреть в главном меню.')

    def test_stats(self):
        message = Message({"from_user": MessageFromUser({'id': 5139217847}),
                           "text": "Статистика"})
        result = self.loop.run_until_complete(main(message=message))

        self.assertEqual(result, 'Статистика аккаунта №4:\n'
                                 '- ID пользователя: 5139217847\n- Имя: Александр\n- Фамилия: Комаров\n- Дата регистрации: 2022-04-16 20:47:56.115784\n- Администратор: Да\n\n- Книг в корзине: 0\n- Заказов: 3 (на сумму 2388 RUB)')


if __name__ == "__main__":
    unittest.main()
