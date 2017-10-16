import pytest

from bottery.platform import BaseEngine


@pytest.mark.parametrize('attr', ['platform', 'tasks'])
def test_baseengine_attrs(attr):
    """Check if attributes from the public API raise NotImplementedError"""
    engine = BaseEngine()
    with pytest.raises(NotImplementedError):
        getattr(engine, attr)


@pytest.mark.parametrize('method_name', ['build_message', 'configure'])
def test_baseengine_calls(method_name):
    """Check if method calls from public API raise NotImplementedError"""
    engine = BaseEngine()
    with pytest.raises(NotImplementedError):
        method = getattr(engine, method_name)
        method()
