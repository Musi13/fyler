import os
from importlib import resources
from pathlib import Path
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QLabel, QMainWindow, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt

from fyler import utils, settings, settings_handler, providers, assets

uifile = resources.open_text(assets, 'settingswindow.ui')
SettingsWindowUI, SettingsWindowBase = uic.loadUiType(uifile)

class SettingsWindow(SettingsWindowUI, SettingsWindowBase):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_settings()
        self.saveButton.clicked.connect(self.save_settings)


    def load_settings(self):
        current = 0
        for idx, (key, value) in enumerate(providers.all_providers.items()):
            self.providerBox.addItem(value.name, key)
            if key == settings['provider']:
                current = idx
        self.providerBox.setCurrentIndex(current)

        current = 0
        for idx, (key, value) in enumerate(settings_handler.action_names.items()):
            self.actionBox.addItem(value, key)
            if key == settings['modify_action']:
                current = idx
        self.actionBox.setCurrentIndex(current)

        self.formatEdit.setText(settings['output_format'])

    def save_settings(self):
        newsettings = {
            'provider': self.providerBox.currentData(),
            'modify_action': self.actionBox.currentData(),
            'output_format': self.formatEdit.text(),
        }
        settings.update(newsettings)
        settings_handler.save_settings()
        self.accept()
