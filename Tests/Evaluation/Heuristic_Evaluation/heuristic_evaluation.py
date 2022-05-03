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
from Solver.Heuristics.breadth_first_by_operations_with_partial_order_pruning import BreadthFirstOperationsPartialOrderPruning
from Solver.Heuristics.hamming_distance_partial_order import HammingDistancePartialOrder
from Solver.Heuristics.tree_distance_partial_order import TreeDistancePartialOrder
from runner import Runner
from Solver.Solving_Algorithms.partial_order import PartialOrderSolver
from Solver.Solving_Algorithms.total_order import TotalOrderSolver
from Solver.model import Model
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

    if result is not None:
        actions_taken_pickle_file = save_pickle_object(result.actions_taken, pickle_test_name + "_" + "actions")
        state_pickle_file = save_pickle_object(result.current_state, pickle_test_name + "_" + "state")
        num_models = result.num_models_used
    else:
        actions_taken_pickle_file, state_pickle_file = "NONE", "NONE"
        num_models = 0

    strat.file.write("\n" + test_name + "," + str(time) + "," + str(num_models) + "," + actions_taken_pickle_file + "," +
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


def test_runner(test, heuristic, early_precon=True, partial_order=False, search=True):
    controller = Runner(test[0], test[1])

    result = [_.start() for _ in re.finditer("/", test[1])]
    test_name = test[1][result[-2] + 1:]

    if search:
        controller.parse_domain()
        controller.parse_problem()
    else:
        # If we are not timing the search we are timing the parsing
        start_time = time.time()
        controller.parse_domain()
        controller.parse_problem()
        end_time = time.time()
        timeTaken = end_time - start_time
        save_to_file(test_name, heuristic, timeTaken, None)
        return

    if partial_order:
        controller.set_solver(PartialOrderSolver)
    else:
        controller.set_solver(TotalOrderSolver)

    controller.set_heuristic(heuristic.class_reference)
    controller.solver.task_expansion_given_param_check = early_precon
    Model.model_counter = 0   # This needs to be reset for each test

    start_time = time.time()
    res = controller.solve()
    end_time = time.time()

    timeTaken = end_time - start_time

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

    if 'search' in kwargs.keys():
        run_search = kwargs['search']
        assert type(run_search) == bool
    else:
        run_search = True

    # Create log csv for each strategy being assessed
    for s in strats:
        create_file(s)
    for t in tests:
        for s in strats:
            for i in range(5):
                if 'partial_order' in kwargs:
                    partial_order = kwargs['partial_order']
                else:
                    partial_order = False
                test_runner(t, s, early_precon, partial_order, run_search)
    for s in strats:
        s.file.close()
    os.chdir("../..")

"""##################################################################################################################"""
"""Test Rover p01 -> p03 with breadth first search without pruning (No early precon checking) -> DONE"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl")]
#
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations, False)]
#
# run_tests(tests, strats, "Rover_no_early_precon", True, early_precon=False)

"""Test Rover p01 -> p04 with breadth first search and pruning (No early precon checking) -> DONE"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p04.hddl")]
#
# strats = [Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning, False)]
# run_tests(tests, strats, "Rover_no_early_precon", False, early_precon=False)

"""##################################################################################################################"""
"""Test Rover p01 -> p04 with breadth first search without pruning - DONE"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl")]
#
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations)]
#
# run_tests(tests, strats, "Test", True)

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
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p04.hddl")]
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
"""Test translog1 -> DONE"""
# tests = [("../../../../Examples/IPC_Tests/um-translog01/domain.hddl", "../../../../Examples//IPC_Tests/um-translog01/problem.hddl")]
#
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations),
# Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning),
#           Strat("Hamming_Distance", HammingDistance), Strat("Tree_Distance", TreeDistance)]
# run_tests(tests, strats, "translog", True)

"""Test translog1 with delete relaxed -> DONE"""
# tests = [("../../../../Examples/IPC_Tests/um-translog01/domain.hddl", "../../../../Examples//IPC_Tests/um-translog01/problem.hddl")]
#
# strats = [Strat("Delete_Relaxed", DeleteRelaxed)]
# run_tests(tests, strats, "translog", False)

"""Test rover with all parameter selection and requirement parameter selection"""

"""###################################################################################################################"""
"""Test depot p1 -> p3 with breadth first operations (WITHOUT PRUNING) - DONE"""
# tests = [("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p01.hddl"),
# ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p02.hddl")
# ,("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p03.hddl")]
#
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations)]
#
# run_tests(tests, strats, "Depot", True)
#
"""Test depot p1 -> p3 with breadth first operations - DONE"""
# tests = [("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p01.hddl"),
# ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p02.hddl"),
# ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p03.hddl")]
#
# strats = [Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning)]
#
# run_tests(tests, strats, "Depot")

