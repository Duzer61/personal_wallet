from datetime import date

from config import config as cf


def validate_choice(
        choice: str, max_choice: int, ignore_zero: bool = True
        ) -> bool | int | str:
    """
    Проверяет ввод пользователя на корректность в стартовом меню.
    Возвращает число в диапазоне от 1 до max_choice или False или 'back'
    в качестве флага для возврата в предыдущее меню.
    """

    if choice.isdigit() and int(choice) in range(ignore_zero, max_choice):
        return 'back' if choice == '0' else int(choice)
    print(cf.INCORRECT_INPUT)
    return False


def validate_date(text_date: str) -> date | bool:
    """
    Проверяет ввод пользователя на корректность в меню с выбором даты.
    Возвращает дату или False.
    """

    current_date = date.today()
    if text_date == '':
        return current_date
    try:
        validated_date: date = date.fromisoformat(text_date)
    except ValueError:
        print(cf.INCORRECT_INPUT)
        return False
    if validated_date > current_date:
        print(cf.INCORRECT_DATE)
        return False
    return validated_date


def validate_value(text_value: str) -> float | bool:
    """
    Проверяет ввод пользователя на корректность в меню с выбором суммы.
    Возвращает сумму или False.
    """

    try:
        value: float = float(text_value)
        if value < 0:
            print(cf.INCORRECT_VALUE)
            return False
    except ValueError:
        print(cf.INCORRECT_VALUE)
        return False
    if '.' in text_value:
        if len(text_value.split('.')[1]) > 2:
            print(cf.INCORRECT_VALUE)
            return False
    return value
