import os
import sys
from copy import deepcopy
from importlib import import_module

from bottery.conf import global_settings


def lazy_obj_method(f):
    def inner(self, *args):
        if not self._wrapped:
            self._setup()
        return f(self._wrapped, *args)

    return inner


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
        sys.path.insert(0, base)

    def _import_settings(self):
        self._configure_settings_path()
        mod = import_module('settings')

class Settings:
    def configure(self):
        self.global_settings()
        self.import_settings()

    def setattr_module(self, mod):
        for setting in dir(mod):
            if setting.isupper():
                setattr(self, setting, getattr(mod, setting))

    def local_settings(self):
        base = os.getcwd()
        sys.path.insert(0, base)
        return import_module('settings')

    def global_settings(self):
        self.setattr_module(global_settings)

    def import_settings(self):
        mod = self.local_settings()
        self.setattr_module(mod)

    def __getattr__(self, name):
        if not self._wrapped:
            self._setup()
        return getattr(self._wrapped, name)


settings = LazySettings()
