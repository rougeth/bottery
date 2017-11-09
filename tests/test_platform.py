import inspect

import pytest

from bottery.platform import BaseEngine


@pytest.mark.parametrize('attr', ['platform', 'tasks'])
def test_baseengine_not_implemented_attrs(attr):
    """Check if attributes from the public API raise NotImplementedError"""
    engine = BaseEngine()
    with pytest.raises(NotImplementedError):
        getattr(engine, attr)


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
async def test_get_response_from_views(view):
    """
    Test if get_response can call an async/sync view and get its response.
    """

    engine = BaseEngine()
    response = await engine.get_response(view, 'ping')
    assert response == 'pong'
