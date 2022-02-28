import copy
import sys
from Solver.model import Model
from Solver.search_queue import SearchQueue
from Internal_Representation.method import Method
from Internal_Representation.action import Action
from Internal_Representation.task import Task
from Internal_Representation.parameter import Parameter
from Internal_Representation.subtasks import Subtasks


class Solver:
    def __init__(self, domain, problem, model=None):
        self.domain = domain
        self.problem = problem

        self.search_models = SearchQueue()

    def solve(self):
        task_counter = 0
        for subT in self.problem.subtasks.get_tasks():
            if subT == "and" or subT == "or":
                continue

            print("Subtask:", task_counter, "-", subT.get_name(), "(" + str(subT.parameters) + ")")

            # Prepare search_models
            self.search_models.clear()

            # Create initial search model
            param_dict = self.__generate_param_dict(subT.task, subT.parameters)
            initial_model = Model(self.problem.initial_state, [subT.task], param_dict)
            self.search_models.add(initial_model)

            search_result = self.__search()
            if search_result is None:
                print("No plan Found")
                sys.exit()
            task_counter += 1

    def __search(self):
        while True:
            # New model to operate on
            search_model = self.search_models.pop()

            # Check what needs to be done to this model
            next_modifier = search_model.get_next_modifier()
            if type(next_modifier) == Task:
                self.__expand_task(next_modifier, search_model)
            elif type(next_modifier) == Method:
                self.__expand_method(next_modifier, search_model)
            elif type(next_modifier) == Subtasks.Subtask and type(next_modifier.task) == Action:
                i = 0
                param_dict = {}
                while i < len(next_modifier.parameters):
                    param_dict[next_modifier.parameters[i].name] = None
                    i += 1
                self.__expand_action(next_modifier, search_model, param_dict)
            else:
                raise NotImplementedError

            # Loop exit conditions
            print("here")

    def __expand_task(self, task: Task, search_model: Model):
        # For each method, create a new search model
        for method in task.methods:
            # Check parameters for new_model
            # Is all the required parameters present or do some need to be chosen
            parameters = search_model.given_params
            if len(method.parameters) < len(search_model.given_params):
                raise NotImplementedError

            # Check preconditions of new_model
            result = method.preconditions.evaluate(search_model, parameters)

            if result:
                # Create new model and add to search_models
                new_model = Model(search_model.current_state, [method] + search_model.search_modifiers, parameters)
                self.search_models.add(new_model)

    def __expand_method(self, method: Method, search_model: Model):
        # Add actions to search model - with parameters
        i = 0
        for action in method.subtasks.tasks:
            assert type(action.task) == Action
            # Check parameter count
            assert len(search_model.given_params) >= len(action.parameters)
            # Add action to search_model
            search_model.insert_modifier(action, i)
            i += 1
        self.search_models.add(search_model)

    def __expand_action(self, action: Action, search_model: Model, param_dict):
        print("here")
        pass

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

    def output(self):
        print("\nActions Taken:")
        print(self.initial_model.actions_taken)

        print("Final State:")
        print(self.initial_model.current_state)
