import sys
# from Internal_Representation.modifier import Modifier
from Internal_Representation.effects import Effects
if 'Internal_Representation.modifier' in sys.modules:
    Modifier = sys.modules['Internal_Representation.modifier'].Modifier
else:
    from Internal_Representation.modifier import Modifier


class Action(Modifier):
    def __init__(self, name, parameters, preconditions, effects: Effects):
        super().__init__(name, parameters, preconditions)
        assert type(effects) == Effects or effects is None
        self.effects = effects

    def get_effects(self):
        return self.effects
