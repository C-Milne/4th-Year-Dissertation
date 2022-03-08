from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Parsers.HDDL_Parser import HDDLParser
from Solver.solver import Solver


def env_setup(HDDL: bool):
    domain = Domain(None)
    problem = Problem(domain)
    domain.add_problem(problem)
    if HDDL:
        parser = HDDLParser(domain, problem)
    else:
        raise NotImplementedError
    solver = Solver(domain, problem)
    return domain, problem, parser, solver
