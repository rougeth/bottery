import os
import sys
from copy import deepcopy
from importlib import import_module

from bottery.conf import global_settings


def lazy_obj_method(f):
    def inner(self, *args):
        self._setup()
        return f(self._wrapped, *args)

    return inner


class LazySettings:
    _wrapped = None

    __getattr__ = lazy_obj_method(getattr)
    __dir__ = lazy_obj_method(dir)

    def __setattr__(self, name, value):
        if name == '_wrapped':
            super().__setattr__(name, value)
        else:
            setattr(self._wrapped, name, value)

    def _setup(self):
        if not self._wrapped:
            self._wrapped = Settings()
            self._wrapped.configure()

    def configure(self, default_settings=global_settings, **options):
        if self._wrapped is not None:  # TODO: check for {}, (), '', etc
            raise RuntimeError('Settings already configured.')

        holder = UserSettingsHolder(default_settings)
        for name, value in options.items():
            setattr(holder, name, value)

        self._wrapped = holder


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


class UserSettingsHolder:
    def __init__(self, defaut_settings):
        for key in dir(defaut_settings):
            if key.isupper():
                value = getattr(defaut_settings, key)
                setattr(self, key, deepcopy(value))


settings = LazySettings()
