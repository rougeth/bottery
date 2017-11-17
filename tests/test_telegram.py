from unittest import mock

import pytest

from bottery.message import Message
from bottery.platform.telegram import TelegramEngine, TelegramUser

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


# Telegram Engine

@pytest.mark.skip()
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


@pytest.mark.skip()
def test_build_message_with_non_message_data():
    engine = TelegramEngine(token='')
    data = {
        'update_id': 123456,
        'message_updated': {
        }
    }

    message = engine.build_message(data)

    assert message is None


@pytest.mark.skip()
def test_telegram_engine_tasks():
    engine = TelegramEngine(token='')
    assert engine.tasks == [engine.polling]


@pytest.mark.skip()
@mock.patch('bottery.platform.telegram.logger.debug')
def test_telegram_engine_configure(mocked_debug):
    '''Make sure logger.debug is called if the response from webhook
       is positive.'''

    def mocked_json(): return {'ok': True}

    def mocked_delete_webhook(): return type('response', (),
                                             {'json': mocked_json})
    engine = TelegramEngine(token='')
    engine.api.delete_webhook = mocked_delete_webhook
    engine.session = ''
    engine.configure()
    assert mocked_debug.called


@pytest.mark.skip()
@mock.patch('bottery.platform.telegram.logger.debug')
def test_telegram_engine_configure_not_ok(mocked_debug):
    '''Make sure logger.debug is not called if the response from webhook
       is negative.'''

    engine = TelegramEngine(token='')
    engine.session = ''
    engine.configure()
    assert not mocked_debug.called


@pytest.mark.skip()
def test_telegram_engine_define_new_mode():
    '''Make sure TelegramEngine supports new modes.'''
    engine = TelegramEngine(token='', mode='else')
    assert engine.mode == 'else'
