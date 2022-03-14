from Internal_Representation.predicate import Predicate


class Effects:
    class Effect:
        def __init__(self, predicate, parameters, negated):
            self.predicate = predicate
            self.parameters = parameters
            self.negated = negated

    class RunTimeEffect:
        def __init__(self, parameter):
            self.parameter = parameter

    def __init__(self):
        self.effects = []

    def add_effect(self, predicate: str, parameters: list[str] = [], negated: bool = False):
        """Params:  - predicate : name of predicate to be modified
                    - parameters : list of parameters belonging to predicate
                    - negated : True if 'not' statement encapsulates effect
                              : False otherwise"""
        assert type(predicate) == Predicate
        assert type(parameters) == list
        for p in parameters:
            assert type(p) == str
        assert type(negated) == bool
        self.effects.append(self.Effect(predicate, parameters, negated))

    def add_runtime_effect(self, parameter: str):
        """(:operator (!!assert ?g)
               ()
               ()
               (?g)
        :param parameter = '?g'
        """
        assert type(parameter) == str
        self.effects.append(self.RunTimeEffect(parameter))
