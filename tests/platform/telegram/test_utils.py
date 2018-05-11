from unittest import mock

import pytest

from bottery import telegram


def test_view_keyboard():
    message = mock.Mock(platform='telegram', _request_payload={})

    @telegram.keyboard([['row 1'], ['row 2']])
    def view_with_keyboard(message):
        pass
    view_with_keyboard(message)

    reply_markup = message._request_payload['reply_markup']
    assert reply_markup['resize_keyboard']
    assert reply_markup['one_time_keyboard']
    assert reply_markup['keyboard'] == [
        [{'text': 'row 1'}],
        [{'text': 'row 2'}],
    ]


@pytest.mark.asyncio
async def test_async_view_with_keyboard():
    message = mock.Mock(platform='telegram', _request_payload={})

    @telegram.keyboard([['row 1'], ['row 2']])
    async def async_view_with_keyboard(message):
        pass
    await async_view_with_keyboard(message)

    reply_markup = message._request_payload['reply_markup']
    assert reply_markup['resize_keyboard']
    assert reply_markup['one_time_keyboard']
    assert reply_markup['keyboard'] == [
        [{'text': 'row 1'}],
        [{'text': 'row 2'}],
    ]


def test_view_keyboard_params():
    message = mock.Mock(platform='telegram', _request_payload={})

    @telegram.keyboard([[]], resize_keyboard=False, one_time_keyboard=False)
    def view_with_keyboard(message):
        pass
    view_with_keyboard(message)

    reply_markup = message._request_payload['reply_markup']
    assert not reply_markup['resize_keyboard']
    assert not reply_markup['one_time_keyboard']
