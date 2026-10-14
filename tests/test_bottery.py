```python
import asyncio
from unittest import mock
from unittest.mock import AsyncMock

import aiohttp
import pytest

from bottery import Bottery


@pytest.fixture
def bot():
    """Cria um Bottery isolado e libera os recursos ao terminar."""
    instance = Bottery()

    try:
        yield instance
    finally:
        # stop() é executado mesmo se uma asserção falhar.
        instance.stop()

        # Salvaguarda para recursos que stop() não tenha encerrado.
        session = getattr(instance, "_session", None)
        loop = getattr(instance, "_loop", None)

        if session is not None and not session.closed:
            if loop is not None and not loop.is_closed():
                loop.run_until_complete(session.close())

        if loop is not None and not loop.is_closed():
            loop.close()


@pytest.fixture
def fake_engine():
    """Engine independente para cada teste."""
    class FakeEngine:
        def __init__(self):
            self.tasks = []
            self.configure_calls = 0

        async def configure(self):
            self.configure_calls += 1
            self.tasks.append("fake_task")

    return FakeEngine()


@pytest.mark.parametrize(
    ("attribute", "instance_type"),
    [
        ("loop", asyncio.AbstractEventLoop),
        ("session", aiohttp.ClientSession),
    ],
)
def test_default_properties(bot, attribute, instance_type):
    assert isinstance(getattr(bot, attribute), instance_type)


@pytest.mark.parametrize(
    ("attribute", "value"),
    [
        ("loop", "custom_loop"),
        ("session", "custom_session"),
    ],
)
def test_already_defined_properties(bot, attribute, value):
    setattr(bot, f"_{attribute}", value)
    assert getattr(bot, attribute) == value


@pytest.mark.asyncio
async def test_configure_without_platforms(bot):
    bot.settings.PLATFORMS = {}

    # Contrato esperado: configuração vazia é inválida.
    # Ajuste ValueError se a implementação documentar outra exceção.
    with pytest.raises(ValueError):
        await bot.configure()


@pytest.mark.parametrize(
    "platforms",
    [
        {"fake": {}},
        {"fake": {"ENGINE": None}},
        {"fake": {"ENGINE": ""}},
    ],
)
@pytest.mark.asyncio
async def test_configure_invalid_engine_configuration(bot, platforms):
    bot.settings.PLATFORMS = platforms

    with pytest.raises(ValueError):
        await bot.configure()


@pytest.mark.asyncio
async def test_configure_missing_module_propagates_import_error(bot):
    bot.settings.PLATFORMS = {
        "fake": {
            "ENGINE": "module.does_not_exist",
        }
    }

    with mock.patch(
        "bottery.bottery.importlib.import_module",
        side_effect=ModuleNotFoundError("module not found"),
    ):
        with pytest.raises(ModuleNotFoundError, match="module not found"):
            await bot.configure()


@pytest.mark.asyncio
async def test_configure_valid_engine(bot, fake_engine):
    bot.settings.PLATFORMS = {
        "fake": {"ENGINE": "module.fake_engine"}
    }

    with mock.patch(
        "bottery.bottery.importlib.import_module"
    ) as mock_import:
        module = mock.Mock()
        module.configure = fake_engine.configure
        mock_import.return_value = module

        await bot.configure()

    mock_import.assert_called_once_with("module.fake_engine")
    assert fake_engine.configure_calls == 1
    assert fake_engine.tasks == ["fake_task"]


@pytest.mark.asyncio
async def test_configure_multiple_platforms(bot):
    platforms = {
        "first": {"ENGINE": "module.first"},
        "second": {"ENGINE": "module.second"},
    }
    bot.settings.PLATFORMS = platforms

    with mock.patch(
        "bottery.bottery.importlib.import_module"
    ) as mock_import:
        module = mock.Mock()
        module.configure = AsyncMock()
        mock_import.return_value = module

        await bot.configure()

    assert mock_import.call_count == len(platforms)
    assert [
        call.args[0] for call in mock_import.call_args_list
    ] == [
        config["ENGINE"] for config in platforms.values()
    ]
    assert module.configure.await_count == len(platforms)


@pytest.mark.asyncio
async def test_configure_engine_failure_is_propagated(bot):
    bot.settings.PLATFORMS = {
        "fake": {"ENGINE": "module.fake_engine"}
    }
    error = RuntimeError("configuration failed")

    with mock.patch(
        "bottery.bottery.importlib.import_module",
        side_effect=error,
    ):
        with pytest.raises(
            RuntimeError,
            match="configuration failed",
        ):
            await bot.configure()


def test_bottery_import_msghandlers(monkeypatch):
    from bottery.conf import settings

    monkeypatch.setattr(
        settings,
        "ROOT_MSGCONF",
        "another_handlers",
        raising=False,
    )

    expected_handlers = ["handlers"]

    with mock.patch(
        "bottery.bottery.importlib.import_module"
    ) as mock_import:
        mock_import.return_value.msghandlers = expected_handlers

        instance = Bottery()
        try:
            assert instance.import_msghandlers() == expected_handlers
            mock_import.assert_called_once_with("another_handlers")
        finally:
            instance.stop()


def test_stop_closes_session_and_loop(bot):
    """Verifica os recursos após stop(), conforme o contrato esperado."""
    session = getattr(bot, "_session", None)
    loop = getattr(bot, "_loop", None)

    bot.stop()

    if session is not None:
        assert session.closed, "A sessão HTTP permaneceu aberta."

    if loop is not None:
        assert loop.is_closed(), "O event loop permaneceu aberto."
```
