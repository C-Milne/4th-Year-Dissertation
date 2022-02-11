from Solver.model import Model


class Solver:
    def __init__(self, parser):
        self.parser = parser
        self.initial_model = Model(self.parser)

    def solve(self):
        task_counter = 0
        for subT in self.parser.subtasks_to_execute:
            if subT == "and" or subT == "or":
                continue
            

            print("SubTask:", task_counter, "-", subT[0], "(" + str(subT[1:]) + ")")
            self.__execute_task(self.initial_model, subT)
            task_counter += 1

    def __execute_task(self, model, task):
        """TODO - make this use new task class"""
        """Execute a task on a given model
        :params - model: model which the changes need to happen on
                - task: task to be carried out"""
        # Find methods in which the given task is present
        for method in self.parser.tasks[task[0]].methods:
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
