class Type:
    def __init__(self, name, parent=None):
        assert type(name) == str
        self.name = name
        assert type(parent) == Type or parent is None
        if parent is None:
            self.parents = []
        else:
            self.parents = [parent]

    def add_parent(self, p):
        if p not in self.parents:
            self.parents.append(p)

    def __str__(self):
        return self.name
