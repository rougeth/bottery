class BasePlataform:

    def __init__(self, **kw):
        for item, value in kw.items():
            setattr(self, item, value)

    @property
    def handler(self):
        raise NotImplementedError('handler property not implemented')

    @property
    def path(self):
        return '/hook/{}/'.format(self.PLATAFORM)
