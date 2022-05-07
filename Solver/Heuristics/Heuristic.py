from abc import ABC, abstractmethod


class Heuristic(ABC):
    def __init__(self, domain, problem, solver, search_models):
        self.domain = domain
        self.problem = problem
        self.solver = solver
        self.search_models = search_models

    @abstractmethod
    def ranking(self, model) -> float:
        raise NotImplementedError

    @abstractmethod
    def presolving_processing(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def task_milestone(self, model) -> bool:
        raise NotImplementedError
