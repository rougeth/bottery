import asyncio

import aiohttp
import pytest

from bottery import Bottery


class FakeSettings:
    PLATFORM = {}


@pytest.fixture
def settings():
    return FakeSettings()


@pytest.fixture
def bot(settings):
    bot = Bottery(settings_module=settings)
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
def test_already_defined_properties(settings, attribute):
    bot = Bottery(settings_module=settings)
    setattr(bot, '_{}'.format(attribute), attribute)
    assert getattr(bot, attribute) == attribute


@pytest.mark.asyncio
async def test_configure_engine(bot, engine):
    await bot.configure_engine(engine)
    assert bot.tasks[0] == engine.tasks[0]


@pytest.mark.asyncio
async def test_configure_no_platforms_found(engine):
    with pytest.raises(Exception):
        await bot.configure()


@pytest.mark.asyncio
async def test_configure_no_platform_engine_found(bot):
    bot.settings.PLATFORMS['fake_engine'] = {
        'ENGINE': 'module.fake_engine'
    }
    assert not bot.tasks
