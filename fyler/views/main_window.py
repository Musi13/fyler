import os
from pathlib import Path
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QLabel, QMainWindow, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt

from fyler import utils
from fyler.providers import anilist
from fyler.utils import listwidget_text_items, listwidget_item
from fyler.views.search_window import SearchWindow

uifile = (Path(__file__) / '../../assets/ui/mainwindow.ui').resolve()
MainWindowUI, MainWindowBase = uic.loadUiType(uifile)

def choose_sources_dialog(parent, title, directory=True):
    options = QFileDialog.Options()
    if directory:
        options |= QFileDialog.ShowDirsOnly
    dialog = QFileDialog(parent, title, os.path.expanduser('~'), options=options)
    dialog.setFileMode(QFileDialog.Directory if directory else QFileDialog.ExistingFiles)
    dialog.setParent(parent, QtCore.Qt.Sheet)
    return dialog

def search_dialog(parent, default=''):
    dialog = QInputDialog(parent)
    dialog.setWindowTitle('Search')
    dialog.setInputMode(QInputDialog.TextInput)
    dialog.setTextValue(default)
    dialog.setOkButtonText('Search')
    dialog.setParent(parent, QtCore.Qt.Sheet)
    return dialog

class MainWindow(MainWindowUI, MainWindowBase):


    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.folderButton.clicked.connect(lambda: self.add_sources(directory=True))
        self.filesButton.clicked.connect(lambda: self.add_sources(directory=False))

        self.matchButton.clicked.connect(self.match_sources)
        self.actionButton.clicked.connect(self.process_action)

        # self.setWindowTitle("Fyler")

        # label = QLabel("This is a PyQt5 window!")

        # # The `Qt` namespace has a lot of attributes to customise
        # # widgets. See: http://doc.qt.io/qt-5/qt.html
        # label.setAlignment(Qt.AlignCenter)

        # # Set the central widget of the Window. Widget will expand
        # # to take up all the space in the window by default.
        # self.setCentralWidget(label)

    def add_sources(self, directory):
        def receive():
            self.sourceList.clear()
            self.destList.clear()
            sources = dialog.selectedFiles()
            for item in sources:
                if os.path.isdir(item):
                    for subdir, dirs, files in os.walk(item):
                        for filename in files:
                            filepath = os.path.join(subdir, filename)
                            qtitem = listwidget_item(filename, filepath)
                            self.sourceList.addItem(qtitem)
                else:
                    qtitem = listwidget_item(os.path.basename(item), item)
                    self.sourceList.addItem(qtitem)

        t = 'directory' if directory else 'files'
        msg = self.tr(f"Choose {t} to rename")
        dialog = choose_sources_dialog(self, msg, directory=directory)
        dialog.open(receive)

    def match_sources(self):
        guess = utils.guess_title(*listwidget_text_items(self.sourceList))
        print(f'Guessing {guess}')
        # dialog = search_dialog(self, guess)
        # dialog.open(receive)

        window = SearchWindow(guess)
        window.setParent(self, QtCore.Qt.Sheet)
        window.show()
        if window.exec_():
            self.destList.clear()
            for i, name in enumerate(listwidget_text_items(self.sourceList)):
                self.destList.addItem(f'{window.result.title} - {i+1}')

    def process_action(self):
        for source, dest in zip(listwidget_text_items(self.sourceList), listwidget_text_items(self.destList)):
            print(f'os.symlink({source}, {dest})')

