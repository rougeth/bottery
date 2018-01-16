import pytest

from bottery.message import Message
from bottery.platform.telegram.engine import TelegramChat
from bottery.platform.telegram.engine import TelegramEngine
from bottery.platform.telegram.engine import TelegramUser


@pytest.fixture
def engine():
    return TelegramEngine


@pytest.fixture
def user():
    return TelegramUser


@pytest.fixture
def chat():
    return TelegramChat


@pytest.fixture()
def message():
    return Message(
        id='',
        platform='',
        text='',
        user=user,
        chat=chat,
        timestamp='',
        raw='',
    )


@pytest.mark.parametrize('chat_type,id_expected', [
    ('group', 456),
    ('private', 123),
])
def test_platform_telegram_engine_get_chat_id(chat_type,
                                              id_expected, engine, message):
    setattr(message.chat, 'id', id_expected)
    setattr(message.chat, 'type', chat_type)
    setattr(message.user, 'id', id_expected)
    assert engine.get_chat_id(engine, message) == id_expected
