class Task:
    def __init__(self, params):
        self.name = None
        self.parameters = []
        self.methods = []
        self.__parse(params)

    def __parse(self, params):
        i = 0
        while i < len(params):
            if i == 0:
                if type(params[i]) == str:
                    self.name = params[i]
                else:
                    raise SyntaxError("Incorrect Definition of Task. A task needs a name")
            elif params[i] == ":parameters":
                i += 1
                self.__parse_parameters(params[i])
            else:
                raise KeyError("Unknown Identifier {} for Task {}".format(params[i], self.name))
            i += 1

    def __parse_parameters(self, params):
        """TODO - test"""
        for p in params:
            if type(p) == str:
                self.parameters.append(p)
            else:
                raise TypeError("Task Parameters Must be a String")

    def add_method(self, method):
        self.methods.append(method)
