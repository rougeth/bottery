import sys
from unittest import mock

import pytest
from aiohttp import web

from bottery.conf import Settings
from bottery.message import Message
from bottery.platform.messenger import engine as Engine


@pytest.fixture
def engine():
    server = web.Application()
    return Engine(token='token', session='session', server=server,
                  engine_name='messenger', settings=Settings())

@pytest.fixture
async def configured_engine(engine):
    engine.settings.HOSTNAME = 'localhost'
    await engine.configure()
    return engine

@pytest.fixture
def client(loop, test_client, configured_engine):
    return loop.run_until_complete(test_client(configured_engine.server))


@pytest.fixture
def message_data():
    return {
        'message': {
            'mid': '8797115104105110103116111110',
            'text': 'I have a dream',
        },
        'sender': {
            'id': '779711411610511032761171161041011143275105110103327411446'
        },
        'timestamp': '1963-08-28',
        'raw': '',
    }


def test_build_message_without_data(engine):
    assert not engine.build_message(None)


def test_build_message_with_invalid_data(engine):
    with pytest.raises(KeyError):
        engine.build_message({'invalid': 'data'})


def test_build_message_with_invalid_data(engine, message_data):
    message = engine.build_message(message_data)
    assert isinstance(message, Message)


@pytest.mark.asyncio
async def test_configure_missing_hostname(engine):
    with pytest.raises(Exception):
        await engine.configure()


@pytest.mark.asyncio
async def test_configure(engine):
    engine.settings.HOSTNAME = 'localhost'
    await engine.configure()

    routes = engine.server.router.routes()
    handlers = set(route.handler for route in list(routes))
    methods = set(route.method for route in list(routes))

    assert len(routes) == 3
    assert methods == {'POST', 'GET', 'HEAD'}
    assert handlers == {engine.verify_webhook, engine.webhook}


async def test_webhook_unexpected_request(client):
    response = await client.post('/messenger', json={'object': 'invalid'})
    assert response.status == 400


async def test_webhook(test_client, configured_engine):
    async def handler(*args, **kwargs):
        pass

    configured_engine.message_handler = mock.MagicMock()
    configured_engine.message_handler.return_value = handler()

    client = await test_client(configured_engine.server)

    request = {
        'object': 'page',
        'entry': [{
            'messaging': 'message'
        }]
    }
    response = await client.post('/messenger', json=request)

    assert response.status == 200
    assert await response.text() == 'EVENT_RECEIVED'
    assert configured_engine.message_handler.called
