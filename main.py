from config import config as cf
from handlers.advanced_handler import AdvancedHandler
from managers.data_managers import Balance


def main() -> None:
    balance = Balance(cf.DATA_PATH)
    menu = AdvancedHandler(balance)
    menu.start()


if __name__ == '__main__':
    main()
