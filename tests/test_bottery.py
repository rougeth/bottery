import asyncio
from unittest import mock

import aiohttp
import pytest

from bottery import Bottery


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def bot():
    bot = Bottery()

    yield bot

    try:
        stop_result = bot.stop()

        if asyncio.iscoroutine(stop_result):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(stop_result)

    except Exception:
        pass


@pytest.fixture
def engine():
    class FakeEngine:
        def __init__(self):
            self.tasks = []
            self.configured = False

        async def configure(self):
            self.configured = True
            self.tasks.append("fake_task")

    return FakeEngine()


# ============================================================
# Property tests
# ============================================================

@pytest.mark.parametrize(
    "attribute,expected_type",
    [
        ("loop", asyncio.AbstractEventLoop),
        ("session", aiohttp.ClientSession),
    ],
)
def test_default_properties(bot, attribute, expected_type):
    value = getattr(bot, attribute)

    assert isinstance(value, expected_type)


@pytest.mark.parametrize("attribute", ["loop", "session"])
def test_already_defined_properties(attribute):
    bot = Bottery()

    setattr(bot, f"_{attribute}", attribute)

    assert getattr(bot, attribute) == attribute


def test_loop_is_singleton(bot):
    loop1 = bot.loop
    loop2 = bot.loop

    assert loop1 is loop2


def test_session_is_singleton(bot):
    session1 = bot.session
    session2 = bot.session

    assert session1 is session2


# ============================================================
# Engine tests
# ============================================================

@pytest.mark.asyncio
async def test_engine_configure_success(engine):
    await engine.configure()

    assert engine.configured is True
    assert engine.tasks == ["fake_task"]


@pytest.mark.asyncio
async def test_engine_configure_adds_task(engine):
    await engine.configure()

    assert len(engine.tasks) == 1
    assert "fake_task" in engine.tasks


# ============================================================
# Configure tests
# ============================================================

@pytest.mark.asyncio
async def test_configure_no_platforms_found(bot):
    with pytest.raises(Exception):
        await bot.configure()


@pytest.mark.skip(reason="Implementar quando houver engine fake real")
@pytest.mark.asyncio
async def test_configure_no_platform_engine_found(bot):
    bot.settings.PLATFORMS["fake_engine"] = {
        "ENGINE": "module.fake_engine"
    }

    assert not bot.tasks


# ============================================================
# Resource lifecycle tests
# ============================================================

@pytest.mark.asyncio
async def test_session_can_be_closed(bot):
    session = bot.session

    await session.close()

    assert session.closed is True


# ============================================================
# Message handler import tests
# ============================================================

@mock.patch("bottery.bottery.importlib.import_module")
def test_bottery_import_msghandlers(mock_import_module):
    from bottery.conf import settings

    settings.configure(
        ROOT_MSGCONF="another_handlers"
    )

    expected_handlers = ["handlers"]

    mock_import_module.return_value.msghandlers = (
        expected_handlers
    )

    bottery = Bottery()

    result = bottery.import_msghandlers()

    assert result == expected_handlers

    mock_import_module.assert_called_once_with(
        "another_handlers"
    )


@mock.patch("bottery.bottery.importlib.import_module")
def test_import_msghandlers_import_error(
    mock_import_module,
):
    mock_import_module.side_effect = ImportError(
        "module not found"
    )

    bottery = Bottery()

    with pytest.raises(ImportError):
        bottery.import_msghandlers()


@mock.patch("bottery.bottery.importlib.import_module")
def test_import_msghandlers_missing_attribute(
    mock_import_module,
):
    class EmptyModule:
        pass

    mock_import_module.return_value = EmptyModule()

    bottery = Bottery()

    with pytest.raises(AttributeError):
        bottery.import_msghandlers()


# ============================================================
# Defensive tests
# ============================================================

def test_loop_property_not_none(bot):
    assert bot.loop is not None


def test_session_property_not_none(bot):
    assert bot.session is not None


def test_session_is_aiohttp_client_session(bot):
    assert isinstance(
        bot.session,
        aiohttp.ClientSession,
    )


def test_loop_is_event_loop(bot):
    assert isinstance(
        bot.loop,
        asyncio.AbstractEventLoop,
    )
