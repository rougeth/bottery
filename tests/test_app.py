import asyncio
import sys
from unittest import mock

import aiohttp
import pytest

from bottery.app import App


@pytest.fixture
def mocked_engine(mock):
    async def fake_configure():
        return True

    mocked_settings = mock.patch('bottery.app.settings')
    mocked_settings.PLATFORMS = {
        'test_platform': {
            'ENGINE': 'tests.fake_engine',
            'OPTIONS': {
                'token': 'should-be-a-valid-token'
            }
        }
    }

    mocked_engine_module = mock.MagicMock()
    mocked_engine_instance = mocked_engine_module.engine.return_value
    mocked_engine_instance.tasks.return_value = [lambda session: 'fake']
    mocked_engine_instance.configure = fake_configure
    sys.modules['tests.fake_engine'] = mocked_engine_module

    yield {
        'module': mocked_engine_module,
        'instance': mocked_engine_instance
    }

    del sys.modules['tests.fake_engine']


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


@pytest.mark.asyncio
@mock.patch('bottery.app.settings')
async def test_app_configure_without_platforms(mocked_settings):
    """Should raise Exception if no platform was found at settings"""

    mocked_settings.PLATFORMS = {}
    app = App()
    with pytest.raises(Exception):
        await app.configure_platforms()


@pytest.mark.asyncio
async def test_app_configure_with_tasks(mocked_engine):
    """App should have empty tasks if not defined on engine"""

    mocked_engine['instance'].tasks = []
    app = App()
    await app.configure_platforms()

    assert not app.tasks


@pytest.mark.skip()
def test_app_configure_with_multiple_tasks(mocked_engine):
    """App should have multiple tasks if defined on engine"""
    async def fake_task(session):
        await asyncio.sleep(0)

    first_task = fake_task
    second_task = fake_task

    mocked_engine['instance'].tasks = [first_task, second_task]
    app = App()
    app.configure_platforms()

    assert app.tasks == [first_task, second_task]


@pytest.mark.skip()
def test_app_configure_with_platforms(mocked_engine):
    """Should call the platform interface methods"""

    app = App()
    app.configure_platforms()

    mocked_engine['module'].engine.assert_called_with(
        session=app.session,
        engine_name='test_platform',
        token='should-be-a-valid-token'
    )
    mocked_engine['instance'].configure.assert_called_with()


@pytest.mark.usefixtures('mocked_engine')
@mock.patch('bottery.app.asyncio')
def test_app_run(mocked_asyncio):
    """Should create tasks and run forever"""

    app = App()
    app.run()

    mocked_event_loop = mocked_asyncio.get_event_loop.return_value

    mocked_asyncio.get_event_loop.assert_called_with()
    mocked_event_loop.run_forever.assert_called_with()


def test_app_stop():
    app = App()
    app.stop()

    assert app.loop.is_closed()
    assert app.session.closed
