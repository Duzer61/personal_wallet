# Проект "Персональный финансовый кошелек". Написан в качестве тестового задания.
### [Описание задания](https://docs.google.com/document/d/1kO7PizgRuTbmiMbi5JHu35icU_UDp5_e09dBcUTz7PE/edit?usp=sharing)
_____________
## Описание проекта.
В соответствие с ТЗ проект представляет собой консольное приложение для учета личных доходов и расходов.

 - Проект написан на Python 3.12 (будет работать начиная от версии 3.10 +)
 - В проекте не использовались дополнительные библиотеки или фреймворки, поэтому в установке виртуальной среды (venv) нет необходимости
 - Для запуска приложения необходимо запустить файл `main.py` командой `python3 main.py` или через интерфейс IDE
 - Сохранение данных реализовано в json-файл. Имя файла и путь к нему задается в константе `DATA_PATH`, в файле `config.py`. Если на момент запуска такой файл отсутствует, то он создается автоматически. Если файл с данными уже создан, то данные из него загружаются в память.
 - Реализована валидация вводимых пользователем данных: 
Даты вводятся в формате ГГГГ-ММ-ДД, если не вводить дату, а нажать Enter, то автоматически применяется текущая дата. Суммы в виде целого неотрицательного числа или десятичной дроби с максимум двумя знаками после точки. Выбор пунктов меню - только целыми числами. В случае некорректно введенных данных - программа сообщает об этом и предлагает ввести данные заново.

### Описание интерфейса
После запуска программы пользователь попадает в основное меню

**Пункты меню:**
1. Добавить запись - служит для добавления записи дохода или расхода
2. Показывает сумму текущего баланса
3. Показывает сумму всех доходов
4. Показывает сумму всех расходов
5. Открывает меню поиска и редактирования записей
6. Сохраняет изменений в файл
7. Выход из программы. При выходе предлагается сохранить изменения (действие по умолчанию) или отказаться от сохранения.
______________

**Меню поиска записей**

1. Поиск по категории ("Доход" или "Расход")
2. Поиск по сумме
3. Поиск по дате (можно произвести поиск за конкретную дату или за период от и до включительно.
4. Возврат в главное меню

После поиска найденные записи выводятся в пронумерованном списке и пользователю предлагается выбрать номер записи для редактирования или вернуться назад к списку найденных записей.

**Меню редактирования записи**

1. Изменить дату
2. Изменить категорию
3. Изменить сумму
4. Изменить описание
5. Удалить запись
6. Назад

При изменении категории, суммы или удалении записи баланс автоматически пересчитывается.
Если пользователь хочет удалить запись, то перед удалением запрашивается подтверждение.

_______
  ##  Автор
Данил Кочетов - [GitHub](https://github.com/Duzer61)