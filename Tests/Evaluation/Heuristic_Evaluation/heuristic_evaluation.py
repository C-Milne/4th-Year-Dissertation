import os
import shutil
import sys
import time
import pickle
import re

working_dir = os.getcwd()
os.chdir("../../..")
sys.path.append(os.getcwd())
from Solver.Heuristics.breadth_first_by_operations_with_pruning import BreadthFirstOperationsPruning
from Solver.Heuristics.breadth_first_by_operations import BreadthFirstOperations
from Solver.Heuristics.hamming_distance import HammingDistance
from Solver.Heuristics.delete_relaxed import DeleteRelaxed
from Solver.Heuristics.tree_distance import TreeDistance
from runner import Runner
from Solver.Solving_Algorithms.partial_order import PartialOrderSolver
from Solver.Solving_Algorithms.total_order import TotalOrderSolver
os.chdir(working_dir)

"""Methods for Operation"""


class Strat:
    def __init__(self, name, class_reference, early_task_precon_checker=True):
        self.name = name
        self.class_reference = class_reference
        self.file = None
        self.early_task_precon_checker = early_task_precon_checker


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
    strat.file.write("example_name,time_taken,search_models_created,serialised_actions_taken,serialised_state")


def save_to_file(test_name, strat, time, result):
    print("Writing: {}".format(time))
    # Pickle actions taken and state. Save them in the /serialised_objects folder
    pickle_test_name = test_name.replace("/", "_") + "_" + strat.name
    actions_taken_pickle_file = save_pickle_object(result.actions_taken, pickle_test_name + "_" + "actions")
    state_pickle_file = save_pickle_object(result.current_state, pickle_test_name + "_" + "state")
    strat.file.write("\n" + test_name + "," + str(time) + "," + str(result.num_models_used) + "," + actions_taken_pickle_file + "," +
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


def test_runner(test, heuristic, early_precon=True, partial_order=False):
    controller = Runner(test[0], test[1])
    controller.parse_domain()
    controller.parse_problem()
    if partial_order:
        controller.set_solver(PartialOrderSolver)
    else:
        controller.set_solver(TotalOrderSolver)
    controller.set_heuristic(heuristic.class_reference)
    controller.set_early_task_precon_checker(heuristic.early_task_precon_checker)
    controller.solver.task_expansion_given_param_check = early_precon

    start_time = time.time()
    res = controller.solve()
    end_time = time.time()

    timeTaken = end_time - start_time

    result = [_.start() for _ in re.finditer("/", test[1])]
    test_name = test[1][result[-2] + 1:]
    save_to_file(test_name, heuristic, timeTaken, res)


def run_tests(tests, strats, sub_folder, clear_folder=False, **kwargs):
    os.chdir("Archive")
    # Clear subfolder
    if clear_folder:
        if os.path.isdir(sub_folder):
            shutil.rmtree(sub_folder)
    if not os.path.isdir(sub_folder):
        os.mkdir(sub_folder)
        os.mkdir(sub_folder + "/serialised_objects")
    os.chdir(sub_folder)

    if "early_precon" in kwargs.keys():
        early_precon = kwargs["early_precon"]
        assert type(early_precon) == bool
    else:
        early_precon = True

    # Create log csv for each strategy being assessed
    for s in strats:
        create_file(s)
    for t in tests:
        for s in strats:
            for i in range(5):
                test_runner(t, s, early_precon)
    for s in strats:
        s.file.close()
    os.chdir("../..")


"""Test Rover p01 -> p03 with breadth first search without pruning - DONE"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl")]
#
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations)]
#
# run_tests(tests, strats, "Rover", True)

"""Test Rover p01 -> p04 with breadth first search and pruning - DONE"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl")
# ,("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p04.hddl")]
# strats = [Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning)]
# run_tests(tests, strats, "Rover", False)

"""Test rover p01 -> p03 with Tree Distance - DONE"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl")]
#
# strats = [Strat("Tree_Distance", TreeDistance)]
#
# run_tests(tests, strats, "Rover")

"""Test rover p01 -> p03 with Delete Relaxed - DONE"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl")]
# # ,("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl")]
# # ,("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl")]
#
# strats = [Strat("Delete_Relaxed", DeleteRelaxed)]
#
# run_tests(tests, strats, "Rover")

"""Test Rover p01 -> p03 with breadth first search without pruning (No early precon checking) -> DONE"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl")]
#
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations, False)]
#
# run_tests(tests, strats, "Rover_no_early_precon", early_precon=False)

"""Test Rover p01 -> p04 with breadth first search and pruning (No early precon checking) -> DONE"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p04.hddl")]
#
# strats = [Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning, False)]
# run_tests(tests, strats, "Rover_no_early_precon", False, early_precon=False)

"""Test rover with Hamming Distance heuristic -> DONE"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p04.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p05.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p06.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p07.hddl")]
#
# strats = [Strat("Hamming_Distance", HammingDistance)]
#
# run_tests(tests, strats, "Rover")

"""###################################################################################################################"""
"""Test translog1 with breadth first search with and without pruning -> DONE"""
# tests = [("../../../../Examples/IPC_Tests/um-translog01/domain.hddl", "../../../../Examples//IPC_Tests/um-translog01/problem.hddl")]
#
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations),
# Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning),
#           Strat("Hamming_Distance", HammingDistance)]
# run_tests(tests, strats, "translog", True)

"""Test rover with all parameter selection and requirement parameter selection"""

"""###################################################################################################################"""
"""Test depot p1 -> p3 with breadth first operations (WITHOUT PRUNING) - DONE"""
# tests = [("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p01.hddl"),
# ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p02.hddl")]
# # ,("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p03.hddl")]
#
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations)]
#
# run_tests(tests, strats, "Depot", True)

"""Test depot p1 -> p3 with breadth first operations - DONE"""
# tests = [("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p01.hddl"),
# ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p02.hddl"),
# ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p03.hddl")]
#
# strats = [Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning)]
#
# run_tests(tests, strats, "Depot")

"""Test depot p1 -> p3 with Delete Relaxed"""
# tests = [("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p01.hddl"),
# ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p02.hddl")]
# # ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p03.hddl")]
#
# strats = [Strat("Delete_Relaxed", DeleteRelaxed)]
#
# run_tests(tests, strats, "Depot")

"""Test depot p1 -> p3 with Hamming Distance - DONE"""
# tests = [("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p01.hddl"),
# ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p02.hddl"),
# ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p03.hddl")]
#
# strats = [Strat("Hamming_Distance", HammingDistance)]
#
# run_tests(tests, strats, "Depot")

"""Test depot p1 -> p3 with Tree Distance- DONE"""
# tests = [("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p01.hddl"),
# ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p02.hddl"),
# ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p03.hddl")]
#
# strats = [Strat("Tree_Distance", TreeDistance)]
#
# run_tests(tests, strats, "Depot")

"""###################################################################################################################"""
"""Test Barman with breadth first"""
tests = [("../../../../Examples/Barman/domain.hddl", "../../../../Examples/Barman/pfile01.hddl")]

strats = [Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning)]

run_tests(tests, strats, "Barman")
