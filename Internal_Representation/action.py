from Internal_Representation.precondition import Precondition
from Internal_Representation.parameter import Parameter


class Action:
    def __init__(self, params, domain):
        self.domain = domain
        self.name = None
        self.parameters = []
        self.preconditions = None
        self.effect = []
        self.requirements = {}
        self.__parse_action(params)

    def __parse_action(self, params):
        """TODO - Checks for name ; Same as method"""
        i = 0
        while i < len(params):
            if i == 0:
                if type(params[i]) is str:
                    if not self.domain.name_assigned(params[i]):
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
        """TODO : Move this to parser"""
        for i in params:
            self.__add_parameter(i)

    def __parse_precondition(self, params):
        """TODO : Move this to parser"""
        # Check for params is a list
        if self.preconditions is None:
            self.preconditions = Precondition(params, self.domain)
        else:
            raise KeyError("Preconditions are already defined for Action {}".format(self.name))

    def __parse_effect(self, params):
        if not type(params) is list:
            raise TypeError("Effect {} is not valid".format(params))
        self.effect = params

    def __add_parameter(self, v):
        self.parameters = Parameter.parse_parameter_list(v, self.domain)

    def __add_precondition_forall(self):
        raise EnvironmentError("Action 'for all' preconditions are not yet implemented.")

    def __add_effect(self, val):
        self.effect = val

    def __prepare_requirements(self):
        for p in self.parameters:
            self.requirements[p.name] = {"type": p.param_type, "predicates": {}}
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
