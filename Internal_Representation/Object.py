from Internal_Representation.Type import Type


class Object:
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

    def set_type(self, t):
        assert type(t) == Type
        self.type = t
