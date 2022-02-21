from Solver.model import Model
from Solver.search_queue import SearchQueue


class Solver:
    def __init__(self, domain, problem, model=None):
        self.domain = domain
        self.problem = problem

        self.search_models = SearchQueue()

        self._available_modifiers = []
        self._unexpanded_tasks = []

    def solve(self):
        task_counter = 0
        for subT in self.problem.subtasks_to_execute:
            if subT == "and" or subT == "or":
                continue

            print("SubTask:", task_counter, "-", subT[0], "(" + str(subT[1:]) + ")")
            # Set up search environment
            if len(subT) == 1:
                self._unexpanded_tasks = subT
            else:
                self._unexpanded_tasks = subT[1]

            self.__search()
            task_counter += 1

    def __search(self):
        # Expand unexpanded_tasks
        if len(self._unexpanded_tasks) > 0:
            # Expand one at a time
            for new_task in self._unexpanded_tasks:
                expansion = self.domain.get_task_methods(new_task)
                for new_modifier in expansion:
                    if new_modifier not in self._available_modifiers:
                        self._available_modifiers.append(new_modifier)
            self._unexpanded_tasks = []

        while True:
            # Search in some direction
                # Choose model in self.search_models and give it a search direction
            if len(self.search_models) == 0:
                self.search_models.add(Model(self.problem, self, self._available_modifiers))
            Node_to_search = self.search_models.pop()
            print(self)

    def __execute_task(self, model, task):
        """TODO - make this use new task class"""
        """Execute a task on a given model
        :params - model: model which the changes need to happen on
                - task: task to be carried out"""
        # Find methods in which the given task is present
        for method in self.domain.tasks[task[0]].methods:
            # Check if preconditions hold
            param_dict = self.__generate_param_dict(method, task[1:])

            if not method.evaluate_preconditions(model, param_dict):
                continue
            self.__execute_method(model, method, param_dict)

    def __execute_method(self, model, method, param_dict):
        """TODO - Dont use this - Either do the execution here or create a new class"""
        """At this point the method preconditions have already been checked"""
        method.execute(model, param_dict)

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

    def output(self):
        print("\nActions Taken:")
        print(self.initial_model.actions_taken)

        print("Final State:")
        print(self.initial_model.current_state)
