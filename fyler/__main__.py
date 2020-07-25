import logging
import sys
from fyler.application import FylerApp


def main():
    logging.basicConfig(level=logging.INFO)
    app = FylerApp(sys.argv)
    app.open_main_window()
    app.exec_()


if __name__ == '__main__':
    main()
