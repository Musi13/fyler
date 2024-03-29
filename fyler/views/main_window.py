import os
import platform
from fnmatch import fnmatch
from importlib import resources

from PyQt5 import uic, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListView, QAbstractItemView, QTreeView

from fyler import assets, utils, settings, settings_handler
from fyler.utils import listwidget_text_items, listwidget_data_items, listwidget_item
from fyler.views.advanced_window import AdvancedWindow
from fyler.views.search_window import SearchWindow
from fyler.views.settings_window import SettingsWindow

uifile = resources.open_text(assets, 'mainwindow.ui')
MainWindowUI, MainWindowBase = uic.loadUiType(uifile)


def choose_sources_dialog(parent, title, directory=True, initial=None):
    options = QFileDialog.Options()
    if directory:
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog
    dialog = QFileDialog(parent, title, os.path.expanduser('~'), options=options)
    dialog.setFileMode(QFileDialog.Directory if directory else QFileDialog.ExistingFiles)
    dialog.setParent(parent, QtCore.Qt.Sheet)

    file_view = dialog.findChild(QListView, 'listView')
    if file_view:
        file_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

    tree_view = dialog.findChild(QTreeView)
    if tree_view:
        tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

    if initial:
        dialog.setDirectory(initial)
    return dialog


class MainWindow(MainWindowUI, MainWindowBase):
    def __init__(self, application=None):
        super().__init__()
        self.setupUi(self)

        self.application = application

        # Scroll lists together
        self.sourceList.verticalScrollBar().valueChanged.connect(
            self.destList.verticalScrollBar().setValue)
        self.destList.verticalScrollBar().valueChanged.connect(
            self.sourceList.verticalScrollBar().setValue)

        # Select from lists together
        self.sourceList.currentRowChanged.connect(self.destList.setCurrentRow)
        self.destList.currentRowChanged.connect(self.sourceList.setCurrentRow)

        self.folderButton.clicked.connect(lambda: self.add_sources(directory=True))
        self.filesButton.clicked.connect(lambda: self.add_sources(directory=False))

        self.matchButton.clicked.connect(self.match_sources)
        self.matchButton.setText(f'Match ({settings.provider().name})')
        self.actionButton.clicked.connect(self.process_action)
        self.actionButton.setText(settings_handler.action_names[settings['modify_action']])

        self.sourceUpButton.clicked.connect(lambda: self.move_item(self.sourceList, 'up'))
        self.sourceDownButton.clicked.connect(lambda: self.move_item(self.sourceList, 'down'))
        self.destUpButton.clicked.connect(lambda: self.move_item(self.destList, 'up'))
        self.destDownButton.clicked.connect(lambda: self.move_item(self.destList, 'down'))

        self.sourceXButton.clicked.connect(lambda: self.remove_item(self.sourceList))
        self.destXButton.clicked.connect(lambda: self.remove_item(self.destList))

        self.settingsButton.clicked.connect(self.edit_settings)
        self.advancedButton.clicked.connect(self.open_advanced)

    def add_sources(self, directory: bool):
        """Open file selection dialog and load choices into sourceList"""
        append = self.application.queryKeyboardModifiers() & Qt.ControlModifier

        def receive():
            if not append:
                self.sourceList.clear()
            self.destList.clear()
            settings['prev_sources_directory'] = dialog.directory().absolutePath()
            settings.save()
            sources = dialog.selectedFiles()
            for item in sources:
                if os.path.isdir(item):
                    for subdir, dirs, files in os.walk(item):
                        for filename in files:
                            filepath = os.path.abspath(os.path.join(subdir, filename))

                            skip = False
                            for pattern in settings['exclude_filters']:
                                if fnmatch(filepath, pattern):
                                    skip = True
                                    break
                            if skip:
                                continue

                            qtitem = listwidget_item(filename, filepath)
                            self.sourceList.addItem(qtitem)
                else:
                    filepath = os.path.abspath(item)

                    skip = True
                    for pattern in settings['exclude_filters']:
                        if fnmatch(filepath, pattern):
                            skip = True
                            break
                    if skip:
                        continue

                    qtitem = listwidget_item(os.path.basename(filepath), filepath)
                    self.sourceList.addItem(qtitem)
            self.sourceList.sortItems()

        t = 'directory' if directory else 'files'
        msg = self.tr(f"Choose {t} to rename" + ' (append)' if append else '')
        dialog = choose_sources_dialog(self, msg, directory=directory, initial=settings.get('prev_sources_directory'))
        dialog.accepted.connect(receive)  # Explicit connect accepted since open() doesnt work with multi-select
        dialog.open()

    def _update_dest_paths(self):
        """Update the paths based on format and episode data"""
        # Ampherstand chosen since most use cases are for multiple shorts in one episode
        chartab = {ord('/'): '&'}
        if 'windows' in platform.platform().lower():
            chartab.update({
                ord(':'): ' -',
                ord('\\'): None,
                ord('"'): "'",
                ord('<'): None,
                ord('>'): None,
                ord('?'): None,
                ord('*'): '!',
                ord('|'): None,
            })
        for i in range(self.destList.count()):
            qtitem = self.destList.item(i)
            item = qtitem.data(Qt.UserRole)
            env = item.template_values()
            for key, value in env.items():
                if callable(value):
                    try:  # Support lambda: <risky>; if <risky> fails, replace with *
                        value = value()
                    except Exception:
                        value = '*'
                env[key] = str(value).translate(chartab)
            try:
                dest = settings['output_format'].format(**env)
            except KeyError as e:
                dest = f"*Error: Template variable {e} not found*"
            qtitem.setText(dest)

    def match_sources(self):
        if self.sourceList.count() <= 0:
            return

        # Guess title by removing some noise and taking longest common prefix
        guess = utils.guess_title(*listwidget_text_items(self.sourceList))
        window = SearchWindow(guess)
        window.setParent(self, Qt.Sheet)
        window.show()
        if window.exec_():
            self.destList.clear()
            for item in window.result.items():
                qtitem = listwidget_item('{placeholder}', item)
                self.destList.addItem(qtitem)
            self._update_dest_paths()

    def process_action(self):
        # Loop through rows, but always use top item to delete after its done
        num_actions = min(self.sourceList.count(), self.destList.count())
        for _ in range(num_actions):
            source = self.sourceList.item(0).data(Qt.UserRole)
            dest = os.path.expanduser(os.path.expandvars(self.destList.item(0).text()))
            extension = os.path.splitext(source)[1]
            if destdir := os.path.dirname(dest):
                os.makedirs(destdir, exist_ok=True)
            settings.action()(source, dest + extension)
            self.sourceList.takeItem(0)
            self.destList.takeItem(0)

    def edit_settings(self):
        window = SettingsWindow()
        window.setParent(self, Qt.Sheet)
        window.show()
        window.exec_()
        self.matchButton.setText(f'Match ({settings.provider().name})')
        self.actionButton.setText(settings_handler.action_names[settings['modify_action']])
        self._update_dest_paths()

    def open_advanced(self):
        window = AdvancedWindow()
        window.setParent(self, Qt.Sheet)
        window.show()
        window.exec_()

    def move_item(self, item_list, direction):
        crow = item_list.currentRow()
        if crow < 0:
            return  # Not selected

        # Qt will handle out of bounds selections
        nrow = crow - 1 if direction == 'up' else crow + 1
        item = item_list.takeItem(crow)
        item_list.insertItem(nrow, item)
        item_list.setCurrentRow(nrow)

    def remove_item(self, item_list):
        crow = item_list.currentRow()
        if crow < 0:
            return  # Not selected
        item_list.takeItem(crow)
