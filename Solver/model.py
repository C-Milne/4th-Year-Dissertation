import sys
import copy
from Internal_Representation.method import Method
from Internal_Representation.action import Action
from Internal_Representation.task import Task
from Internal_Representation.state import State
from Internal_Representation.subtasks import Subtasks

"""The idea here is that this class will contain all information regarding the current state of the environment"""


class Model:
    def __init__(self, state: State, search_modifiers: list[Subtasks.Subtask], problem=None):
        assert type(state) == State
        self.current_state = state
        assert type(search_modifiers) == list
        for m in search_modifiers:
            assert type(m) == Subtasks.Subtask and (type(m.task) == Method or type(m.task) == Action or type(m.task) == Task)
        self.search_modifiers = search_modifiers
        self.problem = problem  # Problem object from internal rep

        self.actions_taken = []
        self.ranking = None

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

    def add_action_taken(self, action: Action):
        assert type(action) == Action
        self.actions_taken.append(action)

    def populate_actions_taken(self, v):
        self.actions_taken = v

    @staticmethod
    def reproduce_actions_taken(model):
        return_list = []
        for a in model.actions_taken:
            return_list.append(a)
        return return_list

    @staticmethod
    def merge_dictionaries(a, b):
        c = a.copy()
        c.update(b)
        return c
