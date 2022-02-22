from Internal_Representation.Type import Type


class Parameter:
    def __init__(self, name, domain, param_type=None):
        self.name = name
        if param_type is None:
            self.param_type = None
        elif type(param_type) == Type:
            # Type given
            self.param_type = Type
        elif type(param_type) == str:
            # Get Type object
            type_found = domain.get_type(param_type)
            if type_found is False:
                raise SyntaxError("Type {} Not Found".format(param_type))
            self.param_type = type_found
        else:
            raise SyntaxError("Type {} is not recognised as a parameter type".format(type(param_type)))

    @staticmethod
    def parse_parameter_list(params, domain):
        """TODO : test this - check parameter name not already in use"""
        """Parses list of parameters and returns a list of parameters"""
        """TODO - test"""
        i = 0
        l = len(params)
        param_list = []
        while i < l:
            p = params[i]
            param_type = None
            if i + 1 < l:
                if params[i + 1] == "-":
                    param_type = params[i + 2]
                    i += 2
            if type(p) == str:
                param_list.append(Parameter(p, domain, param_type))
            else:
                raise TypeError("Task Parameters Must be a String")
            i += 1
        return param_list

    def __eq__(self, other):
        if self.param_type == other.param_type:
            return True
        else:
            return False
