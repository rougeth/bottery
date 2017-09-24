from bottery.views import ping

def test_ping():
    assert ping('ping') == 'pong'
