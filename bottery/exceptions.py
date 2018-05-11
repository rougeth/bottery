class ImproperlyConfigured(Exception):
    """Bottery is somehow improperly configured"""
    pass


class ValidationError(Exception):
    pass


class BotteryDeprecationWarning(Warning):
    pass
