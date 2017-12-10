from importlib import import_module

from bottery.conf import global_settings


class Settings:
    def __init__(self):
        for key in dir(global_settings):
            if key.isupper():
                setattr(self, key, getattr(global_settings, key))

    @classmethod
    def from_object(cls, obj='settings'):
        settings = cls()

        if isinstance(obj, str):
            obj = import_module(obj)

        for key in dir(obj):
            if key.isupper():
                setattr(settings, key, getattr(obj, key))

        return settings
