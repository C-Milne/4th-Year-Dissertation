from Internal_Representation.Object import Object
from Internal_Representation.state import State
from Internal_Representation.Type import Type
from Internal_Representation.precondition import Precondition
from Solver.model import Model
from Internal_Representation.subtasks import Subtasks


class Problem:
    def __init__(self, domain):
        self.objects = {}
        self.initial_state = State(self)
        self.subtasks_to_execute = []
        self.domain = domain
        self.goal_conditions = None

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
        self.subtasks_to_execute = Subtasks(param, self.domain)

    def order_subtasks(self, orderings):
        self.subtasks_to_execute.order_subtasks(orderings)

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

    def add_goal_conditions(self, cons):
        assert type(cons) == Precondition
        self.goal_conditions = cons

    def evaluate_goal(self, model: Model):
        if self.goal_conditions is None:
            return None
        return self.goal_conditions.evaluate(model, self.objects)