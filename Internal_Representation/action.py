from Internal_Representation.modifier import Modifier
from Internal_Representation.effects import Effects


class Action(Modifier):
    def __init__(self, name, parameters, preconditions, effects: Effects):
        super().__init__(name, parameters, preconditions)
        assert type(effects) == Effects or effects is None
        self.effects = effects

        self.requirements = {}
        super(Action, self)._prepare_requirements()
