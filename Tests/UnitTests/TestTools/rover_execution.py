from Solver.solver import Solver
from Solver.model import Model
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Parsers.HDDL_Parser import HDDLParser


def setup():
    domain = Domain(None)
    problem = Problem(domain)
    domain.add_problem(problem)

    parser = HDDLParser(domain, problem)
    parser.parse_domain("../Examples/IPC_Tests/Rover/rover-domain.hddl")
    parser.parse_problem("../Examples/IPC_Tests/Rover/pfile01.hddl")
    task = problem.subtasks.get_tasks()[0]

    # Initialise solver
    solver = Solver(domain, problem)

    # Create initial model
    solver.search_models.clear()
    param_dict = solver._Solver__generate_param_dict(task.task, task.parameters)
    initial_model = Model(problem.initial_state, [task.task], param_dict, problem)
    solver.search_models.add(initial_model)
    return domain, problem, solver
