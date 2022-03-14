from Internal_Representation.precondition import Precondition
from Internal_Representation.parameter import Parameter
from Internal_Representation.reg_parameter import RegParameter


class Modifier:
    def __init__(self, name, parameters: list[Parameter], preconditions=None):
        assert type(name) == str
        self.name = name
        assert type(parameters) == list
        for p in parameters:
            assert isinstance(p, Parameter)
        self.parameters = parameters
        assert type(preconditions) == Precondition or preconditions is None
        self.preconditions = preconditions

    def _prepare_requirements(self):
        for p in self.parameters:
            if type(p) == RegParameter:
                self.requirements[p.name] = {"type": p.type, "predicates": {}}
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
                if p not in self.requirements:
                    self.requirements[p] = {"type": None, "predicates": {}}
                
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

    def __str__(self):
        return self.name
