import inspect
import sys
from unittest import mock

import pytest

from bottery.message import Response
from bottery.platform import BaseEngine
from utils import AsyncMock


@pytest.fixture
def settings():
    settings = mock.Mock()
    sys.modules['settings'] = settings
    yield settings
    del sys.modules['settings']


def test_baseengine_platform_name_not_implemented():
    """Check if attributes from the public API raise NotImplementedError"""
    engine = BaseEngine()
    with pytest.raises(NotImplementedError):
        getattr(engine, 'platform')


@pytest.mark.asyncio
@pytest.mark.parametrize('method_name', ['build_message', 'configure'])
async def test_baseengine_not_implemented_calls(method_name):
    """Check if method calls from public API raise NotImplementedError"""
    engine = BaseEngine()
    with pytest.raises(NotImplementedError):
        method = getattr(engine, method_name)
        if inspect.iscoroutinefunction(method):
            await method()
        else:
            method()


def sync_view(message):
    return 'pong'


async def async_view(message):
    return 'pong'


@pytest.mark.asyncio
@pytest.mark.parametrize('view', [sync_view, async_view], ids=['sync', 'async'])  # noqa
async def test_get_response_from_views(view, settings):
    """
    Test if get_response can call an async/sync view and get its response.
    """

    engine = BaseEngine()
    engine.discovery_view = mock.Mock(return_value=view)
    response = await engine.get_response('ping')
    assert response.text == 'pong'


def test_prepare_response():
    engine = BaseEngine()
    response = engine.prepare_response('response', 'message')
    assert isinstance(response, Response)
    assert response.source == 'message'
    assert response.text == 'response'


def test_prepare_response_with_response_obj():
    expected_response = Response(source='message', text='response')
    engine = BaseEngine()
    response = engine.prepare_response(expected_response, 'message')
    assert response == expected_response


@mock.patch('bottery.platform.logger.error')
def test_prepare_response_none(mocked_error):
    """
    If response is not a str or a Response, it should returns None
    """

    engine = BaseEngine()
    assert engine.prepare_response(0, 'message') is None
    assert mocked_error.call_count == 1


def test_baseengine_handling_message():
    fake_handler = type('Handler', (object,), {
        'check': lambda msg: True,
        'view': True,
    })

    engine = BaseEngine()
    engine.registered_handlers = [fake_handler]
    returned_view = engine.discovery_view('new message')
    assert returned_view


def test_baseengine_handler_not_found():
    fake_handler = type('Handler', (object,), {
        'check': lambda msg: False,
        'view': True,
    })

    engine = BaseEngine()
    engine.registered_handlers = [fake_handler]
    returned_view = engine.discovery_view('new message')
    assert not returned_view


@pytest.mark.skip
@pytest.mark.asyncio
async def test_middlewares(settings):
    middleware = AsyncMock()
    settings.MIDDLEWARES = [middleware]

    engine = BaseEngine()
    engine.discovery_view = mock.Mock(return_value=lambda x: True)

    await engine.get_response('ping')
    assert middleware.call_count == 1
