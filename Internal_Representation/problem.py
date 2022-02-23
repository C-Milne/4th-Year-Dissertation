from Internal_Representation.Object import Object
from Internal_Representation.state import State
from Internal_Representation.Type import Type


class Problem:
    def __init__(self, domain):
        self.objects = {}
        self.initial_state = State(self)
        self.subtasks_to_execute = []
        self.domain = domain

    def add_object(self, ob):
        if type(ob) == list:
            for i in ob:
                self.add_object(i)
        else:
            assert type(ob) == Object
            self.objects[ob.name] = ob

    def add_to_initial_state(self, v):
        if len(v) == 1:
            self.initial_state.add_element(v[0])
        else:
            self.initial_state.add_element(v[0], v[1:])

    def add_subtasks_execute(self, param):
        self.subtasks_to_execute = param

    def get_object(self, name):
        return self.objects[name]

    def get_objects_of_type(self, param_type):
        if type(param_type) == str:
            param_type = self.domain.get_type(param_type)
        if type(param_type) != Type:
            raise TypeError("Unexpected type {}".format(type(param_type)))

        returnObs = []
        for o in self.objects:
            if self.objects[o].type == param_type:
                returnObs.append(self.objects[o])

        return returnObs
