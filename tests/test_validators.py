import unittest
from datetime import date, timedelta

from validators.validators import (validate_choice, validate_date,
                                   validate_value)


class TestValidateChoice(unittest.TestCase):
    def test_valid_choice(self):
        self.assertEqual(validate_choice('1', 10), 1)
        self.assertEqual(validate_choice('10', 11), 10)
        self.assertEqual(validate_choice('5', 6, False), 5)

    def test_invalid_choice(self):
        self.assertFalse(validate_choice('0', 10))
        self.assertFalse(validate_choice('11', 10))
        self.assertFalse(validate_choice('a', 10,))

    def test_back_flag(self):
        self.assertEqual(validate_choice('0', 10, False), 'back')


class TestValidateDate(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(validate_date(''), date.today())

    def test_valid_date(self):
        self.assertEqual(validate_date('2024-05-01'), date(2024, 5, 1))
        self.assertEqual(validate_date('2024-02-29'), date(2024, 2, 29))

    def test_invalid_date(self):
        self.assertFalse(validate_date('2024-13-01'))
        self.assertFalse(validate_date('2024-02-30'))
        self.assertFalse(validate_date('2023-02-29'))

    def test_future_date(self):
        future_date = date.today() + timedelta(days=1)
        self.assertFalse(validate_date(future_date.isoformat()))


class TestValidateValue(unittest.TestCase):
    def test_valid_value(self):
        self.assertEqual(validate_value('10.0'), 10.0)
        self.assertEqual(validate_value('0.01'), 0.01)
        self.assertEqual(validate_value('1000000'), 1000000.00)

    def test_invalid_value(self):
        self.assertFalse(validate_value('-10'))
        self.assertFalse(validate_value('abc'))
        self.assertFalse(validate_value('10.000'))
        self.assertFalse(validate_value('10.00000'))
        self.assertFalse(validate_value('10.0.0'))


if __name__ == '__main__':
    unittest.main()
