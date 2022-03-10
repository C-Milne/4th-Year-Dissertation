from Internal_Representation.parameter import Parameter


class Predicate:
    """Defines predicates as they are given in the domain file.
    Looking for predicates relating to the state of a problem - see problem_predicate.py"""
    def __init__(self, name: str, parameters: list[Parameter] = None):
        assert type(name) == str
        self.name = name
        assert type(parameters) == list or parameters is None
        if type(parameters) == list:
            for i in parameters:
                assert type(i) == Parameter
        self.parameters = parameters

    def __eq__(self, other):
        if self.name == other:
            return True
        return False
