import os
import shutil
import sys
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

    @patch('handlers.handler.Handler.get_date')
    @patch('handlers.handler.Handler.get_category_menu')
    @patch('handlers.handler.Handler.get_value')
    @patch('handlers.handler.Handler.get_description')
    @patch.object(Balance, 'add_action')
    @patch('builtins.print')
    @patch.object(AdvancedHandler, 'show_balance')
    def test_add_action(
        self, mock_show_balance, mock_print, mock_add_action,
        mock_get_description, mock_get_value, mock_get_category_menu,
        mock_get_date
    ):
        mock_get_date.return_value = date(2024, 5, 1)
        mock_get_category_menu.return_value = 'Category'
        mock_get_value.return_value = 100
        mock_get_description.return_value = 'Description'
        mock_add_action.return_value = 'Added Action'
        mock_show_balance.return_value = None

        self.handler.add_action()

        mock_add_action.assert_called_once_with({
            'date': date(2024, 5, 1),
            'category': 'Category',
            'value': 100,
            'description': 'Description'
        })
        print_calls = [
            call(cf.ACTION_ADDED),
            call('Added Action')
        ]
        mock_print.assert_has_calls(print_calls)
        mock_show_balance.assert_called_once()

    @patch('builtins.input', side_effect=['\n'])
    def test_show_balance(self, mock_input):
        with patch('builtins.print') as mock_print:
            self.handler.show_balance()
            expected_calls = [
                call(f'\n{cf.CURRENT_BALANCE}0\n'),
                call()
            ]
            mock_print.assert_has_calls(expected_calls)

    @patch('builtins.input', side_effect=['Нет'])
    @patch('sys.exit')
    def test_to_exit_without_saving(self, mock_exit, mock_input):
        self.handler.to_exit()
        mock_exit.assert_called_once()

    @patch('builtins.input', side_effect=['any_string'])
    @patch('sys.exit')
    @patch.object(AdvancedHandler, 'save')
    def test_to_exit_with_saving(self, mock_save, mock_exit, mock_input):
        self.handler.to_exit()
        mock_save.assert_called_once()
        mock_exit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
