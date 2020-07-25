from importlib import resources

from PyQt5 import uic

from fyler import settings, settings_handler, providers, assets

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
        self.searchEdit.setText(settings['search_result_format'])

    def save_settings(self):
        newsettings = {
            'provider': self.providerBox.currentData(),
            'modify_action': self.actionBox.currentData(),
            'output_format': self.formatEdit.text(),
            'search_result_format': self.searchEdit.text(),
        }
        settings.update(newsettings)
        settings_handler.save_settings()
        self.accept()
