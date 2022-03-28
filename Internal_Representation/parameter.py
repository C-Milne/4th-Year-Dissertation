class Parameter:
    def __init__(self, name: str):
        assert type(name) == str or name is None
        self.name = name
