import asyncio
import sys
from unittest import mock
from time import time

import aiohttp
import pytest

from bottery import Bottery, handlers
from tests.utils import AsyncMock


@pytest.fixture
def fake_engine():
    engine = mock.Mock()
    engine.configure = AsyncMock()
    engine.tasks = []

    engine_module = mock.Mock(engine=engine)
    engine_module.engine.return_value = engine

    sys.modules['fake_engine'] = engine_module
    yield engine
    del sys.modules['fake_engine']


@pytest.fixture
def settings(fake_engine):
    settings = mock.Mock()
    settings.PLATFORMS = {
        'test': {
            'ENGINE': 'fake_engine',
            'OPTIONS': {
                'token': 'should-be-a-valid-token'
            }
        }

    }
    sys.modules['settings'] = settings
    yield settings
    del sys.modules['settings']


@pytest.fixture
def msghandlers():
    handlers_module = mock.Mock(msghandlers=[
        handlers.message('ping', lambda response: 'pong')
    ])

    sys.modules['handlers'] = handlers_module
    yield
    del sys.modules['handlers']


@pytest.fixture
def bot(settings, msghandlers):
    bot = Bottery()
    yield bot
    bot.stop()


@pytest.mark.parametrize('attribute,instance_type', [
    ('loop', asyncio.AbstractEventLoop),
    ('session', aiohttp.ClientSession),
    ('server', aiohttp.web.Application),
])
def test_default_properties(bot, attribute, instance_type):
    assert isinstance(getattr(bot, attribute), instance_type)


@pytest.mark.parametrize('attribute', ['loop', 'session', 'server'])
def test_already_defined_properties(attribute):
    bot = Bottery()
    setattr(bot, '_{}'.format(attribute), attribute)
    assert getattr(bot, attribute) == attribute


def test_global_options(bot):
    expected_options = {'settings', 'active_conversations',
                        'registered_handlers', 'server', 'loop', 'session'}
    global_options = bot.global_options()

    assert set(global_options.keys()) == expected_options


@pytest.mark.asyncio
async def test_configure_no_platforms_found(bot, settings):
    settings.PLATFORMS = {}
    with pytest.raises(Exception):
        await bot.configure_platforms()


@pytest.mark.skip
@pytest.mark.asyncio
async def test_configure_platforms(bot, settings, fake_engine):
    await bot.configure_platforms()
    assert fake_engine.configure.call_count == 1


def test_run(bot):
    mocked_configure = mock.Mock()
    bot.configure = mocked_configure

    with mock.patch.object(bot, '_loop') as mocked_loop:
        bot.run()

    assert mocked_configure.call_count == 1
    assert mocked_loop.run_forever.call_count == 1
