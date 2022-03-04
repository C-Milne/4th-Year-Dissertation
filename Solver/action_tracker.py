from Internal_Representation.action import Action
from Internal_Representation.Object import Object


class ActionTracker:
    def __init__(self, action: Action, parameters_used: dict[Object]):
        assert type(action) == Action
        assert type(parameters_used) == dict
        for k in parameters_used:
            assert type(parameters_used[k]) == Object
        self.action = action
        self.parameters_used = parameters_used

    def __str__(self):
        return_str = "{}".format(self.action.name)
        if len(self.parameters_used) > 0:
            return_str += " -"
            for k in self.parameters_used:
                return_str += " {}".format(self.parameters_used[k])
        return return_str
