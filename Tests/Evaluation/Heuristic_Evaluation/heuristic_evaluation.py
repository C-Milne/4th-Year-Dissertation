import os
import sys
import time
import pickle
import re

working_dir = os.getcwd()
os.chdir("../../..")
sys.path.append(os.getcwd())
from Solver.Heuristics.breadth_first_by_operations_with_pruning import BreadthFirstOperationsPruning
from Solver.Heuristics.breadth_first_by_operations import BreadthFirstOperations
from runner import Runner
os.chdir(working_dir)

"""Methods for Operation"""


class Strat:
    def __init__(self, name, class_reference):
        self.name = name
        self.class_reference = class_reference
        self.file = None


def create_file(strat):
    # Check which files are already made
    # Do not overwrite any existing files
    file_name = strat.name + ".csv"
    counter = 0
    while os.path.exists(file_name):
        counter += 1
        file_name = strat.name + str(counter) + ".csv"

    # Create file
    strat.file = open(file_name, "w")
    strat.file.write("example_name,time_taken,serialised_actions_taken,serialised_state")


def save_to_file(test_name, strat, time, result):
    print("Writing: {}".format(time))
    # Pickle actions taken and state. Save them in the /serialised_objects folder
    pickle_test_name = test_name.replace("/", "_") + "_" + strat.name
    actions_taken_pickle_file = save_pickle_object(result.actions_taken, pickle_test_name + "_" + "actions")
    state_pickle_file = save_pickle_object(result.current_state, pickle_test_name + "_" + "state")
    strat.file.write("\n" + test_name + "," + str(time) + "," + actions_taken_pickle_file + "," +
                     state_pickle_file)


def save_pickle_object(object, file_name) -> str:
    file_name = file_name.replace(".", "")
    # Find a suitable file name
    f_name = "serialised_objects\\" + file_name + ".pickle"
    counter = 0
    while os.path.exists(f_name):
        counter += 1
        f_name = "serialised_objects\\" + file_name + str(counter) + ".pickle"

    # Save pickle file
    file = open(f_name, "wb")
    file.write(pickle.dumps(object))
    file.close()

    # Return file name
    return f_name


def test_runner(test, heuristic):
    controller = Runner(test[0], test[1])
    controller.parse_domain()
    controller.parse_problem()
    controller.set_heuristic(heuristic.class_reference)

    start_time = time.time()
    res = controller.solve()
    end_time = time.time()

    timeTaken = end_time - start_time

    result = [_.start() for _ in re.finditer("/", test[1])]
    test_name = test[1][result[-2] + 1:]
    save_to_file(test_name, heuristic, timeTaken, res)


def run_tests(tests, strats):
    # Create log csv for each strategy being assessed
    for s in strats:
        create_file(s)
    for t in tests:
        for s in strats:
            test_runner(t, s)
    for s in strats:
        s.file.close()


"""Test Rover p01 -> p03 with breadth first search with and without pruning"""
tests = [("../../Examples/Rover/domain.hddl", "../../Examples/Rover/p01.hddl"),
("../../Examples/Rover/domain.hddl", "../../Examples/Rover/p02.hddl"),
("../../Examples/Rover/domain.hddl", "../../Examples/Rover/p03.hddl")]

strats = [Strat("Breadth_First_Operations", BreadthFirstOperations),
Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning)]

run_tests(tests, strats)

"""Test Rover p04 with breadth first search and pruning"""
# tests = [("../../Examples/Rover/domain.hddl", "../../Examples/Rover/p04.hddl")]
# strats = [Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning)]
# run_tests(tests, strats)