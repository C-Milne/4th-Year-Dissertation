from Solver.Heuristics.pruning import Pruning

"""This is an extension to the breadth first search.
Search can be initialised with multiple subtasks. After a model fully expands one subtask its current state is logged.
If another model completes the same subtask and has the same current state, it is pruned."""


class BreadthFirstOperationsPruning(Pruning):
    def __init__(self, domain, problem, solver, search_models):
        super().__init__(domain, problem, solver, search_models)
        self.low_target = True

    def ranking(self, model) -> float:
        return len(model.operations_taken)

    def presolving_processing(self) -> None:
        pass

    def task_milestone(self, model) -> bool:
        return True
