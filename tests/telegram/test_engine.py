from unittest import mock

import pytest

from bottery.exceptions import ImproperlyConfigured
from bottery.message import Message
from bottery.platform.telegram import TelegramEngine, TelegramUser


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


def test_engine_default_mode(token, session):
    engine = TelegramEngine(token=token, session=session)
    assert engine.mode == 'polling'


def test_engine_set_mode(token, session):
    engine = TelegramEngine(token=token, session=session, mode='webhook')
    assert engine.mode == 'webhook'


@pytest.mark.asyncio
async def test_engine_missing_configuration_method(token, session):
    engine = TelegramEngine(token=token, session=session,
                            mode='not-defined-mode')

    with pytest.raises(ImproperlyConfigured):
        await engine.configure()


@pytest.mark.asyncio
async def test_engine_configure_polling(token, mock_session):
    session = mock_session({'ok': True})
    engine = TelegramEngine(token=token, session=session)

    await engine.configure()

    url = 'https://api.telegram.org/bot{}/deleteWebhook'.format(token)
    engine.session.post.assert_called_once_with(url, json={})
    assert engine.tasks == [engine.polling]


@pytest.mark.asyncio
async def test_engine_configure_webhook(server, token, mock_session):
    with mock.patch('bottery.platform.telegram.settings') as mocked_settings:
        mocked_settings.HOSTNAME = 'localhost'

        session = mock_session({'ok': True})
        engine = TelegramEngine(token=token, session=session, server=server,
                                mode='webhook')

        await engine.configure()

        url = 'https://api.telegram.org/bot{}/setWebhook'.format(engine.token)
        payload = {
            'url': 'localhost'
        }

    assert engine.tasks == []
    assert engine.server.router.add_post.called
    engine.session.post.assert_called_once_with(url, json=payload)


def test_build_message(token, session, new_message_data):
    engine = TelegramEngine(token=token, session=session)

    message = engine.build_message(new_message_data)

    assert type(message) == Message
    assert message.text == 'ping'


def test_build_message_with_non_message_data(token, session):
    engine = TelegramEngine(token=token, session=session)
    data = {
        'update_id': 123456,
        'message_updated': {
        }
    }

    message = engine.build_message(data)

    assert message is None
