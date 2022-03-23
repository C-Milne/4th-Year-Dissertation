from typing import List

from Internal_Representation.precondition import Precondition
from Internal_Representation.parameter import Parameter
from Internal_Representation.reg_parameter import RegParameter
from Internal_Representation.requirements import Requirements


class Modifier:
    Precondition = Precondition

    def __init__(self, name, parameters: List[Parameter], preconditions=None):
        assert type(name) == str
        self.name = name
        assert type(parameters) == list
        for p in parameters:
            assert isinstance(p, Parameter)
        self.parameters = parameters
        assert type(preconditions) == Precondition or preconditions is None
        self.preconditions = preconditions
        self.requirements = None

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def get_parameters(self):
        return self.parameters

    def add_precondtions(self, precons: Precondition):
        assert type(precons) == Precondition or precons is None
        if self.preconditions is None:
            self.preconditions = precons
        else:
            raise TypeError("Preconditions are already set for this modifier")

    def get_number_parameters(self):
        return len(self.parameters)

    def __str__(self):
        return self.name
