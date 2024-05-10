from config import config as cf
from managers.data_managers import Balance


def main() -> None:
    balance = Balance(cf.DATA_PATH)
    menu = AdvancedMenu(balance)
    menu.start()


if __name__ == '__main__':
    main()
