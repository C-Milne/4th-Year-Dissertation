class Type:
    def __init__(self, name, parent=None):
        """TODO - Implement Type hierarchy"""
        assert type(name) == str
        self.name = name
        assert type(parent) == Type or parent is None
        self.parent = parent
