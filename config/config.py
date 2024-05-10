DATA_PATH = 'data/balance.json'  # путь к файлу с данными


# Меню
START_MENU = [
    '\nЭто главное меню. Выберите действие: \n',
    '1. Добавить запись',
    '2. Показать текущий баланс',
    '3. Показать сумму всех доходов',
    '4. Показать сумму всех расходов',
    '5. Поиск записей и редактирование',
    '6. Сохранить изменения',
    '7. Выход'
]

SEARCH_MENU = [
    '\nЭто меню поиска. Выберите действие: \n',
    '1. Поиск по категории',
    '2. Поиск по сумме',
    '3. Поиск по дате',
    '4. Возврат в главное меню'
]

EDIT_MENU = [
    '\nВыберите действие: \n',
    '1. Изменить дату',
    '2. Изменить категорию',
    '3. Изменить сумму',
    '4. Изменить описание',
    '5. Удалить запись',
    '6. Назад'
]

DELETE_MENU = [
    '\nВы действительно хотите удалить выбранную запись?\n',
    '1. Да',
    '2. Нет, вернуться в меню редактирования'
]

SELECT_AND_EDIT_MENU = (
    '\nВыберете номер записи для редактирования '
    'или введите 0 для возврата\n'
)

SELECT_CATEGORY = [
    'Выберете категорию: \n',
    '1. Доход',
    '2. Расход'
]

INPUT_DATE_OR_PERIOD = [
    '\nПровести поиск по конкретной дате дате или за период?\n',
    '1. Дата',
    '2. Период',
    '3. Возврат в меню поиска'
]


# Описания для ввода данных
SELECT_NUMBER = 'Выберите номер: '
INPUT_VALUE = 'Введите сумму: '
INPUT_DATE = (
    'Введите дату в формате ГГГГ-ММ-ДД или нажмите Enter '
    'для выбора текущей даты.\n'
    'Дата: '
)
QUESTION_TO_EXIT = (
    'Чтобы сохранить изменения и выйти нажмите Enter.\n'
    'Чтобы выйти без сохранения введите "Нет"'
)
INPUT_DESCRIPTION = 'Введите описание: '
INPUT_DATE_FROM = '\nВведите начальную дату:\n'
INPUT_DATE_TO = '\nВведите конечную дату:\n'


# Информационные сообщения
ACTION_ADDED = '\nЗапись добавлена.'
CURRENT_BALANCE = 'Текущий баланс: '
INCOMES = 'Сумма всех доходов: '
EXPENSES = 'Сумма всех расходов: '
WAIT_FOR_ENTER = 'Нажмите Enter для возврата в главное меню.'
CHANGES_SAVED = '\nИзменения сохранены.'
EXITED = '\nВы вышли из программы.'
FOUND = '\nНайденные записи:\n'
NO_FOUND = '\nНичего не нашлось.\n'
ACTION_EDIT_SELECTED = 'Для редактирования выбрана запись:\n'
ACTION_DELETED = 'Запись удалена. Нажмите Enter для возврата '


# Сообщения об ошибках
INCORRECT_INPUT = '\nНекорректный ввод, попробуйте еще раз. \n'
INCORRECT_DATE = '\nДата не должна быть больше текущей.\n'
INCORRECT_VALUE = (
    '\nИспользуйте только цифры и точку. '
    'Сумма должна не должна быть отрицательной. '
    'Максимально допускается два знака после точки\n'
)
