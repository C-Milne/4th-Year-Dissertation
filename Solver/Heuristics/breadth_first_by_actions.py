from Solver.Heuristics.Heuristic import Heuristic
"""This is a simple intuitive method of breadth first search.
Simply giving priority to search models which have executed the least actions.
This search strategy is very susceptible to infinite recursion making it unusable.
In which case 'breadth_first_by_operations' is a better option."""


class BreadthFirstActions(Heuristic):
    def __init__(self, domain, problem, solver, search_models):
        super().__init__(domain, problem, solver, search_models)
        self.low_target = True

    def ranking(self, model) -> float:
        return len(model.actions_taken)

    def presolving_processing(self) -> None:
        pass

    def task_milestone(self, model) -> bool:
        return True
