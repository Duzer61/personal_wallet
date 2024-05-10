import json
import os
from dataclasses import dataclass
from datetime import date


@dataclass
class Action:
    """
    Класс для хранения информации о транзакциях (доходах и расходах).
    """
    date: date
    category: str
    value: float
    description: str

    def __str__(self):
        return (
            f'Дата: {self.date},\n'
            f'Категория: {self.category},\n'
            f'Сумма: {self.value},\n'
            f'Описание: {self.description}'
        )


class Balance:
    """
    Класс для хранения списка транзакций и состояния баланса.
    """
    def __init__(self, path: str) -> None:
        self.path = path
        self.actions: list[Action] = []
        self.balance: int | float = 0
        self.load()

    def load(self) -> None:
        """
        Загружает список транзакций из файла, считает баланс.
        """
        if not os.path.exists(self.path):
            print('Файл отсутствует. Создаю.')
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            self.save()
            return
        else:
            print('Есть файл. Читаю.')
            with open(self.path, 'r') as f:
                temp = json.load(f)
                for action in temp:
                    action['date'] = date.fromisoformat(action['date'])
                    if action['category'] == 'Доход':
                        self.balance += action['value']
                    else:
                        self.balance -= action['value']
                    self.actions.append(Action(**action))

    def save(self) -> None:
        """
        Сохраняет список транзакций в файл.
        """
        with open(self.path, 'w') as f:
            temp = []
            for action in self.actions:
                action_dict = action.__dict__.copy()
                action_dict['date'] = str(action.date)
                temp.append(action_dict)
            json.dump(temp, f)

    def add_action(self, data: dict) -> Action | None:
        """
        Добавляет новую транзакцию в список.
        """
        try:
            action = Action(**data)
            self.actions.append(action)
            if action.category == 'Доход':
                self.balance += action.value
            else:
                self.balance -= action.value
            return action
        except Exception as e:
            print(f'Ошибка при добавлении транзакции: {e}')
            return None

    def print_all(self) -> None:
        """
        Выводит все транзакции и баланс в консоль.
        """
        for action in self.actions:
            print(action)
            print()
        print(f'Баланс: {self.balance}')

    def get_incomes(self) -> float:
        """
        Возвращает сумму всех доходов.
        """
        return sum(
            action.value for action in self.actions
            if action.category == 'Доход'
        )

    def get_expenses(self) -> float:
        """
        Возвращает сумму всех расходов.
        """
        return sum(
            action.value for action in self.actions
            if action.category == 'Расход'
        )

    def __str__(self):
        """
        Возвращает баланс в виде строки.
        """
        return str(self.balance)
