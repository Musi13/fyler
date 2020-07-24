import os
from pathlib import Path
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QLabel, QMainWindow, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt

from fyler import utils, settings

uifile = (Path(__file__) / '../../assets/ui/searchwindow.ui').resolve()
SearchWindowUI, SearchWindowBase = uic.loadUiType(uifile)

class SearchWindow(SearchWindowUI, SearchWindowBase):
    def __init__(self, initial_query=None):
        super().__init__()
        self.setupUi(self)
        self.result = None

        self.searchButton.clicked.connect(self.do_search)
        self.resultList.itemDoubleClicked.connect(self.accept_result)

        if initial_query:
            self.searchBox.setText(initial_query)


    def accept_result(self):
        # TODO, do another query (detail()) for the result to populate the
        # rest of the metadata, the results can be medias that aren't fleshed out
        self.result = self.resultList.currentItem().data(Qt.UserRole)
        self.result = settings.provider().detail(self.result)
        self.accept()

    def do_search(self):
        if not self.searchBox.text():
            return

        self.resultList.clear()
        results = settings.provider().search(self.searchBox.text())

        for item in results:
            qtitem = utils.listwidget_item(item.title, item)
            self.resultList.addItem(qtitem)
