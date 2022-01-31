from Parsers.HDDL.precondition import Precondition


class Method:
    def __init__(self, params, parser):
        self.parser = parser
        self.name = None
        self.task = None
        self.parameters = []
        self.preconditions = []
        self.ordered_subtasks = None
        self.__parse(params)

    def __parse(self, params):
        """ TODO - Implement support for :ordering """
        i = 0
        while i < len(params):
            if i == 0:
                if type(params[i]) is str:
                    if not self.parser.name_assigned(params[i]):
                        self.name = params[i]
                    else:
                        raise NameError("Name '{}' is already assigned".format(params[i]))
                else:
                    raise TypeError("Method name must be a string.")
            else:
                if params[i] == ":parameters":
                    i += 1
                    self.__parse_parameters(params[i])
                elif params[i] == ":task":
                    i += 1
                    self.__parse_task(params[i])
                elif params[i] == ":precondition":
                    i += 1
                    self.__parse_precondition(params[i])
                elif params[i] == ":ordered-subtasks" or params[i] == ":ordered-tasks" or params[i] == ":subtasks" or \
                        params[i] == ":tasks":
                    i += 1
                    self.__parse_subtasks(params[i])
                else:
                    raise TypeError("Unknown token {}".format(params[i]))

            i += 1

    def __parse_parameters(self, params):
        for param in params:
            self.parameters.append(param)

    def __parse_task(self, params):
        """TODO - Should we check if task is a valid action?"""
        if self.task is not None:
            raise NameError("Task has already been set for this method")

        if type(params) is not list:
            raise TypeError("Invalid type for task")

        self.task = params

    def __parse_precondition(self, params):
        self.preconditions.append(Precondition(params))

    def __parse_subtasks(self, params):
        if self.ordered_subtasks is not None:
            raise AttributeError("Ordered subtasks are already set for this method")
        self.ordered_subtasks = params
