import copy
import sys
from Solver.model import Model
from Solver.search_queue import SearchQueue
from Internal_Representation.method import Method
from Internal_Representation.action import Action
from Internal_Representation.task import Task
from Internal_Representation.parameter import Parameter


class Solver:
    def __init__(self, domain, problem, model=None):
        self.domain = domain
        self.problem = problem

        self.search_models = SearchQueue()

    def solve(self):
        task_counter = 0
        for subT in self.problem.subtasks_to_execute.get_tasks():
            if subT == "and" or subT == "or":
                continue

            print("SubTask:", task_counter, "-", subT.get_name(), "(" + str(subT.parameters) + ")")

            # expand subT
            self.search_models.clear()

            # If subT has the name of an object as a parameter, get the object
            new_params = []
            for p in subT.parameters:
                if type(p) == str:
                    new_params.append(self.problem.get_object(p))
                else:
                    new_params.append(p)

            self.search_models.add(Model(self.problem, self, subT.task, self.__generate_param_dict(subT.task, new_params)))

            search_result = self.__search()
            if search_result is None:
                print("No plan Found")
                sys.exit()
            task_counter += 1

    def __search(self):
        while True:
            # Search in some direction
            # Choose model in self.search_models and give it a search direction
            Node_to_search = self.search_models.pop()

            if Node_to_search is not None:
                if len(Node_to_search.ready_modifiers) == 0:
                    return None

                mod = list(Node_to_search.ready_modifiers.keys())[0]
                params_list = Node_to_search.ready_modifiers[mod]
                if type(params_list) == list:
                    for params in params_list:
                        modifier = Node_to_search.ready_modifiers_refs[mod]
                        self.__node_expansion(copy.deepcopy(Node_to_search), modifier, params)
                elif type(params_list) == dict:
                    modifier = Node_to_search.ready_modifiers_refs[mod]
                    self.__node_expansion(copy.deepcopy(Node_to_search), modifier, params_list)
            else:
                return None

    def __node_expansion(self, node, modifier, param_dict):
        # Apply modifier to node
        if modifier is not None:
            self.__execute(node, modifier, param_dict)
            # Check if node is now in goal state
            if self.problem.evaluate_goal(node):
                print("FOUND GOAL")
        else:
            return

    def __find_satisfying_params(self, model, modifier, set_params:dict={}):
        """TODO - What about methods with no parameters"""
        # Can the model satisfy these parameters in current state?
        if type(set_params) == list:
            set_params = set_params[0]
        assert type(set_params) == dict

        param_dict = set_params

        if type(modifier) == Task:
            if len(param_dict) == len(modifier.parameters):
                keys = list(param_dict.keys())
                for i in range(len(keys)):
                    if not self.__check_object_satisfies_parameter(model, param_dict[keys[i]], modifier.parameters[i]):
                        return False
                return param_dict
            else:
                raise NotImplementedError("This is not implemented")
        else:
            for required_param_name in modifier.requirements:
                if required_param_name.startswith('forall-'):
                    result = modifier.evaluate_preconditions(model, {})
                elif required_param_name in param_dict:
                    continue
                else:
                    required_param = modifier.requirements[required_param_name]
                    # Get objects that satisfy type
                    for i in model.current_state.objects:
                        i = model.current_state.objects[i]
                        if self.__check_object_satisfies_parameter(model, i, required_param):
                            if required_param_name not in param_dict.keys():
                                param_dict[required_param_name] = [i]
                            else:
                                param_dict[required_param_name].append(i)

            if param_dict == {}:
                return False
            return param_dict

    def __check_object_satisfies_parameter(self, model, ob, required_param):
        if type(required_param) == Parameter:
            required_param_type = required_param.param_type
            required_param_predicates = None
        else:
            required_param_type = required_param["type"]
            required_param_predicates = required_param['predicates']

        if required_param_type is not None and required_param_type.name != ob.type.name:
            return False

        if required_param_predicates is None:
            return True

        # Check if object satisfies predicates
        for pred in required_param_predicates:
            if pred == "and" or pred == "not" or pred == "or":
                required_param = required_param_predicates[pred]
                result = []
                for x in required_param.keys():
                    r = self.__check_object_satisfies_parameter(model, ob, {'type': None, 'predicates': {x: required_param[x]}})
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
                        if model.current_state.objects[model.current_state.elements[index][required_param['predicates'][pred]]] == ob:
                            return True
                    except IndexError:
                        continue
                return False

    def __execute_task(self, model, task):
        """TODO - make this use new task class ; Is this method still used?"""
        """Execute a task on a given model
        :params - model: model which the changes need to happen on
                - task: task to be carried out"""
        # Find methods in which the given task is present
        for method in self.domain.tasks[task[0]].methods:
            # Check if preconditions hold
            param_dict = self.__generate_param_dict(method, task[1:])

            if not method.evaluate_preconditions(model, param_dict):
                continue
            self.__execute(model, method, param_dict)

    def __execute(self, model, modifier, param_dict):
        """TODO - Implement, 'or'; What if all ordered subtasks do NOT go through?"""
        """Execute this method on the given model
                    :param  - model : to have actions carried out on
                            - task : is the task to be carried out on the model
                                    : Is None is all tasks are to be carried out
                    :warning - This is a recursive function"""
        """At this point the method preconditions have already been checked"""
        if type(modifier) == Method:
            if modifier.ordered_subtasks is not None:
                task = modifier.ordered_subtasks
            else:
                raise NotImplementedError("Support for partial ordered subtasks is not ready yet")

            # Do something
            if task[0] == "and":
                task = task[1:]
            elif task[0] == "or":
                raise NotImplementedError("This is not implemented")

            index = 0
            model.pop_ready_modifier()
            for subT in task[1:]:
                # Add subtasks to search node ready modifiers
                modifier = self.domain.get_modifier(subT[0])
                pass_param_dict = {}

                for p in subT[1:]:
                    if p in param_dict.keys():
                        pass_param_dict[p] = param_dict[p]

                # Check all the parameters are present
                if len(pass_param_dict) != len(modifier.parameters):
                    print("here")
                model.add_ready_modifier(modifier, pass_param_dict, index)
                index += 1

            # Add model to search queue
            self.search_models.add(model)

        elif type(modifier) == Action:
            self.__execute_action(model, modifier, param_dict)
        elif type(modifier) == Task:
            # Create a new search model with each possible method / action in the space of the task in ready_modifiers
            methods = self.domain.get_task_methods(modifier)
            i = 0
            while i < len(methods):
                # Get options for parameters
                param_options = self.__find_satisfying_params(model, methods[i], param_dict)

                self.__generate_new_search_models(model, methods[i], param_options)
                i += 1
        else:
            raise RuntimeError("Something went wrong")

    def __execute_action(self, model, action, params):
        """TODO - Implement ; what if there is multiple effects?"""
        """Execute the changes of this action on the model"""
        i = 0
        effect_conjunction = False
        while i < len(action.effect):
            if action.effect[i] == "and":
                i += 1
                effect_conjunction = True
                continue
            elif action.effect[i] == "or":
                raise NotImplementedError("Support for OR subtasks has not been developed")

            if action.effect[i][0] == "not":
                identifier = action.effect[i][1][0]
                required_params = action.effect[i][1][1:]
                params_in_use = []
                for p in required_params:
                    params_in_use.append(params[p].name)
                self.__execute_action_remove(identifier, params_in_use, model)
            else:
                # Collection
                if effect_conjunction:
                    identifier = action.effect[i][0]
                    required_params = action.effect[i][1:]
                else:
                    identifier = action.effect[0]
                    required_params = action.effect[1:]
                    i = len(action.effect)  # Stop the iteration of the loop
                params_in_use = []
                for p in required_params:
                    params_in_use.append(params[p].name)
                self.__execute_action_add(identifier, params_in_use, model)
            i += 1
        model.add_action([action.name, params])

    def __execute_action_remove(self, predicate_identifier, predicate_definitions, model):
        if len(predicate_definitions) == 0:
            # Change predicate value
            model.current_state.remove_element(predicate_identifier)
        else:
            model.current_state.remove_element(predicate_identifier, predicate_definitions)

    def __execute_action_add(self, predicate_identifier, predicate_definitions, model):
        if len(predicate_definitions) == 0:
            model.current_state.add_element(predicate_identifier)
        else:
            model.current_state.add_element(predicate_identifier, predicate_definitions)

    def __generate_new_search_models(self, existing_model:Model, modifier, param_options:dict, set_params={}):
        assert type(existing_model) == Model
        assert type(modifier) == Method or type(modifier) == Action
        assert type(param_options) == dict

        keys = list(param_options.keys())
        set_params_keys = list(set_params.keys())
        for k in keys:
            if k in set_params_keys:
                continue
            elif type(param_options[k]) != list:
                set_params[k] = param_options[k]
            elif type(param_options[k]) == list and len(param_options[k]) == 1:
                set_params[k] = param_options[k][0]
            else:
                for option in param_options[k]:
                    pass_dict = param_options
                    pass_dict[k] = option
                    self.__generate_new_search_models(existing_model, modifier, pass_dict, set_params)

        if len(set_params) == len(param_options):
            newModel = copy.deepcopy(existing_model)
            newModel.pop_ready_modifier()
            newModel.add_ready_modifier(modifier, set_params, 0)
            self.search_models.add(newModel)

    def __generate_param_dict(self, method, params):
        # Check number of params is the amount expected
        if len(params) != len(method.parameters):
            return False
        # Map params to self.parameters
        i = 0
        param_dict = {}
        while i < len(method.parameters):
            param_name = method.parameters[i]
            if type(param_name) == Parameter:
                param_name = param_name.name
            param_dict[param_name] = params[i]
            i += 1
        return param_dict

    def check_type_problem(self, ob):
        if ob == self.problem:
            return True
        return False

    def output(self):
        print("\nActions Taken:")
        print(self.initial_model.actions_taken)

        print("Final State:")
        print(self.initial_model.current_state)
