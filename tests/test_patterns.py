from bottery import patterns


def test_message_handler_check_positive_match():
    message = type('Message', (), {'text': 'ping'})
    handler = patterns.MessageHandler(pattern='ping')
    assert handler.check(message)


def test_message_handler_check_negative_match():
    message = type('Message', (), {'text': 'pong'})
    handler = patterns.MessageHandler(pattern='ping')
    assert not handler.check(message)


def test_message_handler_check_positive_match_with_case_sensitive():
    message = type('Message', (), {'text': 'Ping'})
    handler = patterns.MessageHandler(pattern='Ping',
                                      case_sensitive=True)
    assert handler.check(message)


def test_message_handler_check_negative_match_with_case_sensitive():
    message = type('Message', (), {'text': 'Ping'})
    handler = patterns.MessageHandler(pattern='ping',
                                      case_sensitive=True)
    assert not handler.check(message)


def test_startswith_handler_check_positive_match():
    message = type('Message', (), {'text': 'hello my friend'})
    handler = patterns.StartswithHandler(pattern='hello')
    assert handler.check(message)


def test_startswith_handler_check_negative_match():
    message = type('Message', (), {'text': 'Ping'})
    handler = patterns.StartswithHandler(pattern='hello my friend')
    assert not handler.check(message)


def test_startswith_handler_check_positive_match_with_sensitive():
    message = type('Message', (), {'text': 'Hello my friend'})
    handler = patterns.StartswithHandler(pattern='hello',
                                         case_sensitive=False)
    assert handler.check(message)


def test_startswith_handler_check_negative_match_with_sensitive():
    message = type('Message', (), {'text': 'pong'})
    handler = patterns.StartswithHandler(pattern='hello',
                                         case_sensitive=False)
    assert not handler.check(message)


def test_default_handler():
    message = type('Message', (), {'text': 'pong'})
    assert patterns.DefaultHandler().check(message)


def test_patterns_handlers():
    handler = patterns.PatternsHandler()
    assert not handler.registered


def test_patterns_handler_message():
    handler = patterns.PatternsHandler()
    decorator = handler.message('ping')

    def view(): 'pong'
    assert callable(decorator)
    assert decorator(view) == view
    assert handler.registered


def test_patterns_handler_startswith():
    handler = patterns.PatternsHandler()
    decorator = handler.startswith('ping')

    def view(): 'pong'
    assert callable(decorator)
    assert decorator(view) == view
    assert handler.registered
