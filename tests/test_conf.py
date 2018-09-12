from unittest import mock

import pytest

from bottery.conf import Settings, UserSettingsHolder, lazy_obj_method


@pytest.mark.parametrize('wrapped,expected_result', (
    (False, True), (True, False),
))
def test_lazy_obj_method(wrapped, expected_result):
    class Settings:
        _wrapped = wrapped
        _setup = mock.Mock()
        __dir__ = lazy_obj_method(dir)

    settings = Settings()
    dir(settings)

    assert settings._setup.called is expected_result


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
