import asyncio
from unittest import mock

import aiohttp
import pytest

from bottery.app import App


def test_app_session():
    app = App()
    assert isinstance(app.session, aiohttp.ClientSession)

def test_app_already_configured_session():
    app = App()
    app._session = 'session'
    assert app.session == 'session'

def test_app_loop():
    app = App()
    assert isinstance(app.loop, asyncio.AbstractEventLoop)

def test_app_already_configured_loop():
    app = App()
    app._loop = 'loop'
    assert app.loop == 'loop'

@mock.patch('bottery.app.settings')
def test_app_configure_without_platforms(mocked_settings):
    """Should raise Exception if no platform was found at settings"""

    mocked_settings.PLATFORMS = {}
    app = App()
    with pytest.raises(Exception):
        app.configure_platforms()

