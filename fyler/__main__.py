import sys
from PyQt5.QtWidgets import QMainWindow
from fyler.application import FylerApp

def main():
    app = FylerApp(sys.argv)
    app.open_main_window()
    app.exec_()

if __name__ == '__main__':
    main()
