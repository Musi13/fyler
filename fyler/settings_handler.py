import os
import json
from appdirs import AppDirs

dirs = AppDirs('fyler', 'fyler')
CONFIG_FILE = os.environ.get('FYLER_CONFIG_FILE', os.path.join(dirs.user_config_dir, 'config.json'))

def default_settings():
    return {
        'provider': 'anilist',
        'modify_action': 'symlink',
    }

def load_settings(filepath=CONFIG_FILE):
    ret = default_settings()
    try:
        with open(filepath) as f:
            ret.update(json.load(f))
    except Exception:
        pass
    return ret

settings = load_settings()

def save_settings(filepath=CONFIG_FILE, settings_dict=None):
    if settings_dict is None:  # Set this way in case the settings reference is changed
        settings_dict = settings
    if not os.path.exists(CONFIG_FILE):
        os.makedirs(os.path.dirname(CONFIG_FILE), mode=0o775, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(settings, f, indent=4)
