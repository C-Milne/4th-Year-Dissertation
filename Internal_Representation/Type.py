class Type:
    def __init__(self, name, parent=None):
        assert type(name) == str
        self.name = name
        assert type(parent) == Type or parent is None
        self.parent = parent

    def __str__(self):
        return self.name
