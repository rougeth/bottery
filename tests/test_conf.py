from unittest import mock

import pytest

from bottery.conf import Settings


@pytest.fixture
def mocked_settings():
    settings = mock.MagicMock()
    sys.modules['settings'] = settings
    yield settings
    del sys.modules['settings']


@pytest.mark.skip
def test_global_settings():
    settings = Settings()

    assert settings.PLATFORMS == {}
    assert settings.TEMPLATES == []


@pytest.mark.skip
def test_settings_from_module(mocked_settings):
    mocked_settings.PLATFORM = 'matrix'

    settings = Settings.from_object('settings')
    assert settings.PLATFORM == 'matrix'
    assert settings.PLATFORM == 'matrix'
