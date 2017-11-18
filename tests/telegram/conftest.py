from unittest import mock

import pytest


@pytest.fixture
def token():
    return 'telegram-api-token'


@pytest.fixture
def session():

    async def fake_post(*args, **kwargs):
        pass

    mocked_session = mock.MagicMock()
    mocked_session.post.return_value = fake_post()
    return mocked_session
