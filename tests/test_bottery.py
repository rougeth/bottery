import asyncio
from unittest import mock

import aiohttp
import pytest

from bottery import Bottery


class FakeSettings:
    PLATFORM = {}


@pytest.fixture
def bot():
    bot = Bottery()
    yield bot
    bot.stop()


@pytest.fixture
def engine():
    class FakeEngine:
        tasks = []

        async def configure(self):
            self.tasks.append('fake_task')

    return FakeEngine()


@pytest.mark.parametrize('attribute,instance_type', [
    ('loop', asyncio.AbstractEventLoop),
    ('session', aiohttp.ClientSession),
])
def test_default_properties(bot, attribute, instance_type):
    assert isinstance(getattr(bot, attribute), instance_type)


@pytest.mark.parametrize('attribute', ['loop', 'session'])
def test_already_defined_properties(attribute):
    bot = Bottery()
    setattr(bot, '_{}'.format(attribute), attribute)
    assert getattr(bot, attribute) == attribute


@pytest.mark.asyncio
async def test_configure_no_platforms_found(engine):
    with pytest.raises(Exception):
        await bot.configure()


@pytest.mark.skip
@pytest.mark.asyncio
async def test_configure_no_platform_engine_found(bot):
    bot.settings.PLATFORMS['fake_engine'] = {
        'ENGINE': 'module.fake_engine'
    }
    assert not bot.tasks


@mock.patch('bottery.bottery.importlib.import_module')
def test_bottery_import_msghandlers(mock_import_module):
    # TODO: export settings to a fixture
    from bottery.conf import settings
    settings.configure(ROOT_MSGCONF='another_handlers')

    expected_return = ['handlers']
    mock_import_module.return_value.msghandlers = expected_return

    bottery = Bottery()
    assert bottery.import_msghandlers() == expected_return
    assert mock_import_module.call_args == (('another_handlers',),)
