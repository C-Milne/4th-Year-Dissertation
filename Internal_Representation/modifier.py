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

    def _prepare_requirements(self):
        req = Requirements(self.parameters, self.preconditions)
        self.requirements = req.prepare_requirements()
        self._compare_requirements_parameters()

    def _compare_requirements_parameters(self):
        """Check that all the parameters listed in the requirements are present in the parameters list.
        If any are missing; add them"""
        for p in self.requirements:
            if p.startswith('forall'):
                continue
            if p not in [x.name for x in self.parameters]:
                self.parameters.append(RegParameter(p, self.requirements[p]['type']))

    def __str__(self):
        return self.name
