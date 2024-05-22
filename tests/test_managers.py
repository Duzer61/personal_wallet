import os
import shutil
import unittest
from datetime import date

from managers.data_managers import Action, Balance


class TestFinance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'temp'
        cls.test_file = os.path.join(cls.test_dir, 'test.json')
        cls.balance = Balance(cls.test_file)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    def test_action_str(self):
        action = Action(date(2024, 5, 21), 'Доход', 1000, 'Зарплата')
        expected_str = (
            "Дата: 2024-05-21,\n"
            "Категория: Доход,\n"
            "Сумма: 1000,\n"
            "Описание: Зарплата"
        )
        self.assertEqual(str(action), expected_str)

    def test_balance(self):
        data = {
            'date': date(2024, 5, 21),
            'category': 'Доход',
            'value': 1000,
            'description': 'Зарплата'
        }
        self.balance.add_action(data)
        self.assertEqual(self.balance.get_incomes(), 1000)
        self.assertEqual(self.balance.get_expenses(), 0)
        self.assertEqual(str(self.balance), '1000')

    def test_save_and_load(self):
        data = {
            'date': date(2024, 5, 21),
            'category': 'Расход',
            'value': 500,
            'description': 'Покупка продуктов'
        }
        self.balance.add_action(data)
        self.balance.save()

        new_balance = Balance(self.test_file)
        self.assertEqual(new_balance.get_incomes(), 1000)
        self.assertEqual(new_balance.get_expenses(), 500)
        self.assertEqual(str(new_balance), '500')


if __name__ == '__main__':
    unittest.main()
