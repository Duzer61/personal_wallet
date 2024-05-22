import os
import shutil
import unittest
from datetime import date
from unittest.mock import call, patch

from config import config as cf
from handlers.advanced_handler import AdvancedHandler
from managers.data_managers import Balance


class TestHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаем экземпляр Handler для тестирования
        cls.test_dir = 'temp'
        cls.test_file = os.path.join(cls.test_dir, 'test.json')
        cls.balance = Balance(cls.test_file)
        cls.handler = AdvancedHandler(cls.balance)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    @patch('builtins.input', side_effect=['1', '2'])
    def test_get_category_menu(self, mock_input):
        # Проверяем, что метод get_category_menu возвращает ожидаемую категорию
        self.assertEqual(self.handler.get_category_menu(), 'Доход')
        self.assertEqual(self.handler.get_category_menu(), 'Расход')

    @patch('builtins.input', side_effect=['100'])
    def test_get_value(self, mock_input):
        value = self.handler.get_value()
        self.assertIsInstance(value, float)
        self.assertEqual(value, 100.0)

    @patch('builtins.input', side_effect=['2024-05-01'])
    def test_get_date(self, mock_input):
        check_date = self.handler.get_date()
        self.assertIsInstance(check_date, date)
        self.assertEqual(check_date, date(2024, 5, 1))

    # @patch('builtins.print')
    # def test_show_balance(self, mock_print):
    #     self.handler.show_balance()
    #     mock_print.assert_called_with(f'\n{cf.CURRENT_BALANCE}0\n')
    @patch('builtins.input', side_effect=['\n'])
    def test_show_balance(self, mock_input):
        with patch('builtins.print') as mock_print:
            self.handler.show_balance()
            expected_calls = [
                call(f'\n{cf.CURRENT_BALANCE}0\n'),
                call()
            ]
            mock_print.assert_has_calls(expected_calls)


if __name__ == '__main__':
    unittest.main()
