import os
import sys
from copy import deepcopy
from importlib import import_module

from bottery.conf import global_settings
from bottery.exceptions import ImproperlyConfigured


class Settings:
    def __init__(self):
        self._global_settings()
        self._import_settings()

    def _global_settings(self):
        for key in dir(global_settings):
            if key.isupper():
                value = getattr(global_settings, key)
                setattr(self, key, deepcopy(value))

    def _configure_settings_path(self):
        base = os.getcwd()
        settings_path = os.path.join(base, 'settings.py')
        if not os.path.isfile(settings_path):
            raise ImproperlyConfigured('Could not find settings module')

        sys.path.insert(0, base)

    def _import_settings(self):
        self._configure_settings_path()
        mod = import_module('settings')

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


settings = LazySettings()
