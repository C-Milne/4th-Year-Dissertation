import sys
import copy
from Internal_Representation.method import Method
from Internal_Representation.action import Action
from Internal_Representation.task import Task
from Internal_Representation.state import State
from Internal_Representation.subtasks import Subtasks
from Solver.action_tracker import ActionTracker

"""The idea here is that this class will contain all information regarding the current state of the environment"""


class Model:

    model_counter = 0

    def __init__(self, state: State, search_modifiers: list, problem=None,
                 waiting_subtasks: list = [], **kwargs):
        assert type(state) == State
        self.current_state = state
        assert type(search_modifiers) == list
        for m in search_modifiers:
            assert type(m) == Subtasks.Subtask and (
                        type(m.task) == Method or type(m.task) == Action or type(m.task) == Task)
        self.search_modifiers = search_modifiers
        self.problem = problem  # Problem object from internal rep
        self.waiting_subtasks = waiting_subtasks

        self.actions_taken = []
        self.operations_taken = []
        self.ranking = None
        self.num_models_used = None
        self.model_number = self.model_counter
        Model.model_counter += 1
        self.parent_model_number = None
        if "parent_num" in kwargs:
            if type(kwargs['parent_num']) == int:
                self.parent_model_number = kwargs['parent_num']

    def get_model_number(self) -> int:
        return self.model_number

    def set_parent_model_number(self, num: int):
        self.parent_model_number = num

    def set_ranking(self, ranking):
        assert type(ranking) == float or type(ranking) == int
        self.ranking = ranking

    def get_next_modifier(self):
        mod = self.search_modifiers.pop(0)
        return mod

    def get_ranking(self):
        return self.ranking

    def insert_modifier(self, modifier, index=0):
        assert type(modifier) == Task or type(modifier) == Method or type(modifier) == Action or \
               (type(modifier) == Subtasks.Subtask and type(modifier.task) == Action) or \
               (type(modifier) == Subtasks.Subtask and type(modifier.task) == Task)
        self.search_modifiers.insert(index, modifier)

    def add_operation(self, mod, parameters_used):
        assert type(mod) == Action or type(mod) == Task or type(mod) == Method
        op = ActionTracker(mod, parameters_used)
        if type(mod) == Action:
            self.actions_taken.append(op)
        self.operations_taken.append(op)

    def populate_actions_taken(self, v):
        self.actions_taken = v

    def populate_operations_taken(self, v):
        self.operations_taken = v

    def promote_waiting_subtask(self):
        if len(self.search_modifiers) == 0 and len(self.waiting_subtasks) > 0:
            self.search_modifiers.append(self.waiting_subtasks.pop(0))

    @staticmethod
    def reproduce_actions_taken(model):
        return_list = []
        for a in model.actions_taken:
            return_list.append(a)
        return return_list

    @staticmethod
    def reproduce_operations_list(model):
        return_list = []
        for a in model.operations_taken:
            return_list.append(a)
        return return_list

    @staticmethod
    def merge_dictionaries(a, b):
        c = a.copy()
        c.update(b)
        return c
