"""Exception classes for Bottery"""


class BotteryException(Exception):
    """A base class for all Bottery exceptions for easier catching."""
    pass


class ImproperlyConfigured(BotteryException):
    """Bottery is somehow improperly configured"""
    pass
