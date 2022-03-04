import copy
import sys
from Solver.model import Model
from Solver.search_queue import SearchQueue
from Internal_Representation.method import Method
from Internal_Representation.action import Action
from Internal_Representation.task import Task
from Internal_Representation.parameter import Parameter
from Internal_Representation.subtasks import Subtasks
from Internal_Representation.Object import Object
from Internal_Representation.problem_predicate import ProblemPredicate
from Internal_Representation.state import State


class Solver:
    def __init__(self, domain, problem, model=None):
        self.domain = domain
        self.problem = problem

        self.search_models = SearchQueue()

    def solve(self):
        task_counter = 0
        search_result = None
        for subT in self.problem.subtasks.get_tasks():
            if subT == "and" or subT == "or":
                continue

            print("Subtask:", task_counter, "-", subT.get_name() + str([p.name for p in subT.parameters]))

            # Prepare search_models
            self.search_models.clear()

            # Create initial search model
            param_dict = self.__generate_param_dict(subT.task, subT.parameters)
            subT.add_given_parameters(param_dict)
            if search_result is None:
                initial_model = Model(State.reproduce(self.problem.initial_state), [subT], self.problem)
            else:
                initial_model = Model(State.reproduce(search_result.current_state), [subT], self.problem)
            self.search_models.add(initial_model)

            search_result = self.__search()
            if search_result is None:
                print("No plan Found")
                sys.exit()
            task_counter += 1
        return search_result

    def __search(self, step_control=False):
        """:parameter   - step_control  - If True, then loop will only execute once"""
        while True:
            # New model to operate on
            search_model = self.search_models.pop()

            # Check what needs to be done to this model
            next_modifier = search_model.get_next_modifier()
            assert type(next_modifier) == Subtasks.Subtask

            if type(next_modifier.task) == Task:
                self.__expand_task(next_modifier, search_model)
            elif type(next_modifier.task) == Method:
                self.__expand_method(next_modifier, search_model)
            elif type(next_modifier.task) == Action:
                self.__expand_action(next_modifier, search_model)
            else:
                raise NotImplementedError

            # Loop exit conditions
            if self.search_models.get_num_search_models() == 0:
                if self.search_models.get_num_completed_models() == 1:
                    return self.search_models.get_sole_completed_model()
                break
            elif step_control:
                break
            # Also check goal conditions

    def __expand_task(self, subtask: Subtasks.Subtask, search_model: Model):
        # For each method, create a new search model
        for method in subtask.task.methods:
            # Check parameters for new_model
            # Is all the required parameters present or do some need to be chosen
            parameters = {}
            for k in subtask.given_params.keys():
                parameters[k] = subtask.given_params[k]

            comparison_result = self.__compare_parameters(method, parameters)

            if not comparison_result[0]:
                found_params = self.__find_satisfying_parameters(search_model, method, parameters)
            else:
                found_params = [parameters]

            for param_option in found_params:
                # Check preconditions of new_model
                result = None
                for k in method.parameters:
                    if not k.name in param_option:
                        result = False

                if result is None:
                    result = method.preconditions.evaluate(search_model, param_option)

                if result:
                    subT = Subtasks.Subtask(method, method.parameters)
                    subT.add_given_parameters(param_option)
                    # Create new model and add to search_models
                    new_model = Model(State.reproduce(search_model.current_state),
                                      [subT] + search_model.search_modifiers, self.problem)
                    self.search_models.add(new_model)

    def __expand_method(self, subtask: Subtasks.Subtask, search_model: Model):
        # Add actions to search model - with parameters
        i = 0
        if subtask.task.subtasks is None:
            return
        for mod in subtask.task.subtasks.tasks:
            assert type(mod.task) == Action or type(mod.task) == Task

            mod = Subtasks.Subtask(mod.task, mod.parameters)

            # Check parameter count
            parameters = {}
            param_keys = [p.name for p in mod.parameters]
            action_keys = [p.name for p in mod.task.parameters]
            for j in range(len(action_keys)):
                parameters[action_keys[j]] = subtask.given_params[param_keys[j]]

            comparison_result = self.__compare_parameters(mod.task, parameters)
            assert comparison_result[0] == True

            mod.add_given_parameters(parameters)

            # Add mod to search_model
            search_model.insert_modifier(mod, i)
            i += 1
        self.search_models.add(search_model)

    def __expand_action(self, subtask: Subtasks.Subtask, search_model: Model):
        assert type(subtask) == Subtasks.Subtask and type(subtask.task) == Action

        # Check preconditions
        if not subtask.task.preconditions.evaluate(search_model, subtask.given_params):
            return

        for eff in subtask.task.effects.effects:
            param_list = []
            for i in eff.parameters:
                param_list.append(subtask.given_params[i])
            if eff.negated:
                # Predicate needs to be removed
                search_model.current_state.remove_element(eff.predicate, param_list)
            else:
                # Predicate needs to be added
                new_predicate = ProblemPredicate(eff.predicate, param_list)
                search_model.current_state.add_element(new_predicate)

        search_model.add_action_taken(subtask.task)
        self.search_models.add(search_model)

    def __compare_parameters(self, method: Method, parameters: dict[Object]):
        """ Compares if all the parameters required for a method are given
        :parameter  - method : Method
        :parameter  - parameters : {'?objective1': Object, '?mode': Object}
        :returns    - [True] : if parameters match what is required by method
        :returns    - [False, missing_params] : otherwise. missing_params = ["name1", "name2" ... ]
        """
        assert type(method) == Method or type(method) == Action or type(method) == Task
        assert type(parameters) == dict
        for p in parameters:
            assert type(parameters[p]) == Object

        missing_params = []
        for p in method.parameters:
            # Check if a parameter corresponding to p is in parameters dictionary
            if not p.name in parameters:
                missing_params.append(p.name)
                continue
            if p.type != parameters[p.name].type:
                raise TypeError("Parameter {} of type {} does not match required type {}"
                                .format(p.name, parameters[p.name].type.name, p.type))
        if len(missing_params) == 0:
            return [True]
        return [False, missing_params]

    def __find_satisfying_parameters(self, model: Model, method: Method, param_dict: dict[Object] = {}):
        """Find parameters to satisfy a modifier
        :parameter model:
        :parameter method:
        :parameter param_dict:    : parameters already set - {'?objective': Object, '?mode': Object}
        :return: list of possible combinations of parameters
        """
        assert type(model) == Model and type(method) == Method and type(param_dict) == dict
        for required_param_name in method.requirements:
            if required_param_name.startswith('forall-'):
                raise NotImplementedError
            elif required_param_name in param_dict:
                continue
            else:
                requirements = method.requirements[required_param_name]
                for i in self.problem.objects:
                    i = self.problem.objects[i]
                    match = self.__check_object_satisfies_parameter(model, i, requirements)
                    if match:
                        if required_param_name not in param_dict.keys():
                            param_dict[required_param_name] = [i]
                        else:
                            param_dict[required_param_name].append(i)
        if param_dict == {}:
            return False
        # Convert param_dict into a form which can be used - [[?a, ?b, ?c], [?a, ?b, ?d], ... ]
        return self.__convert_parameter_options_execution_ready(param_dict)

    def __check_object_satisfies_parameter(self, model, object, requirements: dict):
        """
        :param model:
        :param object:
        :param requirements: {'type': Type, 'predicates': {'and': {'on_board': 1, 'supports': 1}}
        :return: True - If object satisfies the requirements
        :return: False - Otherwise
        """
        required_type = requirements['type']
        required_predicates = requirements['predicates']

        # Check type
        if required_type is not None and required_type.name != object.type.name:
            return False

        # If there is no requirements on predicates then the object satisfies
        if required_predicates is None or len(required_predicates) == 0:
            return True

        # Check if each predicate is satisfied
        for pred in required_predicates:
            if pred == "and" or pred == "not" or pred == "or":
                required_param = required_predicates[pred]
                result = []
                for x in required_param.keys():
                    r = self.__check_object_satisfies_parameter(model, object,
                                                                {'type': None, 'predicates': {x: required_param[x]}})
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
                indexes = model.current_state.get_indexes(pred)
                if indexes is None:
                    return False
                for index in indexes:
                    try:
                        if object == model.current_state.elements[index].objects[required_predicates[pred] - 1]:
                            return True
                    except IndexError:
                        continue
                return False

    def __convert_parameter_options_execution_ready(self, param_dict):
        """The aim of this method is to return a list with all possible combinations of values from param_dict.
        This method is called from self.__find_satisfying_parameters()
        :parameter param_dict: {'?objective': Object, '?mode': Object, '?camera': [Object], '?rover': [Object],
        '?waypoint': [Object, Object, Object, Object]}
        :return: list of dictionaries containing all possible combinations
        """
        combinations = []

        def __create_combinations(remaining_params, selected_params={}):
            if remaining_params == {}:
                combinations.append(selected_params)
                return
            k = list(remaining_params.keys())[0]
            popped = remaining_params.pop(k)
            for po in popped:
                __create_combinations(remaining_params, Model.merge_dictionaries(selected_params, {k: po}))

        # Check input format
        for p in param_dict:
            q = param_dict[p]
            if type(q) == Object:
                param_dict[p] = [q]
            elif type(q) == list:
                for i in q:
                    assert type(i) == Object
            else:
                raise TypeError("Unknown type {}".format(type(q)))
        # Create combinations
        __create_combinations(param_dict)
        return combinations

    def __generate_param_dict(self, modifier, params):
        assert type(modifier) == Method or type(modifier) == Action or type(modifier) == Task
        # Check number of params is the amount expected
        if len(params) != len(modifier.parameters):
            return False
        # Map params to self.parameters
        i = 0
        param_dict = {}
        while i < len(modifier.parameters):
            param_name = modifier.parameters[i]
            if type(param_name) == Parameter:
                param_name = param_name.name
            param_dict[param_name] = params[i]
            i += 1
        return param_dict

    def output(self, resulting_model: Model):
        assert type(resulting_model) == Model

        print("\nActions Taken:")
        print([a.name for a in resulting_model.actions_taken])

        print("Final State:")
        print(resulting_model.current_state)
