from Internal_Representation.action import Action
from Internal_Representation.task import Task
from Internal_Representation.method import Method
from Internal_Representation.Object import Object


class ActionTracker:
    def __init__(self, action: Action, parameters_used: dict[str, Object]):
        assert type(action) == Action or type(action) == Method or type(action) == Task
        assert type(parameters_used) == dict
        for k in parameters_used:
            assert type(parameters_used[k]) == Object
        self.action = action
        self.parameters_used = parameters_used

    def __eq__(self, other):
        if self.action != other.action:
            return False
        if len(self.parameters_used) != len(other.parameters_used):
            return False
        for i in self.parameters_used:
            if not i in other.parameters_used:
                return False
            elif self.parameters_used[i] != other.parameters_used[i]:
                return False
        return True

    def __str__(self):
        return_str = "{}".format(self.action.name)
        if len(self.parameters_used) > 0:
            return_str += " -"
            for k in self.parameters_used:
                return_str += " {}".format(self.parameters_used[k])
        return return_str
