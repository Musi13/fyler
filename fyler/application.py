from PyQt5.QtWidgets import QApplication
from fyler.views.main_window import MainWindow


class FylerApp(QApplication):
    def __init__(self, args_raw):
        super().__init__(args_raw)

    def open_main_window(self):
        self.main_window = MainWindow(self)
        self.main_window.show()
        self.main_window.raise_()
