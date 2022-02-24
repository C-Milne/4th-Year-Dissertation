import sys
import copy
from Internal_Representation.method import Method
from Internal_Representation.action import Action
from Internal_Representation.task import Task
"""The idea here is that this class will contain all information regarding the current state of the environment"""


class Model:
    def __init__(self, intake, solver, modifier, given_params:dict=None):
        self.current_state = {}
        self.solver = solver
        self.actions_taken = []

        self.__populate_current_state(intake)

        self.ready_modifiers = {}
        self.ready_modifiers_refs = {}

        if not given_params is None:
            # Check if modifier is ready
            self.__check_proposed_parameters(given_params, modifier)

        self.num_actions_taken = 0
        self.ready_unused_modifiers = 0
        self.__ranking = None

        if len(self.ready_modifiers.keys()) == 0:
            self.count_available_unused_modifiers()

    def __populate_current_state(self, intake):
        if self.solver.check_type_problem(intake):
            self.__populate_current_state_problem(intake)
        elif type(intake) == dict:
            self.__populate_current_state_dict(intake)
        else:
            raise TypeError("Unexpected parameter type {} for intake".format(type(intake)))

    def __populate_current_state_problem(self, parser):
        self.current_state = parser.initial_state

    def __populate_current_state_dict(self, dict):
        self.current_state = dict

    def add_action(self, action):
        self.actions_taken.append(action)

    def add_ready_modifier(self, modifier_name, param_dict, index):
        if type(modifier_name) == list:
            modifier_name = modifier_name[0]

        if type(modifier_name) == Method or type(modifier_name) == Action or type(modifier_name) == Task:
            modifier = modifier_name
        else:
            modifier = self.solver.domain.get_modifier(modifier_name)

        # Check all parameters were given
        if len(param_dict) != len(modifier.parameters):
            raise ValueError("Not enough parameters given")

        # Add to ready modifiers
        dict = {}
        current_keys = list(self.ready_modifiers.keys())

        # Maintain any modifiers already in place
        for i in range(index):
            dict = self.__merge_dictionaries(dict, {current_keys[i]: self.ready_modifiers[current_keys[i]]})

        # Add new modifier
        if type(modifier_name) != str:
            modifier_name = modifier_name.name

        dict = self.__merge_dictionaries(dict, {modifier.name: param_dict})

        # Add remaining modifiers
        for i in range(index, len(current_keys)):
            dict = self.__merge_dictionaries(dict, {current_keys[i]: self.ready_modifiers[current_keys[i]]})
        self.ready_modifiers = dict
        self.ready_modifiers_refs[modifier.name] = modifier

    def pop_ready_modifier(self):
        key = list(self.ready_modifiers.keys())[0]
        del self.ready_modifiers[key]
        del self.ready_modifiers_refs[key]

    def count_available_unused_modifiers(self):
        """TODO : Test this"""
        # Count which methods are available to the model in the current state
        for i in self.available_modifiers:
            # Can the model satisfy these parameters in current state?
            result = self.__find_satisfying_params(i)
            if not result:
                continue
            else:
                self.__check_proposed_parameters(result, i)

    def __check_proposed_parameters(self, param_dict_list, modifier, set_param_dict={}):
        """Parameters   - param_dict_list : Dictionary of lists for each possible parameter - {'?a':[ob1, ob2, ob3]...}
                        - modifier : Task, action, or method
                        - set_param_dict : Internal use only"""
        num_params = len(param_dict_list.keys())
        if num_params == 0:
            if len(set_param_dict.keys()) == modifier.get_number_parameters():
                result = modifier.evaluate_preconditions(self, set_param_dict)
            else:
                result = False

            if result:
                if modifier.name in self.ready_modifiers:
                    self.ready_modifiers[modifier.name].append(set_param_dict)
                else:
                    self.ready_modifiers[modifier.name] = [set_param_dict]
                    self.ready_modifiers_refs[modifier.name] = modifier
        else:
            k = list(param_dict_list.keys())[0]
            pass_dict = copy.deepcopy(param_dict_list)
            del pass_dict[k]
            if type(k) == list:
                for i in param_dict_list[k]:
                    self.__check_proposed_parameters(pass_dict, modifier, self.__merge_dictionaries(set_param_dict, {k: i}))
            else:
                self.__check_proposed_parameters(pass_dict, modifier, self.__merge_dictionaries(set_param_dict, {k: param_dict_list[k]}))

    def set_ranking(self, v):
        assert type(v) == float or type(v) == int
        self.__ranking = v

    def get_ranking(self):
        return self.__ranking

    def get_current_state_predicates(self):
        return self.current_state.get_predicates()

    def get_predicate_index(self, name):
        return self.current_state.get_indexes(name)

    def __merge_dictionaries(self, a, b):
        c = a.copy()
        c.update(b)
        return c
