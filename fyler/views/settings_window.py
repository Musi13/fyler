import os
from pathlib import Path
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QLabel, QMainWindow, QFileDialog, QInputDialog
from PyQt5.QtCore import Qt

from fyler import utils, settings, settings_handler

uifile = (Path(__file__) / '../../assets/ui/settingswindow.ui').resolve()
SettingsWindowUI, SettingsWindowBase = uic.loadUiType(uifile)

class SettingsWindow(SettingsWindowUI, SettingsWindowBase):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_settings()
        self.saveButton.clicked.connect(self.save_settings)


    def load_settings(self):
        self.providerEdit.setText(settings['provider'])
        self.actionEdit.setText(settings['modify_action'])
        self.formatEdit.setText(settings['output_format'])

    def save_settings(self):
        newsettings = {
            'provider': self.providerEdit.text(),
            'modify_action': self.actionEdit.text(),
            'output_format': self.formatEdit.text(),
        }
        settings.update(newsettings)
        settings_handler.save_settings()
        self.accept()
