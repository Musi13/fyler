import os
from pathlib import Path
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QLabel, QMainWindow, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt

from fyler import utils, settings, settings_handler
from fyler.utils import listwidget_text_items, listwidget_data_items, listwidget_item
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

        # TODO: Add buttons/hotkeys for reassigning matches
        # TODO: Scroll the two lists together
        self.folderButton.clicked.connect(lambda: self.add_sources(directory=True))
        self.filesButton.clicked.connect(lambda: self.add_sources(directory=False))

        self.matchButton.clicked.connect(self.match_sources)
        self.actionButton.clicked.connect(self.process_action)
        self.actionButton.setText(settings['modify_action'].title())

        self.sourceUpButton.clicked.connect(lambda: self.move_item(self.sourceList, 'up'))
        self.sourceDownButton.clicked.connect(lambda: self.move_item(self.sourceList, 'down'))
        self.destUpButton.clicked.connect(lambda: self.move_item(self.destList, 'up'))
        self.destDownButton.clicked.connect(lambda: self.move_item(self.destList, 'down'))

        self.sourceXButton.clicked.connect(lambda: self.remove_item(self.sourceList))
        self.destXButton.clicked.connect(lambda: self.remove_item(self.destList))



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
                            filepath = os.path.abspath(os.path.join(subdir, filename))
                            qtitem = listwidget_item(filename, filepath)
                            self.sourceList.addItem(qtitem)
                else:
                    filepath = os.path.abspath(item)
                    qtitem = listwidget_item(os.path.basename(filepath), filepath)
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
                # TODO: These formats are failing because of invalid types (sometimes things are None),
                # it would be nice if those cases resulted in a * or something
                env.update({
                    'n': window.result.title,
                    's': episode.season_number,
                    'e': episode.episode_number,
                    'sxe': f'{episode.season_number}x{episode.episode_number:02}',
                    's00e00': f'S{episode.season_number:02}E{episode.episode_number:02}' if episode.season_number and episode.episode_number else '*',
                    'e00': f'{episode.episode_number:02}',
                    't': episode.title,
                    'id': episode.id,
                })
                dest = settings['output_format'].format(**env).replace('/', '&')
                self.destList.addItem(dest)

    def process_action(self):
        for source, dest in zip(listwidget_data_items(self.sourceList), listwidget_text_items(self.destList)):
            action = settings['modify_action']  # TODO: settings.action()
            extension = os.path.splitext(source)[1]
            print(f'{action}({source}, {dest}{extension})')

    def edit_settings(self):
        window = SettingsWindow()
        window.setParent(self, Qt.Sheet)
        window.show()
        window.exec_()
        self.actionButton.setText(settings_handler.action_names[settings['modify_action']])
        # TODO: Re-evaluate all destList items with output_format

    def move_item(self, item_list, direction):
        crow = item_list.currentRow()
        if crow < 0:
            return  # Not selected

        nrow = crow - 1 if direction == 'up' else crow + 1
        item = item_list.takeItem(crow)
        item_list.insertItem(nrow, item)
        item_list.setCurrentRow(nrow)

    def remove_item(self, item_list):
        crow = item_list.currentRow()
        if crow < 0:
            return  # Not selected
        item_list.takeItem(crow)
