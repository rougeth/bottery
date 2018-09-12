from unittest import mock

import pytest

from bottery.conf import UserSettingsHolder, lazy_obj_method


@pytest.mark.parametrize('wrapped,expected_result', (
    (False, True), (True, False),
))
def test_lazy_obj_method(wrapped, expected_result):
    class Settings:
        _wrapped = wrapped
        _setup = mock.Mock()
        __dir__ = lazy_obj_method(dir)

    settings = Settings()
    dir(settings)

    assert settings._setup.called is expected_result
