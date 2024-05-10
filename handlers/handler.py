import os
import sys
from datetime import date

from config import config as cf
from managers.data_managers import Action, Balance
from validators.validators import (validate_choice, validate_date,
                                   validate_value)


class Handler:
    """
    Основной класс для взаимодействия с пользователем
    и управления действиями приложения.
    """

    def __init__(self, balance: Balance) -> None:
        self.balance = balance
        self.clear_screen()

    def start(self) -> None:
        """
        Стартовое меню. Запускает основной цикл программы.
        """
        while True:
            choice: int = self.make_choice(cf.START_MENU)
            func_names: dict[int, str] = {
                1: 'add_action',
                2: 'show_balance',
                3: 'show_incomes',
                4: 'show_expenses',
                5: 'search_menu',
                6: 'save',
                7: 'to_exit',
            }
            func_name: str = func_names[choice]
            func = getattr(self, func_name, None)
            if func:
                func()

    def search_menu(self) -> None:
        """
        Меню поиска.
        """
        pass

    def get_category_menu(self) -> str:
        """
        Служит для выбора пользователем категории. Валидирует ввод
        и возвращает категорию транзакции (Доход или Расход).
        """

        choice: int = self.make_choice(cf.SELECT_CATEGORY)
        category: str = 'Доход' if choice == 1 else 'Расход'
        return category

    def add_action(self) -> None:
        """
        Управляет добавлением транзакции. Запрашивает у пользователя
        данные о транзакции и добавляет ее в баланс.
        """

        data: dict = {}
        data['date'] = self.get_date()
        data['category'] = self.get_category_menu()
        data['value'] = self.get_value()
        data['description'] = self.get_description()
        action: Action | None = self.balance.add_action(data)
        if action:
            print(cf.ACTION_ADDED)
            print(action)
            self.show_balance()
        return

    def get_date(self) -> date:
        """
        Служит для ввода пользователем даты. Валидирует ввод
        и возвращает дату. Выбор по умолчанию -> текущая дата.
        """

        text_date: bool | str | date = False
        while not isinstance(text_date, date):
            text_date = input(cf.INPUT_DATE)
            text_date = validate_date(text_date)
        return text_date

    def get_value(self) -> float:
        """
        Служит для ввода пользователем суммы. Валидирует ввод.
        Сумма должна быть неотрицательным целым или десятичным
        числом с максимально двумя знаками после точки.
        """

        value: bool | str | float = False
        while not isinstance(value, float):
            value = input(cf.INPUT_VALUE)
            value = validate_value(value)
        return value

    def get_description(self) -> str:
        """
        Служит для ввода пользователем описания.
        """
        return input(cf.INPUT_DESCRIPTION)

    def show_balance(self) -> None:
        """
        Выводит текущий баланс.
        """

        print(f'\n{cf.CURRENT_BALANCE}{self.balance}\n')
        self.wait_for_enter()

    def show_incomes(self) -> None:
        """
        Выводит сумму всех доходов.
        """

        print(f'\n{cf.INCOMES}{self.balance.get_incomes()}\n')
        self.wait_for_enter()

    def show_expenses(self) -> None:
        """
        Выводит сумму всех расходов.
        """

        print(f'\n{cf.EXPENSES}{self.balance.get_expenses()}\n')
        self.wait_for_enter()

    def wait_for_enter(self) -> None:
        """
        Ожидает нажатия Enter для возврата.
        """

        input(cf.WAIT_FOR_ENTER)
        print()
        self.clear_screen()

    def to_exit(self) -> None:
        """
        Выход из программы с возможностью сохранения изменений.
        """

        print(cf.QUESTION_TO_EXIT)
        if input().lower() != 'нет':
            self.save()
        print(cf.EXITED)
        sys.exit()

    def save(self) -> None:
        """
        Сохраняет данные в файл.
        """

        self.balance.save()
        print(cf.CHANGES_SAVED)

    def make_choice(self, menu_list: list) -> int:
        """
        Возвращает выбранное пользователем значение (номер пункта меню).
        """

        choice: bool | str | int = False
        while not choice:
            for i in menu_list:
                print(i)
            choice = input(cf.SELECT_NUMBER)
            choice = validate_choice(choice, len(menu_list))
        return int(choice)

    def clear_screen(self) -> None:
        """
        Очищает экран.
        """
        os.system('clear')
