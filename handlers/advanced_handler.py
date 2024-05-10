from config import config as cf
from handlers.handler import Handler, date, validate_choice


class AdvancedHandler(Handler):
    """
    Класс расширенного меню с поиском и редактированием.
    """

    def search_menu(self) -> None:
        """
        Меню поиска.
        Предлагает пользователю выполнить поиск по различным критериям.
        1. Поиск по категории
        2. Поиск по сумме
        3. Поиск по дате или периоду
        4. Вернуться в главное меню
        После выбора варианта пользователь может выбрать и отредактировать
        конкретные действия, найденные по выбранному критерию.
        """
        while True:
            choice: int = self.make_choice(cf.SEARCH_MENU)
            match choice:
                case 1:
                    selected_actions = self.search_by_category()
                case 2:
                    selected_actions = self.search_by_value()
                case 3:
                    selected_actions = self.date_or_period_menu()
                case 4:
                    self.clear_screen()
                    return
            self.clear_screen()
            if not selected_actions:
                print(cf.NO_FOUND)
                continue
            selected_actions.sort(key=lambda x: x.date)
            self.select_and_edit_menu(selected_actions)

    def select_and_edit_menu(self, selected_actions) -> None:
        """
        Меню выбора и редактирования записи.
        Отображает список найденных записей и позволяет пользователю выбрать
        одну из них для редактирования, либо вернуться в меню поиска.
        """
        while True:
            self.clear_screen()
            self.show_selected_actions(selected_actions)
            print(cf.SELECT_AND_EDIT_MENU)
            choice: bool | str | int = False
            while not choice:
                choice = input(cf.SELECT_NUMBER)
                choice = validate_choice(
                    choice, len(selected_actions) + 1, ignore_zero=False
                )
                if choice == 'back':
                    self.clear_screen()
                    return
            edit_action = selected_actions[int(choice) - 1]
            self.edit_menu(edit_action, selected_actions)

    def edit_menu(self, edit_action, selected_actions) -> None:
        """
        Меню редактирования записи.
        Отображает выбранную запись и позволяет пользователю редактировать
        ее данные или удалить запись, либо вернуться к найденным записям.
        """

        while True:
            deleted = False  # Флаг, который показывает, удалена ли запись
            self.clear_screen()
            print(cf.ACTION_EDIT_SELECTED)
            print(edit_action)
            choice: int = self.make_choice(cf.EDIT_MENU)
            match choice:
                case 1:
                    self.edit_date(edit_action)
                case 2:
                    self.edit_category(edit_action)
                case 3:
                    self.edit_value(edit_action)
                case 4:
                    self.edit_description(edit_action)
                case 5:
                    deleted = self.delete_action_menu(
                        edit_action, selected_actions
                    )
                case 6:
                    return
            if deleted:
                return

    def date_or_period_menu(self) -> list:
        """
        Выбор типа поиска по дате (дата или период).
        """
        while True:
            choice: int = self.make_choice(cf.INPUT_DATE_OR_PERIOD)
            match choice:
                case 1:
                    selected_actions = self.search_by_date()
                case 2:
                    selected_actions = self.search_by_period()
                case 3:
                    return []
            return selected_actions

    def search_by_category(self) -> list:
        """
        Поиск по категории.
        """

        category: str = self.get_category_menu()
        selected_actions: list = []
        for action in self.balance.actions:
            if action.category == category:
                selected_actions.append(action)
        return selected_actions

    def search_by_value(self) -> list:
        """
        Поиск по сумме.
        """

        value: float = self.get_value()
        selected_actions: list = []
        for action in self.balance.actions:
            if action.value == value:
                selected_actions.append(action)
        return selected_actions

    def search_by_date(self) -> list:
        """
        Поиск по дате.
        """

        selected_date: date = self.get_date()
        selected_actions: list = []
        for action in self.balance.actions:
            if action.date == selected_date:
                selected_actions.append(action)
        return selected_actions

    def search_by_period(self) -> list:
        """
        Поиск по периоду (включая начало и конец периода).
        """

        print(cf.INPUT_DATE_FROM)
        start_date: date = self.get_date()
        print(cf.INPUT_DATE_TO)
        end_date: date = self.get_date()
        selected_actions: list = []
        for action in self.balance.actions:
            if start_date <= action.date <= end_date:
                selected_actions.append(action)
        return selected_actions

    def show_selected_actions(self, selected_actions) -> None:
        """
        Вывод выбранных записей на экран.
        """
        print(cf.FOUND)
        for num, action in enumerate(selected_actions):
            print(f'{num + 1}. {action}')
            print('----------------')

    def edit_date(self, edit_action) -> None:
        """
        Редактирует дату.
        """
        edit_action.date = self.get_date()
        return

    def edit_category(self, edit_action) -> None:
        """
        Редактирует категорию и пересчитывает баланс если категория поменялась.
        """
        old_category = edit_action.category
        edit_action.category = self.get_category_menu()
        if edit_action.category == old_category:
            return
        if old_category == 'Доход':
            self.balance.balance -= edit_action.value * 2
        else:
            self.balance.balance += edit_action.value * 2
        return

    def edit_value(self, edit_action) -> None:
        """
        Редактирует сумму и пересчитывает баланс.
        """
        old_value = edit_action.value
        edit_action.value = self.get_value()
        difference = edit_action.value - old_value
        if edit_action.category == 'Доход':
            self.balance.balance += difference
        else:
            self.balance.balance -= difference
        return

    def delete_action_menu(self, edit_action, selected_actions) -> bool:
        """
        Меню удаления записи. Запрашивает подтверждение у пользователя
        и в случае подтверждения удаляет запись.
        """
        while True:
            choice: int = self.make_choice(cf.DELETE_MENU)
            match choice:
                case 1:
                    self.delete_action(edit_action, selected_actions)
                    return True
                case 2:
                    return False

    def delete_action(self, edit_action, selected_actions) -> None:
        """
        Удаляет выбранную запись, пересчитывает баланс.
        """

        if edit_action.category == 'Доход':
            self.balance.balance -= edit_action.value
        else:
            self.balance.balance += edit_action.value
        selected_actions.remove(edit_action)
        self.balance.actions.remove(edit_action)
        self.clear_screen()
        input(cf.ACTION_DELETED)
        return

    def edit_description(self, edit_action) -> None:
        """
        Редактирует описание.
        """
        edit_action.description = self.get_description()
        return
