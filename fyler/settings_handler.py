import os
import json
from collections import  UserDict
from appdirs import AppDirs

from fyler.providers import all_providers

dirs = AppDirs('fyler', 'fyler')
CONFIG_FILE = os.environ.get('FYLER_CONFIG_FILE', os.path.join(dirs.user_config_dir, 'config.json'))

# internal name -> func
_action_funcs = {
    'rename': os.rename,
    'symlink': os.symlink,
}

# internal name -> friendly name
# TODO: one dict? More confusing but no duplication
action_names = {
    'rename': 'Rename',
    'symlink': 'Symlink',
}

class SettingsDict(UserDict):
    appdirs = dirs
    def provider(self):
        return all_providers[self['provider']]

    def action(self):
        return _action_funcs[self['modify_action']]

def default_settings():
    return SettingsDict({
        'provider': 'anilist',
        'modify_action': 'symlink',
        'output_format': '{n} - {s00e00} - {t}'
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
