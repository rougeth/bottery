import importlib
import os
import sys


def import_settings():
    base = os.getcwd()
    settings_path = os.path.join(base, 'settings.py')
    if not os.path.isfile(settings_path):
        raise Exception('Could not find settings module')
    sys.path.insert(0, base)

    return importlib.import_module('settings')
