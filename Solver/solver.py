from Solver.model import Model


class Solver:
    def __init__(self, parser):
        self.parser = parser
        self.initial_model = Model(self.parser)

    def solve(self):
        """TODO - implement this"""
        if self.parser.is_goal_empty():
            self.__solve_subtasks()

    def __solve_subtasks(self):
        task_counter = 0
        for subT in self.parser.subtasks_to_execute:
            print("SubTask:", task_counter, "-", subT[0], "(" + str(subT[1:]) + ")")
            self.__execute_task(self.initial_model, subT)
            task_counter += 1

    def __execute_task(self, model, task):
        """Execute a task on a given model
        :params - model: model which the changes need to happen on
                - task: task to be carried out"""
        # Find methods in which the given task is present
        for method in self.parser.methods:
            if method.task[0] == task[0]:
                # Check if preconditions hold
                param_dict = self.__generate_param_dict(method, task[1:])

                if not method.evaluate_preconditions(model, param_dict):
                    continue
                self.__execute_method(model, method, param_dict)

    def __execute_method(self, model, method, param_dict):
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
        """TODO - implement"""
        print("Actions Taken:")
        print(self.initial_model.actions_taken)

        print("Final State:")
        print(self.initial_model.current_state)
