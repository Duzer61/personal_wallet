import os
import shutil
import unittest
from copy import deepcopy
from datetime import date
from unittest.mock import call, patch

from config import config as cf
from handlers.advanced_handler import AdvancedHandler
from managers.data_managers import Action, Balance


class TestHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'temp'
        cls.test_file = os.path.join(cls.test_dir, 'test.json')

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    def setUp(self):
        self.balance = Balance(self.test_file)
        self.balance.actions = [
            Action(
                date=date(2024, 5, 1), category='Доход',
                value=100_000, description='Test income'
            ),
            Action(
                date=date(2024, 5, 2), category='Расход',
                value=10_000, description='Test spending'
            ),
            Action(
                date=date(2024, 5, 3), category='Доход',
                value=5_000, description='Test income 2'
            ),
            Action(
                date=date(2024, 5, 4), category='Расход',
                value=1_000, description='Test spending 2'
            ),
        ]
        self.balance.balance = 94_000.0
        self.handler = AdvancedHandler(self.balance)

    @patch('builtins.input', side_effect=['1', '2'])
    def test_get_category_menu(self, mock_input):
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
                call(f'\n{cf.CURRENT_BALANCE}94000.0\n'),
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

    @patch(
        'handlers.advanced_handler.AdvancedHandler.get_category_menu',
        side_effect=['Доход', 'Расход']
    )
    def test_search_by_category(self, mock_get_category_menu):
        expected_categories = ['Доход', 'Расход']
        for counter, category in enumerate(expected_categories):
            result = self.handler.search_by_category()
            self.assertEqual(len(result), 2)
            self.assertIn(self.handler.balance.actions[counter], result)
            self.assertIn(self.handler.balance.actions[counter + 2], result)

            categories = [action.category for action in result]
            self.assertIn(category, categories)
            unexpected_category = 'Расход' if category == 'Доход' else 'Доход'
            self.assertNotIn(unexpected_category, categories)

    @patch(
        'handlers.advanced_handler.AdvancedHandler.get_value',
        side_effect=[100_000.0]
    )
    def test_search_by_value(self, mock_get_value):
        result = self.handler.search_by_value()
        self.assertEqual(len(result), 1)
        self.assertIn(self.handler.balance.actions[0], result)

    @patch(
        'handlers.advanced_handler.AdvancedHandler.get_date',
        side_effect=[date(2024, 5, 1)]
    )
    def test_search_by_date(self, mock_get_date):
        result = self.handler.search_by_date()
        self.assertEqual(len(result), 1)
        self.assertIn(self.handler.balance.actions[0], result)

    @patch(
        'handlers.advanced_handler.AdvancedHandler.get_date',
        side_effect=[date(2024, 5, 1), date(2024, 5, 3)]
    )
    def test_search_by_period(self, mock_get_date):
        result = self.handler.search_by_period()
        self.assertEqual(len(result), 3)
        for action in self.handler.balance.actions[:3]:
            self.assertIn(action, result)
        self.assertNotIn(self.handler.balance.actions[3], result)

    @patch(
        'handlers.advanced_handler.AdvancedHandler.get_category_menu',
        side_effect=['Доход', 'Расход']
    )
    def test_edit_category(self, mock_get_category_menu):
        edit_action = self.handler.balance.actions[1]

        self.handler.edit_category(edit_action)
        self.assertEqual(edit_action.category, 'Доход')
        self.assertEqual(self.handler.balance.balance, 114_000.0)

        self.handler.edit_category(edit_action)
        self.assertEqual(edit_action.category, 'Расход')
        self.assertEqual(self.handler.balance.balance, 94_000.0)

    @patch(
        'handlers.advanced_handler.AdvancedHandler.get_value',
        side_effect=[2000.0, 6000.0]
    )
    def test_edit_value(self, mock_get_value):
        edit_action = self.handler.balance.actions[3]
        self.handler.edit_value(edit_action)
        self.assertEqual(edit_action.value, 2000.0)
        self.assertEqual(self.handler.balance.balance, 93_000.0)

        edit_action = self.handler.balance.actions[2]
        self.handler.edit_value(edit_action)
        self.assertEqual(edit_action.value, 6000.0)
        self.assertEqual(self.handler.balance.balance, 94_000.0)

    @patch('builtins.input', side_effect=['\n', '\n'])
    def test_delete_action(self, mock_input):
        edit_action = self.handler.balance.actions[3]
        selected_actions = self.handler.balance.actions[1:4:2]

        self.handler.delete_action(edit_action, selected_actions)
        self.assertEqual(len(self.handler.balance.actions), 3)
        self.assertEqual(len(selected_actions), 1)
        self.assertNotIn(edit_action, self.handler.balance.actions)
        self.assertNotIn(edit_action, selected_actions)
        self.assertEqual(self.handler.balance.balance, 95_000.0)

        edit_action = self.handler.balance.actions[2]
        selected_actions = self.handler.balance.actions[:3:2]

        self.handler.delete_action(edit_action, selected_actions)
        self.assertEqual(self.handler.balance.balance, 90_000.0)


if __name__ == '__main__':
    unittest.main()
