from Solver.Solving_Algorithms.solver import Solver


class TotalOrderSolver(Solver):
    def __init__(self, domain, problem):
        super().__init__(domain, problem)