"""Test depot p1 -> p3 with Delete Relaxed"""
# tests = [("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p01.hddl")]
# # ("../../../../Examples/Depots/domain.hddl", "../../../../Examples/Depots/p02.hddl")]
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
"""Test Barman with breadth first (NO PRUNING) - DONE"""
# tests = [("../../../../Examples/Barman/domain.hddl", "../../../../Examples/Barman/pfile01.hddl")]
#
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations)]
#
# run_tests(tests, strats, "Barman", True)
#
"""Test Barman with breadth first - DONE"""
# tests = [("../../../../Examples/Barman/domain.hddl", "../../../../Examples/Barman/pfile01.hddl")]
#
# strats = [Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning)]
#
# run_tests(tests, strats, "Barman")

"""Test Barman with Delete Relaxed - DONE"""
# tests = [("../../../../Examples/Barman/domain.hddl", "../../../../Examples/Barman/pfile01.hddl")]
#
# strats = [Strat("Delete_Relaxed", DeleteRelaxed)]
#
# run_tests(tests, strats, "Barman")

"""Test Barman with Tree Distance - DONE"""
# tests = [("../../../../Examples/Barman/domain.hddl", "../../../../Examples/Barman/pfile01.hddl")]
#
# strats = [Strat("Tree_Distance", TreeDistance)]
#
# run_tests(tests, strats, "Barman")

"""Test Barman with Hamming Distance - DONE"""
# tests = [("../../../../Examples/Barman/domain.hddl", "../../../../Examples/Barman/pfile01.hddl")]
#
# strats = [Strat("Hamming_Distance", HammingDistance)]
#
# run_tests(tests, strats, "Barman")

"""###################################################################################################################"""
"""Test Factories with Breadth First (NO PRUNING) - DONE"""
# tests = [("../../../../Examples/Factories/domain.hddl", "../../../../Examples/Factories/pfile01.hddl")]
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations)]
# run_tests(tests, strats, "Factories", True)

"""Test factories with Breadth First - DONE"""
# tests = [("../../../../Examples/Factories/domain.hddl", "../../../../Examples/Factories/pfile01.hddl")]
# strats = [Strat("Breadth_First_Operations_Pruning", BreadthFirstOperationsPruning)]
# run_tests(tests, strats, "Factories")

"""Test Factories with Delete Relaxed"""
# tests = [("../../../../Examples/Factories/domain.hddl", "../../../../Examples/Factories/pfile01.hddl")]
# strats = [Strat("Delete_Relaxed", DeleteRelaxed)]
# run_tests(tests, strats, "Factories")

"""Test Factories with Tree Distance - DONE"""
# tests = [("../../../../Examples/Factories/domain.hddl", "../../../../Examples/Factories/pfile01.hddl")]
#
# strats = [Strat("Tree_Distance", TreeDistance)]
#
# run_tests(tests, strats, "Factories")

"""Test Factories with Hamming Distance - DONE"""
# tests = [("../../../../Examples/Factories/domain.hddl", "../../../../Examples/Factories/pfile01.hddl")]
#
# strats = [Strat("Hamming_Distance", HammingDistance)]
#
# run_tests(tests, strats, "Factories")

