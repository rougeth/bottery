import pytest

from bottery.platform import BaseEngine


def test_baseengine_platform():
    """Check if platform attr raise NotImplementedError"""
    engine = BaseEngine()
    with pytest.raises(NotImplementedError):
        engine.platform


def test_baseengine_tasks():
    """Check if tasks attr raise NotImplementedError"""
    engine = BaseEngine()
    with pytest.raises(NotImplementedError):
        engine.tasks


def test_baseengine_build_message():
    """Check if build_message method raise NotImplementedError"""
    engine = BaseEngine()
    with pytest.raises(NotImplementedError):
        engine.build_message()


def test_baseengine_configure():
    """Check if configure method raise NotImplementedError"""
    engine = BaseEngine()
    with pytest.raises(NotImplementedError):
        engine.configure()
