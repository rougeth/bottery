import importlib
import os
import sys

from bottery.conf import global_settings


class Settings:
    def __init__(self):
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        base = os.getcwd()
        settings_path = os.path.join(base, 'settings.py')
        if not os.path.isfile(settings_path):
            raise Exception('Could not find settings module')
        sys.path.insert(0, base)

        mod = importlib.import_module('settings')

        for setting in dir(mod):
            if setting.isupper():
                setattr(self, setting, getattr(mod, setting))


class LazySettings:
    _wrapped = None

    def _setup(self):
        self._wrapped = Settings()

    def __getattr__(self, name):
        if not self._wrapped:
            self._setup()
        return getattr(self._wrapped, name)
