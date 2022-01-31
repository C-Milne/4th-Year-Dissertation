class Action:
    def __init__(self, params, parser):
        self.parser = parser
        self.name = None
        self.free_variables = []
        self.preconditions_predicates = {}
        self.preconditions_forall = []
        self.effect = []
        self.__parse_action(params)

    def __parse_action(self, params):
        i = 0
        while i < len(params):
            if i == 0:
                if type(params[i]) is str:
                    if not self.parser.name_assigned(params[i]):
                        self.name = params[i]
                    else:
                        raise NameError("Name '{}' is already assigned".format(params[i]))
                else:
                    raise TypeError("Action name must be a string.")
            else:
                if params[i] == ":parameters":
                    i += 1
                    self.__parse_parameters(params[i])
                elif params[i] == ":precondition":
                    i += 1
                    self.__parse_precondition(params[i])
                elif params[i] == ":effect":
                    i += 1
                    self.__parse_effect(params[i])

            i += 1

    def __parse_parameters(self, params):
        for i in params:
            self.__add_free_variable(i)

    def __parse_precondition(self, params):
        # Check for params is a list
        if not type(params) is list:
            raise TypeError("Precondition {} is not valid".format(params))
        i = 0

        if params[i] == 'forall':
            self.__add_precondition_forall()
        else:
            # This means the precondition is a predicate (variable)
            self.__add_precondition_predicate(params[i], params[i + 1])
            i += 2

    def __parse_effect(self, params):
        if not type(params) is list:
            raise TypeError("Effect {} is not valid".format(params))
            self.__add_effect(params)

    def __add_free_variable(self, v):
        """TODO - Check variable name is not already in use"""
        if v in self.free_variables:
            raise NameError("Name {} is already defined in action {}".format(v, self.name))
        self.free_variables.append(v)

    def __add_precondition_forall(self):
        raise EnvironmentError("Action 'for all' preconditions are not yet implemented.")

    def __add_precondition_predicate(self, key, val):
        """TODO - Check parameters"""
        self.preconditions_predicates[key] = val

    def __add_effect(self, val):
        self.effect.append(val)
