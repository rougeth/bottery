from bottery import patterns


def test_patterns():
    handler = patterns.Patterns()
    assert not handler.registered


def test_patterns_message():
    handler = patterns.Patterns()
    decorator = handler.message('ping')

    def view():
        pass

    assert callable(decorator)
    assert decorator(view) == view
    assert handler.registered


def test_patterns_startswith():
    handler = patterns.Patterns()
    decorator = handler.startswith('ping')

    def view():
        pass

    assert callable(decorator)
    assert decorator(view) == view
    assert handler.registered
