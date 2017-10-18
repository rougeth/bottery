integrations = ['telegram']


class Response():
    def __init__(self, *args, **kw):
        for integration in integrations:
            i = kw.get(integration, None)

            if i:
                setattr(self, integration, i)
