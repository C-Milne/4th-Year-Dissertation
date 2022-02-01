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

            task_counter += 1

    def __execute(self, model, task):
        """TODO : Consider preconditons"""
        """Execute a task on a given model
        :params - model: model which the changes need to happen on
                - task: task to be carried out"""

    def __output(self):
        """TODO - implement"""
        pass
