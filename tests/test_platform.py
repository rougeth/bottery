import pytest

from bottery.platform import BasePlatform


def test_platform_baseplatform():
    platform = 'TEST_PLATFORM'
    bp = BasePlatform(platform=platform)

    assert bp.webhook_endpoint == '/hook/{}'.format(platform)
    assert not len(bp.tasks)

    with pytest.raises(Exception):
        bp.build_message()
