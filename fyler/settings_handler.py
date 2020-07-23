import os
import json
from collections import  UserDict
from appdirs import AppDirs

from fyler.providers import all_providers

dirs = AppDirs('fyler', 'fyler')
CONFIG_FILE = os.environ.get('FYLER_CONFIG_FILE', os.path.join(dirs.user_config_dir, 'config.json'))

class SettingsDict(UserDict):
    def provider(self):
        return all_providers[self['provider']]

def default_settings():
    return SettingsDict({
        'provider': 'anilist',
        'modify_action': 'symlink',
        'output_format': '{title} - {season_number} - {episode_number}'
    })

def load_settings(filepath=CONFIG_FILE):
    ret = default_settings()
    try:
        with open(filepath) as f:
            ret.update(json.load(f))
    except Exception:
        pass
    return ret

settings = load_settings()

def save_settings(filepath=CONFIG_FILE):
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), mode=0o775, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(settings.data, f, indent=4)