"""###################################################################################################################"""
"""PARTIAL ORDER TESTS"""
"""Test PO-Rover Breadth First (NO PRUNING) - DONE"""
# tests = [("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile01.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile02.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile03.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile04.hddl")]
#
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations)]
# run_tests(tests, strats, "Rover_Partial_Order", True, partial_order=True)

"""Test PO-Rover Breadth First - DONE"""
# tests = [("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile01.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile02.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile03.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile04.hddl")]
#
# strats = [Strat("Breadth_First_Operations_PO_Pruning", BreadthFirstOperationsPartialOrderPruning)]
# run_tests(tests, strats, "Rover_Partial_Order", partial_order=True)

"""Test Hamming Distance (Partial Order) - DONE"""
# tests = [("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile01.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile02.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile03.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile04.hddl")]
#
# strats = [Strat("Hamming_Distance_Partial_Order", HammingDistancePartialOrder)]
# run_tests(tests, strats, "Rover_Partial_Order", partial_order=True)

"""Test Tree Distance (Partial Order)"""
# tests = [("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile01.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile02.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile03.hddl"),
# ("../../../../Examples/Partial_Order/Rover/domain.hddl", "../../../../Examples/Partial_Order/Rover/pfile04.hddl")]
#
# strats = [Strat("Tree_Distance_Partial_Order", TreeDistancePartialOrder)]
# run_tests(tests, strats, "Rover_Partial_Order", partial_order=True)

"""###################################################################################################################"""
"""Test Barman Partial Order - Breadth First (No Pruning) -> DONE"""
# tests = [("../../../../Examples/Partial_Order/Barman/domain.hddl", "../../../../Examples/Partial_Order/Barman/pfile01.hddl")
# # ,("../../../../Examples/Partial_Order/Barman/domain.hddl", "../../../../Examples/Partial_Order/Barman/pfile02.hddl")
# ]
# strats = [Strat("Breadth_First_Operations", BreadthFirstOperations)]
# run_tests(tests, strats, "Barman_Partial_Order", True, partial_order=True)

"""Test Barman Partial Order - Breadth First-> DONE"""
# tests = [("../../../../Examples/Partial_Order/Barman/domain.hddl", "../../../../Examples/Partial_Order/Barman/pfile01.hddl")
# # ,("../../../../Examples/Partial_Order/Barman/domain.hddl", "../../../../Examples/Partial_Order/Barman/pfile02.hddl")
# ]
# strats = [Strat("Breadth_First_Operations_PO_Pruning", BreadthFirstOperationsPartialOrderPruning)]
# run_tests(tests, strats, "Barman_Partial_Order", partial_order=True)

"""Test Barman Partial Order - Hamming Distance -> DONE"""
# tests = [("../../../../Examples/Partial_Order/Barman/domain.hddl", "../../../../Examples/Partial_Order/Barman/pfile01.hddl")
# # ,("../../../../Examples/Partial_Order/Barman/domain.hddl", "../../../../Examples/Partial_Order/Barman/pfile02.hddl")
# ]
# strats = [Strat("Hamming_Distance_Partial_Order", HammingDistancePartialOrder)]
# run_tests(tests, strats, "Barman_Partial_Order", partial_order=True)

"""Test Barman Partial Order - Tree Distance -> DONE"""
# tests = [("../../../../Examples/Partial_Order/Barman/domain.hddl", "../../../../Examples/Partial_Order/Barman/pfile01.hddl")
# # ,("../../../../Examples/Partial_Order/Barman/domain.hddl", "../../../../Examples/Partial_Order/Barman/pfile02.hddl")
# ]
# strats = [Strat("Tree_Distance_Partial_Order", TreeDistancePartialOrder)]
# run_tests(tests, strats, "Barman_Partial_Order", partial_order=True)

"""###################################################################################################################"""
"""Test Barman partial order - Breadth First (No Pruning)"""

"""Test Barman partial order - Breadth First"""

"""Test Barman partial order - Hamming Distance"""

"""Test Barman partial order - Tree Distance"""


