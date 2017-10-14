import pytest

from bottery.platform import BaseEngine


def test_platform_baseplatform():
    platform = 'TEST_PLATFORM'
    bp = BaseEngine(platform=platform)

    assert bp.webhook_endpoint == '/hook/{}'.format(platform)
    assert not len(bp.tasks)

    with pytest.raises(Exception):
        bp.build_message()
