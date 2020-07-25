from pathlib import Path
from PyQt5 import uic
from fyler import providers

uifile = (Path(__file__) / '../../assets/ui/advancedwindow.ui').resolve()
AdvancedWindowUI, AdvancedWindowBase = uic.loadUiType(uifile)


class AdvancedWindow(AdvancedWindowUI, AdvancedWindowBase):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.anidbDownloadButton.clicked.connect(self.download_anidb_data)

    def download_anidb_data(self):
        providers.all_providers['anidb'].download_title_data()
