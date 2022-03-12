from Internal_Representation.Type import Type


class Parameter:
    def __init__(self, name, param_type=None):
        self.name = name
        if param_type is None:
            self.type = None
        elif type(param_type) == Type:
            # Type given
            self.type = param_type
        else:
            raise SyntaxError("Type {} is not recognised as a parameter type".format(type(param_type)))

    def __eq__(self, other):
        try:
            if self.param_type == other.param_type:
                return True
            else:
                return False
        except AttributeError:
            return False
