import asyncio
from unittest import mock

import aiohttp
import pytest

from bottery import Bottery
from bottery.conf import settings  # Importação movida para o topo do arquivo


@pytest.fixture
def bot():
    """Cria uma instância isolada de Bottery e encerra seus recursos."""
    instance = Bottery()

    try:
        yield instance
    finally:
        instance.stop()


@pytest.mark.parametrize(
    ("attribute", "instance_type"),
    [
        ("loop", asyncio.AbstractEventLoop),
        ("session", aiohttp.ClientSession),
    ],
)
def test_default_properties(bot, attribute, instance_type):
    """Verifica os tipos das propriedades padrão."""
    value = getattr(bot, attribute)

    assert isinstance(value, instance_type)


@pytest.mark.parametrize("attribute", ["loop", "session"])
def test_already_defined_properties(bot, attribute):
    """Verifica se propriedades previamente definidas são preservadas."""
    expected = f"fake_{attribute}"

    setattr(bot, f"_{attribute}", expected)

    assert getattr(bot, attribute) == expected


@pytest.mark.asyncio
async def test_configure_no_platforms_found(bot):
    """Verifica o comportamento quando não há plataformas configuradas."""
    # Dica: Substitua 'Exception' por uma exceção específica do Bottery,
    # se o framework fornecer uma (ex: ConfigurationError, BotteryError).
    with pytest.raises(Exception):
        await bot.configure()


@pytest.mark.asyncio
async def test_bottery_stop(bot):
    """Verifica se o método stop encerra a sessão corretamente."""
    session = bot.session
    bot.stop()
    
    # Garante que a sessão do aiohttp foi devidamente fechada
    assert session.closed


@mock.patch("bottery.bottery.importlib.import_module")
def test_bottery_import_msghandlers(mock_import_module, monkeypatch):
    """Verifica a importação dos manipuladores de mensagens."""
    expected_handlers = ["handlers"]
    mock_module = mock.Mock()
    mock_module.msghandlers = expected_handlers

    mock_import_module.return_value = mock_module

    monkeypatch.setattr(
        settings,
        "ROOT_MSGCONF",
        "another_handlers",
        raising=False,
    )

    bottery = Bottery()

    try:
        result = bottery.import_msghandlers()

        assert result == expected_handlers

        mock_import_module.assert_called_once_with(
            "another_handlers"
        )
    finally:
        bottery.stop()