from typing import List

from Internal_Representation.precondition import Precondition
from Internal_Representation.parameter import Parameter
from Internal_Representation.reg_parameter import RegParameter
from Internal_Representation.requirements import Requirements


class Modifier:
    def __init__(self, name, parameters: List[Parameter], preconditions=None):
        assert type(name) == str
        self.name = name
        assert type(parameters) == list
        for p in parameters:
            assert isinstance(p, Parameter)
        self.parameters = parameters
        assert type(preconditions) == Precondition or preconditions is None
        self.preconditions = preconditions

    def _prepare_requirements(self):
        req = Requirements(self.parameters, self.preconditions)
        self.requirements = req.prepare_requirements()

    def __str__(self):
        return self.name
