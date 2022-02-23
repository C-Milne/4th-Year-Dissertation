from Internal_Representation.precondition import Precondition
from Internal_Representation.parameter import Parameter


class Method:
    def __init__(self, params, domain):
        self.domain = domain
        self.name = None
        self.task = None
        self.parameters = []
        self.preconditions = None
        self.subtasks = {}
        self.ordered_subtasks = []
        self.requirements = {}
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

    def get_number_parameters(self):
        return len(self.parameters)

    def get_precondition(self):
        return self.preconditions

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
                elif params[i] == ":ordering":
                    i += 1
                    self.__order_subtasks(params[i])
                else:
                    raise TypeError("Unknown token {}".format(params[i]))

            i += 1
        self.__prepare_requirements()

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
        """TODO - Move this to parser ; Should we check if task is a valid action? ; Create a task class? - could link the method class to the task class"""
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
        """TODO : Move to parser"""
        self.preconditions = Precondition(params, self.domain)

    def __parse_subtasks(self, params):
        """TODO : Is this an action? - if so make reference to action objects"""
        if len(self.ordered_subtasks) > 1:
            raise AttributeError("Ordered subtasks are already set for this method")
        for i in params:
            if i == "and":
                continue
            if type(i) == list and len(i) > 1 and type(i[1]) == list:
                label = i[0]
                task = i[1]
                self.subtasks[label] = task
            else:
                self.ordered_subtasks.append(i)

    def __order_subtasks(self, params):
        for i in params:
            if i == "and":
                continue
            assert type(i) == list
            operator = i[0]     # < or >
            taskA = self.subtasks[i[1]]
            taskB = self.subtasks[i[2]]
            if operator == ">":
                taskA, taskB = taskB, taskA

            # TaskA comes before taskB
            if not taskA in self.ordered_subtasks and not taskB in self.ordered_subtasks:
                self.ordered_subtasks.append(taskA)
                self.ordered_subtasks.append(taskB)
            elif not taskA in self.ordered_subtasks:
                # Get index of taskB
                taskB_index = self.ordered_subtasks.index(taskB)
                self.ordered_subtasks.insert(taskB_index, taskA)
            else:
                self.ordered_subtasks.append(taskB)

    def __get_parameter(self, name):
        for p in self.parameters:
            if p.name == name:
                return p
        raise RuntimeError("Parameter '{}' Not Found In Method '{}'".format(name, self.get_name()))

    def __prepare_requirements(self):
        for p in self.parameters:
            self.requirements[p.name] = {"type": p.param_type, "predicates": {}}
        if self.preconditions is not None:
            self.__prepare_prelayer = []
            self.__prepare_requirements_precons()
            del self.__prepare_prelayer

    def __prepare_requirements_precons(self, predicates=None):
        i = 0
        if predicates is None:
            predicates = self.preconditions.conditions
        pred_name = None
        add_prelayer = False
        while i < len(predicates):
            p = predicates[i]
            if type(p) == list:
                self.__prepare_requirements_precons(p)

            if p == "and" or p == "or" or p == "not" or p == "forall":
                self.__prepare_prelayer.append(p)
                add_prelayer = True

            elif p[0] != "?":
                pred_name = p
            elif len(self.__prepare_prelayer) > 0 and self.__prepare_prelayer[-1] == "forall":
                if type(predicates) == list and predicates[0][0] == "?":
                    # Create new forall clause in requirements
                    req_name = "forall-{}-".format(predicates[2])
                    num = 1
                    while req_name + str(num) in self.requirements.keys():
                        num += 1
                    self.requirements[req_name + str(num)] = {}
                    i += 3
                else:
                    for k in self.requirements.keys():
                        if k.startswith("forall") and self.requirements[k] == {}:
                            self.requirements[k] = {pred_name: p}
            else:
                dict = self.requirements[p]["predicates"]
                for l in self.__prepare_prelayer:
                    if l not in dict.keys():
                        dict[l] = {}
                        dict = dict[l]
                    else:
                        dict = dict[l]
                dict[pred_name] = i
            i += 1

        if add_prelayer:
            self.__prepare_prelayer = self.__prepare_prelayer[:-1]
