from Internal_Representation.precondition import Precondition
from Internal_Representation.parameter import Parameter


class Method:
    def __init__(self, params, domain):
        self.domain = domain
        self.name = None
        self.task = None
        self.parameters = []
        self.preconditions = None
        self.ordered_subtasks = None
        self.__parse(params)

    def evaluate_preconditions(self, model, param_dict):
        """:params  - model : proposed model
                    - params : list of parameters
        :returns    - True : if method can be run on the given model with given parameters
                    - False : Otherwise"""
        # Evaluate preconditions
        if self.preconditions is None:
            return True
        assert type(self.preconditions) == Precondition
        return self.preconditions.evaluate(model, param_dict)

    def get_parameters(self):
        return self.parameters

    def get_precondition(self):
        return self.preconditions

    def execute(self, model, param_dict, task=None):
        """TODO - Implement, 'or'; What if all ordered subtasks do NOT go through?"""
        """Execute this method on the given model
        :param  - model : to have actions carried out on
                - task : is the task to be carried out on the model
                        : Is None is all tasks are to be carried out
        :warning - This is a recursive function"""
        if task is None:
            if self.ordered_subtasks is not None:
                task = self.ordered_subtasks
            else:
                raise NotImplementedError("Support for partial ordered subtasks is not ready yet")

        # Do something
        if task[0] == "and":
            tasks_status = [self.execute(model, param_dict, x) for x in task[1:]]
        elif task[0] == "or":
            pass
        else:
            # Carry out action
            action = self.parser.get_action(task[0])
            action.execute(model, [param_dict[x] for x in task[1:]])

    def get_name(self):
        if self.name is None:
            return 'Unknown'
        return self.name

    def __parse(self, params):
        """ TODO - Implement support for :ordering """
        i = 0
        while i < len(params):
            if i == 0:
                self.__parse_name(params)
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

    def __parse_name(self, params):
        i = 0
        if type(params[i]) is str and len(params) % 2 == 1 and params[i][0] != ":":
            if not self.domain.name_assigned(params[i]):
                self.name = params[i]
            else:
                raise NameError("Name '{}' is already assigned".format(params[i]))
        else:
            raise SyntaxError("Error with Method name. Must be a string not beginning with ':'."
                              "\nPlease check your domain file.")

    def __parse_parameters(self, params):
        self.parameters += Parameter.parse_parameter_list(params, self.domain)

    def __parse_task(self, params):
        """TODO - Should we check if task is a valid action? ; Create a task class? - could link the method class to the task class"""
        if self.task is not None:
            if self.name is None:
                raise KeyError("Task has already been set for this method")
            else:
                raise KeyError("Task has already been set for method '{}'. Please check your domain file."
                               .format(self.name))

        if len(params) > 1:
            # Get the parameters required
            task_params = []
            for p in params[1:]:
                task_params.append(self.__get_parameter(p))

            self.task = self.domain.get_task(params[0], task_params)
        else:
            self.task = self.domain.get_task(params[0])

        if self.task is None:
            raise KeyError("Task '{}' is not defined. Please check your domain file.".format(params[0]))
        else:
            self.task.add_method(self)

    def __parse_precondition(self, params):
        self.preconditions = Precondition(params)

    def __parse_subtasks(self, params):
        if self.ordered_subtasks is not None:
            raise AttributeError("Ordered subtasks are already set for this method")
        self.ordered_subtasks = params

    def __get_parameter(self, name):
        for p in self.parameters:
            if p.name == name:
                return p
        raise RuntimeError("Parameter '{}' Not Found In Method '{}'".format(name, self.get_name()))
