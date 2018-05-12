import pytest

from bottery.messenger import MessengerAPI
from utils import AsyncMock


@pytest.fixture
def api():
    session = AsyncMock()
    return MessengerAPI('token', session)


def test_make_url_default_version():
    api = MessengerAPI('token', 'session')
    expected_url = 'https://graph.facebook.com/v2.6/method?access_token=token'
    assert api.make_url('/method') == expected_url


@pytest.mark.asyncio
async def test_messages(api):
    await api.messages('id123', 'hello, world!')
    assert api.session.post.called
