from importlib import resources
from PyQt5 import uic
from fyler import providers, assets

uifile = resources.open_text(assets, 'advancedwindow.ui')
AdvancedWindowUI, AdvancedWindowBase = uic.loadUiType(uifile)


class AdvancedWindow(AdvancedWindowUI, AdvancedWindowBase):
    """Window for Advanced Tools, usually special action that don't happen often"""
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.anidbDownloadButton.clicked.connect(self.download_anidb_data)

    def download_anidb_data(self):
        providers.all_providers['anidb'].download_title_data()
