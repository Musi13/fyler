from importlib import resources

from PyQt5 import uic
from PyQt5.QtCore import Qt

from fyler import utils, settings, assets

uifile = resources.open_text(assets, 'searchwindow.ui')
SearchWindowUI, SearchWindowBase = uic.loadUiType(uifile)


class SearchWindow(SearchWindowUI, SearchWindowBase):
    def __init__(self, initial_query=None):
        super().__init__()
        self.setupUi(self)
        self.result = None

        # TODO: Consider changing the search text to something like "Search ({provider})"
        self.searchButton.clicked.connect(self.do_search)
        self.searchButton.setText(f'Search {settings.provider().name}')
        self.resultList.itemDoubleClicked.connect(self.accept_result)

        if initial_query:
            self.searchBox.setText(initial_query)

    def accept_result(self):
        self.result = self.resultList.currentItem().data(Qt.UserRole)
        self.result = settings.provider().detail(self.result)
        self.accept()

    def do_search(self):
        if not self.searchBox.text():
            return

        self.resultList.clear()
        results = settings.provider().search(self.searchBox.text())

        for item in results:
            try:
                text = settings['search_result_format'].format(**item.template_values())
            except KeyError as e:
                text = f"*Error: Template variable {e} not found*"
            qtitem = utils.listwidget_item(text, item)
            self.resultList.addItem(qtitem)
