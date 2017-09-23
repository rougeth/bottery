from bottery.conf.patterns import Pattern


def test_pattern_instance():
    view = lambda: 'Hello world'
    pattern = Pattern('ping', view)
    assert pattern.pattern == 'ping'
    assert pattern.view == view


def test_pattern_check_right_message():
    '''
    Check if Pattern class return the view when message checks with
    pattern.
    '''
    view = lambda: 'Hello world'
    pattern = Pattern('ping', view)
    message = type('Message', (object,), {'text': 'ping'})
    result = pattern.check(message)
    assert result == view


def test_pattern_check_wrong_message():
    '''
    Check if Pattern class returns False when message doesn't
    check with pattern.
    '''
    view = lambda: 'Hello world'
    pattern = Pattern('ping', view)
    message = type('Message', (object,), {'text': 'pong'})
    assert not pattern.check(message)
