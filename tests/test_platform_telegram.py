import aiohttp
import pytest

from bottery.platform.telegram.api import TelegramAPI
from bottery.platform.telegram.engine import TelegramEngine


def test_platform_telegram_api_non_existent_method():
    api = TelegramAPI('token', aiohttp.ClientSession)
    with pytest.raises(AttributeError):
        api.non_existent_method()


@pytest.mark.asyncio
async def test_platform_telegram_api_get_updates():
    api = TelegramAPI('token', aiohttp.ClientSession)
    with pytest.raises(TypeError):
        await api.get_updates()


def test_platform_telegram_engine_get_chat_id_private():
    user = type('TelegramUser', (), {'id': '123'})
    chat = type('TelegramChat', (), {'type': 'private'})
    message = type('Message', (), {'user': user, 'chat': chat})
    engine = TelegramEngine

    assert engine.get_chat_id(engine, message) == '123'


def test_platform_telegram_engine_get_chat_id_group():
    chat = type('TelegramChat', (), {'id': '456', 'type': 'group'})
    message = type('Message', (), {'chat': chat})
    engine = TelegramEngine

    assert engine.get_chat_id(engine, message) == '456'
