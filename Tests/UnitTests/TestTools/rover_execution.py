from Solver.solver import Solver
from Solver.model import Model
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Internal_Representation.state import State
from Parsers.HDDL_Parser import HDDLParser


def setup():
    domain = Domain(None)
    problem = Problem(domain)
    domain.add_problem(problem)

    parser = HDDLParser(domain, problem)
    parser.parse_domain("../Examples/IPC_Tests/Rover/rover-domain.hddl")
    parser.parse_problem("../Examples/IPC_Tests/Rover/pfile01.hddl")

    # Initialise solver
    solver = Solver(domain, problem)
    return domain, problem, solver


def execution_prep(problem, solver):
    solver.solve(search=False)
