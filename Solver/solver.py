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
        """TODO - implement"""
        task_counter = 0
        for subT in self.parser.subtasks_to_execute:
            print("Task:", task_counter, "-", subT[0], "(" + str(subT[1:]) + ")")
            self.__execute_task(self.initial_model, subT)
            task_counter += 1

    def __execute_task(self, model, task):
        """TODO : Consider preconditons"""
        """Execute a task on a given model
        :params - model: model which the changes need to happen on
                - task: task to be carried out"""
        # Find methods in which the given task is present
        for method in self.parser.methods:
            if method.task[0] == task[0]:
                # Check if preconditions hold
                if not method.evaluate_preconditions(model, task[1:]):
                    continue
                self.__execute_method(model, method)

    def __execute_method(self, model, method):
        """TODO : Implement"""
        print("here")

    def __output(self):
        """TODO - implement"""
        pass
