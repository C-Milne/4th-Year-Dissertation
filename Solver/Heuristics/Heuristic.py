"""The 'low_target' value MUST be set by any instance of this class.
If 'low_target' is True then models with a low ranking will be prioritised over those with a high score.
If 'low_target' is False then models with a high ranking will be given priority over those with a low score"""


class Heuristic:
    def __init__(self, domain, problem, solver, search_models):
        self.domain = domain
        self.problem = problem
        self.solver = solver
        self.search_models = search_models
        self.low_target = None

    def ranking(self, model) -> float:
        raise NotImplementedError