import os
import pickle
import re
from runner import Runner
"""This file is used to calculate the size of a parsed problem.
The results are stored in a common pickled dictionary."""
pickle_file_name = "problem_sizes.pickle"


def calculate_size(domain_file: str, problem_file: str) -> int:
    controller = Runner(domain_file, problem_file)
    controller.parse_domain()
    controller.parse_problem()

    domain_size = _calculate_domain_size(controller)
    problem_size = _calculate_problem_size(controller)

    size_dict = _open_pickled_dictionary()

    indexes = [_.start() for _ in re.finditer("/", problem_file)]
    problem_name = problem_file[indexes[-2] + 1:]

    size_dict[problem_name] = domain_size + problem_size
    _write_pickled_dictionary(size_dict)
    return domain_size + problem_size


def _calculate_domain_size(controller: Runner) -> int:
    domain_size = 0

    domain_size += len(controller.domain.predicates)
    domain_size += len(controller.domain.types)

    for t in controller.domain.tasks:
        t = controller.domain.tasks[t]
        domain_size += 1
        if t.parameters is not None:
            domain_size += len(t.parameters)

    for m in controller.domain.methods:
        m = controller.domain.methods[m]
        domain_size += 1
        if m.parameters is not None:
            domain_size += len(m.parameters)
        if m.subtasks is not None:
            domain_size += len(m.subtasks)
        if m.preconditions is not None:
            domain_size += len(m.preconditions)
        if m.constraints is not None:
            domain_size += len(m.constraints)

    for a in controller.domain.actions:
        a = controller.domain.actions[a]
        domain_size += 1
        if a.parameters is not None:
            domain_size += len(a.parameters)
        if a.preconditions is not None:
            domain_size += len(a.preconditions)
        if a.effects is not None:
            domain_size += len(a.effects)

    return domain_size


def _calculate_problem_size(controller: Runner) -> int:
    problem_size = 0

    problem_size += len(controller.problem.objects)
    if controller.problem.goal_conditions is not None:
        problem_size += len(controller.problem.goal_conditions)
    problem_size += (len(controller.problem.subtasks) * 10)
    problem_size += len(controller.problem.initial_state)
    return problem_size


def _open_pickled_dictionary() -> dict:
    """If pickle file does not exist, return an empty dict"""
    if os.path.exists(pickle_file_name):
        # Open and return the dictionary
        with open(pickle_file_name, 'rb') as handle:
            size_dict = pickle.load(handle)
        return size_dict
    return {}


def _write_pickled_dictionary(size_dict) -> None:
    with open(pickle_file_name, 'wb') as handle:
        pickle.dump(size_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def get_pickled_dictionary() -> dict:
    pass
