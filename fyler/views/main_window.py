import os
from pathlib import Path
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QLabel, QMainWindow, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt

from fyler import utils, settings
from fyler.utils import listwidget_text_items, listwidget_item
from fyler.views.search_window import SearchWindow
from fyler.views.settings_window import SettingsWindow

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

class MainWindow(MainWindowUI, MainWindowBase):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)

        self.folderButton.clicked.connect(lambda: self.add_sources(directory=True))
        self.filesButton.clicked.connect(lambda: self.add_sources(directory=False))

        self.matchButton.clicked.connect(self.match_sources)
        self.actionButton.clicked.connect(self.process_action)
        self.actionButton.setText(settings['modify_action'].title())

        self.settingsButton.clicked.connect(self.edit_settings)

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
        if self.sourceList.count() <= 0:
            return

        guess = utils.guess_title(*listwidget_text_items(self.sourceList))
        window = SearchWindow(guess)
        window.setParent(self, Qt.Sheet)
        window.show()
        if window.exec_():
            self.destList.clear()
            for episode in window.result.episodes:
                env = window.result.asdict()
                env['episode_number'] = episode.asdict()['episode_number']
                env['season_number'] = episode.asdict()['season_number']
                self.destList.addItem(settings['output_format'].format(**env))

    def process_action(self):
        actions = {
            'symlink': os.symlink,
            'rename': os.rename,
        }
        for source, dest in zip(listwidget_text_items(self.sourceList), listwidget_text_items(self.destList)):
            action = settings['modify_action']  # TODO: actions[settings['modify_action']]
            print(f'{action}({source}, {dest})')

    def edit_settings(self):
        window = SettingsWindow()
        window.setParent(self, Qt.Sheet)
        window.show()
        window.exec_()
        self.actionButton.setText(settings['modify_action'].title())
        # TODO: Re-evaluate all destList items with output_format
