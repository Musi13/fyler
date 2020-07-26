import os
import json
from collections import UserDict
from appdirs import AppDirs

from fyler.providers import all_providers
from fyler.utils import noop_action, relative_symlink

dirs = AppDirs('fyler', 'fyler')
CONFIG_FILE = os.environ.get('FYLER_CONFIG_FILE', os.path.join(dirs.user_config_dir, 'config.json'))

# internal name -> func
_action_funcs = {
    'rename': os.rename,
    'absolute_symlink': os.symlink,
    'relative_symlink': relative_symlink,
    'hardlink': os.link,
    'noop': noop_action,
}

# internal name -> friendly name
# TODO: one dict? More confusing but no duplication
action_names = {
    'rename': 'Rename',
    'absolute_symlink': 'Absolute Symlink',
    'relative_symlink': 'Relative Symlink',
    'hardlink': 'Hardlink',
    'noop': 'No-op (Debug)',
}


class SettingsDict(UserDict):
    appdirs = dirs

    def provider(self):
        return all_providers[self['provider']]

    def action(self):
        return _action_funcs[self['modify_action']]


def default_settings():
    return SettingsDict({
        'provider': 'thetvdb',
        'modify_action': 'rename',
        'output_format': '{n} - {s00e00} - {t}',
        'search_result_format': '{t}',
    })


def load_settings(filepath=CONFIG_FILE):
    """Load settings from `filepath`"""
    ret = default_settings()
    try:
        with open(filepath) as f:
            ret.update(json.load(f))
    except Exception:
        pass
    return ret


settings = load_settings()


def save_settings(filepath=CONFIG_FILE):
    """Save settings to `filepath`"""
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), mode=0o775, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(settings.data, f, indent=4)
