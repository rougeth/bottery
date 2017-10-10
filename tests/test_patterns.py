from bottery.conf.patterns import DefaultPattern, Pattern


def test_pattern_instance():
    def view(): return 'Hello world'
    pattern = Pattern('ping', view)
    assert pattern.pattern == 'ping'
    assert pattern.view == view


def test_pattern_check_right_message():
    '''
    Check if Pattern class return the view when message checks with
    pattern.
    '''
    def view(): return 'Hello world'
    pattern = Pattern('ping', view)
    message = type('Message', (object,), {'text': 'ping'})
    result = pattern.check(message)
    assert result == view


def test_pattern_check_wrong_message():
    '''
    Check if Pattern class returns False when message doesn't
    check with pattern.
    '''
    def view(): return 'Hello world'
    pattern = Pattern('ping', view)
    message = type('Message', (object,), {'text': 'pong'})
    assert not pattern.check(message)


def test_default_pattern_instance():
    def view(): return 'Hello world'
    pattern = DefaultPattern(view)
    assert pattern.view == view


def test_default_pattern_check_message():
    '''
    Check if DefaultPattern class return the message if any pattern
    is given.
    '''
    def view(): return 'Hello world'
    pattern = DefaultPattern(view)
    message = type('Message', (object,), {'text': 'ping'})
    result = pattern.check(message)
    assert result == view
