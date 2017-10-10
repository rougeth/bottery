from bottery.views import ping


def test_ping():
    assert ping('any_string') == 'pong'
    assert ping(1) == 'pong'
    assert ping(None) == 'pong'
