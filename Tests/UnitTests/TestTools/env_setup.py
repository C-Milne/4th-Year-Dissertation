from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Parsers.HDDL_Parser import HDDLParser
from Parsers.JSHOP_Parser import JSHOPParser
from Parsers.parser import Parser
from Solver.Solving_Algorithms.solver import Solver
from Solver.Solving_Algorithms.partial_order import PartialOrderSolver


def env_setup(HDDL: bool) -> [Domain, Problem, Parser, PartialOrderSolver]:
    domain = Domain(None)
    problem = Problem(domain)
    domain.add_problem(problem)
    if HDDL:
        parser = HDDLParser(domain, problem)
    else:
        parser = JSHOPParser(domain, problem)
    solver = PartialOrderSolver(domain, problem)
    return domain, problem, parser, solver


def solver_setup(solver: Solver, problem: Problem) -> None:
    solver.solve(search=False)
