import sys
import copy
from Internal_Representation.problem import Problem
"""The idea here is that this class will contain all information regarding the current state of the environment"""


class Model:
    def __init__(self, intake, solver, modifiers):
        self.current_state = {}
        if type(intake) == Problem:
            self.__populate_current_state_parser(intake)
        elif type(intake) == dict:
            self.__populate_current_state_dict(intake)
        else:
            raise TypeError("Unexpected parameter type {} for intake".format(type(intake)))
        self.solver = solver
        self.available_modifiers = modifiers
        self.actions_taken = []
        self.num_actions_taken = 0
        self.available_unused_modifiers = 0
        self.ready_modifiers = {}
        self.count_available_unused_modifiers()

    def __populate_current_state_parser(self, parser):
        self.current_state = parser.initial_state

    def __populate_current_state_dict(self, dict):
        self.current_state = dict

    def add_action(self, action):
        self.actions_taken.append(action)

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
                print(result)

    def __find_satisfying_params(self, modifier):
        """TODO - What about methods with no parameters"""
        # Can the model satisfy these parameters in current state?
        param_dict = {}
        for required_param_name in modifier.requirements:
            if required_param_name.startswith('forall-'):
                result = modifier.evaluate_preconditions(self, {})
                print(result)
            else:
                required_param = modifier.requirements[required_param_name]
                # Get objects that satisfy type
                for i in self.current_state.objects:
                    i = self.current_state.objects[i]
                    if self.__check_object_satifies_parameter(i, required_param):
                        if required_param_name not in param_dict.keys():
                            param_dict[required_param_name] = [i]
                        else:
                            param_dict[required_param_name].append(i)

        if param_dict == {}:
            return False
        return param_dict

    def __check_object_satifies_parameter(self, ob, required_param):
        if required_param['type'] is not None and required_param['type'] != ob.type:
            return False

        # Check if object satisfies predicates
        for pred in required_param['predicates']:
            if pred == "and" or pred == "not" or pred == "or":
                required_param = required_param['predicates'][pred]
                result = []
                for x in required_param.keys():
                    r = self.__check_object_satifies_parameter(ob, {'type': None, 'predicates': {x: required_param[x]}})
                    if type(r) == list:
                        result += r
                    else:
                        result.append(r)
                if pred == "and":
                    for i in result:
                        if i is False:
                            return False
                    return True
                elif pred == "not":
                    i = 0
                    while i < len(result):
                        result[i] = not result[i]
                        i += 1
                    return result
                else:
                    # pred == or
                    for i in result:
                        if i is True:
                            return True
                    return False
            else:
                indexes = self.current_state.get_indexes(pred)
                if indexes is None:
                    return False
                for index in indexes:
                    try:
                        if self.current_state.objects[self.current_state.elements[index][required_param['predicates'][pred]]] == ob:
                            return True
                    except IndexError:
                        continue
                return False

    def __check_proposed_parameters(self, param_dict_list, modifier, set_param_dict={}):
        num_params = len(param_dict_list.keys())
        if num_params == 1:
            k = list(param_dict_list.keys())[0]
            for i in param_dict_list[k]:
                pass_dict = self.__merge_dictionaries(set_param_dict, {k: i})
                result = modifier.evaluate_preconditions(self, pass_dict)
                if result:
                    if modifier.name in self.ready_modifiers:
                        self.ready_modifiers[modifier.name].append(pass_dict)
                    else:
                        self.ready_modifiers[modifier.name] = [pass_dict]
        else:
            k = param_dict_list.keys()[0]
            pass_dict = copy.deepcopy(param_dict_list)
            del pass_dict[k]
            for i in param_dict_list[k]:
                self.__check_proposed_parameters(pass_dict, modifier, self.__merge_dictionaries(set_param_dict, {k: i}))

    def __merge_dictionaries(self, a, b):
        c = a.copy()
        c.update(b)
        return c
