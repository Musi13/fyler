import logging
import sys
from argparse import ArgumentParser
from fyler.application import FylerApp
from fyler.utils import popup_excepthook


def parse_args():
    parser = ArgumentParser(
        description='A GUI tool to bulk rename files based on metadata from web databases'
    )
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    sys.excepthook = popup_excepthook
    app = FylerApp(sys.argv)
    app.open_main_window()
    app.exec_()


if __name__ == '__main__':
    main()
