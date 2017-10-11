from bottery.views import pong


def test_pong():
    assert pong('any_string') == 'pong'
    assert pong(1) == 'pong'
    assert pong(None) == 'pong'
