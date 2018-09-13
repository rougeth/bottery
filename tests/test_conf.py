from unittest import mock

import pytest

from bottery.conf import (LazySettings, Settings, UserSettingsHolder,
                          lazy_obj_method)


def test_lazy_obj_method():
    class Settings:
        _wrapped = None
        _setup = mock.Mock()
        __dir__ = lazy_obj_method(dir)

    settings = Settings()
    dir(settings)

    assert settings._setup.called is True


@mock.patch('bottery.conf.Settings')
def test_lazysettings_setup(mock_settings):
    lazy_settings = LazySettings()
    lazy_settings._setup()

    assert mock_settings.called is True
    assert lazy_settings._wrapped.configure.called is True


def test_lazysettings_set_wrapped():
    lazy_settings = LazySettings()
    lazy_settings._wrapped = 'test'
    assert lazy_settings._wrapped == 'test'


def test_lazysettings_setattr():
    lazy_settings = LazySettings()
    lazy_settings._wrapped = type('_wrapped', (), {})

    lazy_settings.attr = 'value'

    assert lazy_settings._wrapped.attr == 'value'


def test_lazysettings_configure():
    lazy_settings = LazySettings()
    lazy_settings.configure(attr='value')

    # Default settings
    assert lazy_settings.TEMPLATES == []
    assert lazy_settings.PLATFORMS == {}
    assert lazy_settings.MIDDLEWARES == []
    # Settings by params
    assert lazy_settings.attr == 'value'


def test_lazysettings_already_configured():
    lazy_settings = LazySettings()
    lazy_settings._wrapped = 'settings'

    with pytest.raises(RuntimeError):
        lazy_settings.configure()


def test_settings_configure():
    settings = Settings()
    settings.global_settings = mock.Mock()
    settings.import_settings = mock.Mock()

    settings.configure()
    assert settings.global_settings.called is True
    assert settings.import_settings.called is True


def test_settings_global_settings():
    settings = Settings()
    settings.global_settings()

    assert settings.TEMPLATES == []
    assert settings.PLATFORMS == {}
    assert settings.MIDDLEWARES == []


@mock.patch('bottery.conf.sys')
@mock.patch('bottery.conf.import_module')
@mock.patch('bottery.conf.os.getcwd', return_value='test_settings')
def test_settings_local_settings(mock_getcwd, mock_import_module, mock_sys):
    mock_sys.path = []

    settings = Settings()
    settings.local_settings()

    assert mock_sys.path[0] == 'test_settings'
    assert mock_import_module.called is True
    assert mock_getcwd.called is True


def test_settings_setattr_module():
    mod = type('Settings', (), {'VALID': True, 'invalid': False})
    settings = Settings()
    settings.setattr_module(mod)

    assert settings.VALID
    assert not hasattr(settings, 'invalid')


@mock.patch('bottery.conf.import_module')
def test_settings_import_settings(mock_import_module):
    mod = type('Settings', (), {
        'DEBUG': True,
        'anotherconf': True,
    })

    settings = Settings()
    settings.local_settings = mock.Mock(return_value=mod)
    settings.import_settings()

    assert settings.DEBUG


def test_usersettingsholder():
    templates = []
    default_settings = type('Settings', (), {
        'TEMPLATES': templates,
        'anotherconf': True,
    })

    settings = UserSettingsHolder(default_settings)
    assert settings.TEMPLATES == templates
    assert id(settings.TEMPLATES) != id(templates)
    assert not hasattr(settings, 'anotherconf')
