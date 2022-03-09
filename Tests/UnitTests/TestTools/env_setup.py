from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Parsers.HDDL_Parser import HDDLParser
from Solver.solver import Solver
from Internal_Representation.state import State
from Solver.model import Model


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


def solver_setup(solver, problem):
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
