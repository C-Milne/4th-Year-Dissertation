from Internal_Representation.Object import Object
from Internal_Representation.state import State


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
        self.initial_state.add_element(v)

    def add_subtasks_execute(self, param):
        self.subtasks_to_execute = param

    def get_object(self, o):
        return self.objects[o]
