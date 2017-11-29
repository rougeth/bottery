from unittest import mock

import pytest


@pytest.fixture
def token():
    return 'telegram-api-token'


@pytest.fixture
def server():
    return mock.MagicMock()


@pytest.fixture
def mock_session():
    def session(expected_response=None):
        class FakeResponse:
            async def json(self):
                return expected_response

        async def fake_api_call(*args, **kwargs):
            return FakeResponse()

        mocked_session = mock.MagicMock()
        mocked_session.post.return_value = fake_api_call()
        return mocked_session
    return session


@pytest.fixture
def session(mock_session):
    return mock_session({})


@pytest.fixture
def new_message_data():
    return {
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
