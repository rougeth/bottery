import aiohttp

import pytest

from bottery.platform.telegram.api import TelegramAPI


def test_platform_telegram_api_non_existent_method():
    api = TelegramAPI('token', aiohttp.ClientSession)
    with pytest.raises(AttributeError):
        api.non_existent_method()


@pytest.mark.asyncio
async def test_platform_telegram_api_get_updates():
    api = TelegramAPI('token', aiohttp.ClientSession)
    with pytest.raises(TypeError):
        await api.get_updates()
