from Internal_Representation.predicate import Predicate
from Internal_Representation.reg_parameter import RegParameter
from Internal_Representation.precondition import Precondition


class DerivedPredicate(Predicate):
    def __init__(self, name: str, parameters: list[RegParameter] = None):
        super().__init__(name, parameters)
        self.conditions = []

    def add_condition(self, condition: Precondition):
        assert type(condition) == Precondition
        self.conditions.append(condition)