"""###################################################################################################################"""
"""TEST TOTAL ORDERED PROBLEM WITH PARTIAL ORDER SOLVER AND TOTAL ORDER SOLVER (ROVER 1 -> 4)"""
"""Partial Order -> Done"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p04.hddl")]
#
# strats = [Strat("Breadth_First_Operations_Pruning_PO", BreadthFirstOperationsPruning)]
#
# run_tests(tests, strats, "Rover_PO_TO", True, partial_order=True)

"""Total Order -> Done"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl"),
# ("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p04.hddl")]
#
# strats = [Strat("Breadth_First_Operations_Pruning_TO", BreadthFirstOperationsPruning)]
#
# run_tests(tests, strats, "Rover_PO_TO")

"""###################################################################################################################"""
"""Test JSHOP - Compare Execution times to parsing times"""
"""Test Basic HDDL vs JSHOP"""
"""Parsing Time"""
"""HDDL"""
# tests = [("../../../../Examples/Basic/basic.hddl", "../../../../Examples/Basic/pb1.hddl")]
#
# strats = [Strat("HDDL_Parsing", BreadthFirstOperations)]
#
# run_tests(tests, strats, "Basic", True, search=False)

"""JSHOP"""
# tests = [("../../../../Examples/JShop/basic/basic.jshop", "../../../../Examples/JShop/basic/problem.jshop")]
#
# strats = [Strat("JSHOP_Parsing", BreadthFirstOperations)]
#
# run_tests(tests, strats, "Basic", False, search=False)

"""Solve Time"""
"""HDDL"""
# tests = [("../../../../Examples/Basic/basic.hddl", "../../../../Examples/Basic/pb1.hddl")]
#
# strats = [Strat("Breadth_First_HDDL", BreadthFirstOperations)]
#
# run_tests(tests, strats, "Basic", False)

"""JSHOP"""
# tests = [("../../../../Examples/JShop/basic/basic.jshop", "../../../../Examples/JShop/basic/problem.jshop")]
#
# strats = [Strat("Breadth_First_JSHOP", BreadthFirstOperations)]
#
# run_tests(tests, strats, "Basic", False)

"""Test Rover HDDL vs JSHOP"""
"""Parsing Time"""
"""HDDL"""
# tests = [("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p01.hddl")
#          ,("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p02.hddl")
#          ,("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p03.hddl")
#          ,("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p04.hddl")
#          ,("../../../../Examples/Rover/domain.hddl", "../../../../Examples/Rover/p05.hddl")
#          ]
#
# strats = [Strat("Breadth_First_HDDL", BreadthFirstOperations)]
#
# run_tests(tests, strats, "HDDL_JSHOP_Rover", True, search=False)

"""JSHOP"""
# tests = [("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb1.jshop")
#          ,("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb2.jshop")
#          ,("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb3.jshop")
#          ,("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb4.jshop")
#          ,("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb5.jshop")
#          ]
#
# strats = [Strat("Breadth_First_JSHOP", BreadthFirstOperations)]
#
# run_tests(tests, strats, "HDDL_JSHOP_Rover", False, search=False)

"""Total Time"""
"""JSHOP"""
"""Breadth First (No Pruning)"""
tests = [("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb1.jshop")
         ]

strats = [Strat("Breadth_First", BreadthFirstOperations)]

run_tests(tests, strats, "JSHOP_Rover", True)

"""Breadth First"""
tests = [("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb1.jshop")
         ,("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb2.jshop")
         ,("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb3.jshop")
         ,("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb4.jshop")
         ]

strats = [Strat("Breadth_First_Pruning", BreadthFirstOperationsPruning)]

run_tests(tests, strats, "JSHOP_Rover")

"""Tree Distance"""
tests = [("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb1.jshop")
         ,("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb2.jshop")
         ,("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb3.jshop")
         ,("../../../../Examples/JShop/rover/rover.jshop", "../../../../Examples/JShop/rover/pb4.jshop")
         ]

strats = [Strat("Tree_Distance", TreeDistance)]

run_tests(tests, strats, "JSHOP_Rover")
