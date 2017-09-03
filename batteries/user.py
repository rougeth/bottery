class User:
    def __init__(self, id, first_name, last_name=None, username=None,
                 language=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language = language
