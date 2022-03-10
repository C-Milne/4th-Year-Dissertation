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
    task_counter = 0
    subtasks = problem.subtasks.get_tasks()
    list_subT = []
    num_tasks = len(subtasks)
    while task_counter < num_tasks:
        subT = subtasks[task_counter]
        if subT == "and" or subT == "or":
            del subtasks[task_counter]
            num_tasks -= 1
            continue

        # Create initial search model
        param_dict = solver._Solver__generate_param_dict(subT.task, subT.parameters)
        subT.add_given_parameters(param_dict)
        list_subT.append(subT)
        task_counter += 1

    initial_model = Model(State.reproduce(problem.initial_state), list_subT, problem)
    solver.search_models.add(initial_model)
