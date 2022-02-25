class Effects:
    class Effect:
        def __init__(self, predicate, parameters, negated):
            self.predicate = predicate
            self.parameters = parameters
            self.negated = negated

    def __init__(self):
        self.effects = []

    def add_effect(self, predicate: str, parameters: list = [], negated: bool = False):
        """Params:  - predicate : name of predicate to be modified
                    - parameters : list of parameters belonging to predicate
                    - negated : True if 'not' statement encapsulates effect
                              : False otherwise"""
        assert type(predicate) == str
        assert type(parameters) == list
        assert type(negated) == bool
        self.effects.append(self.Effect(predicate, parameters, negated))
