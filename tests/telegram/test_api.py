import pytest

from bottery.platform.telegram import TelegramAPI, mixed_case


def test_mixed_case():
    assert mixed_case('set_webhook') == 'setWebhook'
    assert mixed_case('get_chat_member') == 'getChatMember'


def test_telegram_api_url(token, session):
    api = TelegramAPI(token, session)
    expected_url = 'https://api.telegram.org/bot{}/setWebhook'.format(token)
    assert api.make_url('set_webhook') == expected_url


@pytest.mark.asyncio
async def test_telegram_api_method_not_defined(token, session):
    api = TelegramAPI(token, session)
    with pytest.raises(AttributeError):
        # This is returning a warning but I do not know why:
        # RuntimeWarning: coroutine 'session.<locals>.fake_post' was never
        # awaited.
        await api.get_chat_member()


@pytest.mark.asyncio
async def test_telegram_api_request(token, session):
    '''Make sure session.post is being called with the right args'''

    api = TelegramAPI(token, session)

    expected_url = api.make_url('send_message')
    expected_data = {
        'chat_id': 1,
        'text': 'Hello World',
    }

    await api.send_message(**expected_data)
    expected_url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
    session.post.assert_called_once_with(expected_url, json=expected_data)
