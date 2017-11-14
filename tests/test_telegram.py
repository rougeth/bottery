from unittest import mock

import pytest

from bottery.message import Message
from bottery.platform.telegram import (TelegramAPI, TelegramEngine,
                                       TelegramUser, mixed_case)


@pytest.fixture
def session():
    class Response:
        async def json(self):
            return {'ok': True}

    async def mocked_post(*args, **kwargs):
        return Response()

    with mock.MagicMock() as session:
        session.post.return_value = mocked_post()
        yield session


# TelegramUser


def test_telegram_user_with_last_name():
    sender = {
        'id': 1,
        'first_name': 'Andrew',
        'last_name': 'Martin',
    }

    user = TelegramUser(sender)
    assert str(user) == 'Andrew Martin (1)'


def test_telegram_user_without_last_name():
    sender = {
        'id': 1,
        'first_name': 'Andrew',
    }

    user = TelegramUser(sender)
    assert str(user) == 'Andrew (1)'


# TelegramAPI

def test_mixed_case():
    assert mixed_case('set_webhook') == 'setWebhook'
    assert mixed_case('get_chat_member') == 'getChatMember'


def test_telegram_api_url():
    token = 123
    api = TelegramAPI(token)
    expected_url = 'https://api.telegram.org/bot123/setWebhook'
    assert api.make_url('set_webhook') == expected_url


def test_telegram_api_method_not_defined():
    api = TelegramAPI('token')
    with pytest.raises(AttributeError):
        api.get_chat_member()


@pytest.mark.asyncio
async def test_telegram_api_request():
    '''Make sure requests.post is being called with the right args'''

    async def mocked_post(*args, **kwargs):
        pass

    session = mock.MagicMock()
    session.post.return_value = mocked_post()

    api = TelegramAPI('token', session=session)
    url = api.make_url('send_message')
    data = {
        'chat_id': 1,
        'text': 'Hello World',
    }
    await api.send_message(**data)

    session.post.assert_called_once_with(url, json=data)


# Telegram Engine

def test_build_message():
    engine = TelegramEngine(token='')
    data = {
        'update_id': 123456,
        'message': {
            'message_id': 1,
            'from': {
                'id': 321,
                'is_bot': False,
                'first_name': 'Andrew',
                'last_name': 'Martin',
                'username': 'amartin',
                'language_code': 'en-US'
            },
            'chat': {
                'id': 42,
                'first_name': 'Andrew',
                'last_name': 'Martin',
                'username': 'amartin',
                'type': 'private'
            },
            'date': 1506805222,
            'text': 'ping'
        }
    }

    message = engine.build_message(data)

    assert type(message) == Message
    assert message.text == 'ping'


def test_build_message_with_non_message_data():
    engine = TelegramEngine(token='')
    data = {
        'update_id': 123456,
        'message_updated': {
        }
    }

    message = engine.build_message(data)

    assert message is None


def test_telegram_engine_tasks():
    engine = TelegramEngine(token='')
    assert engine.tasks == [engine.polling]


@pytest.mark.asyncio
async def test_telegram_engine_configure(session):
    '''Make sure logger.debug is called if the response from webhook
       is positive.'''

    engine = TelegramEngine(token='', session=session)
    await engine.configure()
    session.post.assert_called_once_with(
        'https://api.telegram.org/bot/deleteWebhook',
        json={})


@mock.patch('bottery.platform.telegram.logger.debug')
@pytest.mark.asyncio
async def test_telegram_engine_configure_not_ok(mocked_debug):
    '''Make sure logger.debug is not called if the response from webhook
       is negative.'''

    engine = TelegramEngine(token='')
    engine.session = ''
    await engine.configure()
    assert not mocked_debug.called


def test_telegram_engine_define_new_mode():
    '''Make sure TelegramEngine supports new modes.'''
    engine = TelegramEngine(token='', mode='else')
    assert engine.mode == 'else'
