from bottery import patterns


def view():
    pass


def test_patterns():
    handler = patterns.Patterns()
    assert not handler.registered


def _test_decorators(decorator, handler):
    assert callable(decorator)
    assert decorator(view) == view
    assert handler.registered


def test_patterns_message():
    handler = patterns.Patterns()
    decorator = handler.message('ping')
    _test_decorators(decorator, handler)


def test_patterns_startswith():
    handler = patterns.Patterns()
    decorator = handler.startswith('ping')
    _test_decorators(decorator, handler)


def test_patterns_regex():
    handler = patterns.Patterns()
    decorator = handler.regex('ping')
    _test_decorators(decorator, handler)
