import copy
import sys
from Solver.model import Model
from Solver.search_queue import SearchQueue
from Internal_Representation.method import Method
from Internal_Representation.action import Action
from Internal_Representation.task import Task


class Solver:
    def __init__(self, domain, problem, model=None):
        self.domain = domain
        self.problem = problem

        self.search_models = SearchQueue()

        self._available_modifiers = []
        self._unexpanded_tasks = []

    def solve(self):
        task_counter = 0
        for subT in self.problem.subtasks_to_execute.get_tasks():
            if subT == "and" or subT == "or":
                continue

            print("SubTask:", task_counter, "-", subT.get_name(), "(" + str(subT.parameters) + ")")
            # expand subT
            self._unexpanded_tasks = [subT.task, subT.parameters]

            search_result = self.__search()
            if search_result is None:
                print("No plan Found")
                sys.exit()
            task_counter += 1

    def __search(self):
        # Expand unexpanded_tasks
        if len(self._unexpanded_tasks) > 0:
            # Expand one at a time
            for new_task in self._unexpanded_tasks:
                already_set_parameters = None
                if len(new_task) > 1:
                    already_set_parameters = new_task[1:]
                    new_task = new_task[0]
                expansion = self.domain.get_task_methods(new_task)
                for new_modifier in expansion:
                    if new_modifier not in self._available_modifiers:
                        self._available_modifiers.append([new_modifier, already_set_parameters])

            self._unexpanded_tasks = []

        while True:
            # Search in some direction
                # Choose model in self.search_models and give it a search direction
            if len(self.search_models) == 0:
                self.search_models.add(Model(self.problem, self, self._available_modifiers))
            Node_to_search = self.search_models.pop()

            if Node_to_search is not None:
                self.__search_node(Node_to_search)
            else:
                return None

    def __search_node(self, node):
        if len(node.ready_modifiers) == 0:
            return None

        mod = list(node.ready_modifiers.keys())[0]
        for params in node.ready_modifiers[mod]:
            modifier = self.domain.get_modifier(mod)
            self.__node_expansion(copy.deepcopy(node), modifier, params)

    def __node_expansion(self, node, modifier, param_dict):
        # Apply modifier to node
        if modifier is not None:
            self.__execute(node, modifier, param_dict)
            # Check if node is now in goal state
            if self.problem.evaluate_goal(node):
                print("FOUND GOAL")
        else:
            return

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
                # Add subtasks to search node available modifiers
                # Add subtasks to search node ready modifiers
                model.add_ready_modifier(subT, [param_dict], index)
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
                newModel = copy.deepcopy(model)
                newModel.pop_ready_modifier()
                newModel.add_ready_modifier(methods[i], [param_dict], 0)
                self.search_models.add(newModel)
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

    def __generate_param_dict(self, method, params):
        # Check number of params is the amount expected
        if len(params) != len(method.parameters):
            return False
        # Map params to self.parameters
        i = 0
        param_dict = {}
        while i < len(method.parameters):
            param_dict[method.parameters[i]] = params[i]
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
