import subprocess
import unittest
import os
from Tests.UnitTests.TestTools.env_setup import env_setup
from Tests.Evaluation.output_plan_reader import read_plan, display_plan
from runner import Runner
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Parsers.HDDL_Parser import HDDLParser
from Solver.Heuristics.distance_to_goal import PredicateDistanceToGoal
from Solver.Heuristics.tree_distance import TreeDistance
from Solver.Parameter_Selection.All_Parameters import AllParameters
from Solver.Parameter_Selection.Requirement_Selection import RequirementSelection


class RunnerTests(unittest.TestCase):
    original_dir = os.getcwd()

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"
        self.test_tools_path = "TestTools/"
        self.blocksworld_path = "../Examples/Blocksworld/"
        self.rover_path = "../Examples/IPC_Tests/Rover/"
        self.rover_col_path = "../Examples/Rover/"
        self.IPC_Tests_path = "../Examples/IPC_Tests/"
        os.chdir(self.original_dir)

    def test_load_unknown_domain(self):
        # Test loading unknown domain file
        with self.assertRaises(FileNotFoundError) as error:
            cont = Runner("../Examples/WrongBasic/basic.hddl", self.basic_pb1_path)
            cont.parse_domain()
        self.assertEqual("Domain file entered could not be found. ({})".format("../Examples/WrongBasic/basic.hddl"),
                         str(error.exception))

    def test_load_unknown_problem(self):
        # Test loading unknown problem file
        with self.assertRaises(FileNotFoundError) as error:
            cont = Runner(self.basic_domain_path, "../Examples/WrongBasic/pb1.hddl")
            cont.parse_domain()
            cont.parse_problem()
        self.assertEqual("Problem file entered could not be found. ({})".format("../Examples/WrongBasic/pb1.hddl"),
                         str(error.exception))

    def test_load_known_file(self):
        # Test loading basic domain and basic pb1
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.basic_domain_path)
        parser.parse_problem(self.basic_pb1_path)

    def test_load_one_file(self):
        # Test only passing in one file path
        with self.assertRaises(Exception) as error:
            Runner(self.basic_domain_path)
        self.assertTrue("__init__() missing 1 required positional argument: 'problem_path'" == str(error.exception) or
                        "Runner.__init__() missing 1 required positional argument: 'problem_path'" == str(error.exception))

    @unittest.skip
    def test_load_incompatible_files(self):
        # Test loading incompatible files
        with self.assertRaises(TypeError) as error:
            Runner(self.basic_domain_path, self.basic_pb1_path_SHOP)
        self.assertEqual("Problem file type (shop) does not match domain file type (hddl)", str(error.exception))

    def test_load_unknown_file_type(self):
        # Test loading a txt file
        with self.assertRaises(TypeError) as error:
            cont = Runner("TestTools/fakeDomain.txt", self.basic_pb1_path)
            cont.parse_domain()
        self.assertEqual("Unknown descriptor type (txt)", str(error.exception))

        # # Load file with no suffix
        # with self.assertRaises(IOError) as error:
        #     Runner("TestTools/fakeDomain2", self.basic_pb1_path)
        # self.assertEqual("File type not identified. (TestTools/fakeDomain2)", str(error.exception))

    def test_file_writing_command_line_args(self):
        os.chdir("../..")
        res = os.popen("python ./runner.py Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl -w runner_test_basic_p1")
        output = res.read()
        self.assertEqual("""Subtask: 0 - swap[\'banjo\', \'kiwi\']

Actions Taken:
drop - kiwi
pickup - banjo

Operations Taken:
swap - banjo kiwi
have_second - banjo kiwi
drop - kiwi
pickup - banjo

Search Models Created During Search: 3
""", output)
        self.assertTrue(os.path.exists("output/runner_test_basic_p1"))

    def test_file_writing_and_reading(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.basic_domain_path)
        parser.parse_problem(self.basic_pb1_path)
        res = solver.solve()
        Runner.output_result_file(res, "runner_test_basic_p1")
        plan = read_plan("../../output/runner_test_basic_p1")

        self.assertEqual(res.model_number, plan.model_number)
        self.assertEqual(res.current_state, plan.current_state)

    def test_runner_command_line_incorrect_args(self):
        original_dir = os.getcwd()
        os.chdir("../..")
        error_raised = False
        try:
            res = subprocess.check_output("python ./runner.py Tests/Examples/Basic/basic.hddl -w runner_test_basic_p1",
                                          stderr=subprocess.PIPE)
            output, error = res.communicate()
        except Exception as e:
            msg = e.stderr.decode("utf-8")
            # msg = msg[434:]   # This is for debugger inspection only
            self.assertEqual("""usage: runner.py [-h] [-w W] [-heuModName HEUMODNAME] [-heuPath HEUPATH]\r
                 [-paramSelectName PARAMSELECTNAME]\r
                 [-paramSelectPath PARAMSELECTPATH]\r
                 [D] [P]\r
runner.py: error: Incorrect Usage. Correct usage 'python runner.py <domain.suffix> <problem.suffix>'\r
""", msg)
            error_raised = True
        self.assertTrue(error_raised, "An Error Was not Raised When Running the Command")
        os.chdir(original_dir)

    def test_runner_command_line_help(self):
        os.chdir("../..")
        res = os.popen("python ./runner.py -h")
        output = res.read()
        self.assertEqual("""usage: runner.py [-h] [-w W] [-heuModName HEUMODNAME] [-heuPath HEUPATH]
                 [-paramSelectName PARAMSELECTNAME]
                 [-paramSelectPath PARAMSELECTPATH]
                 [D] [P]

positional arguments:
  D                     File path to Domain File
  P                     File path to Problem File

optional arguments:
  -h, --help            show this help message and exit
  -w W                  File path to Write Resulting Plan File
  -heuModName HEUMODNAME
                        Name of Heuristic Class
  -heuPath HEUPATH      File path to Heuristic File
  -paramSelectName PARAMSELECTNAME
                        Name of Parameter Selector Class
  -paramSelectPath PARAMSELECTPATH
                        File path to Parameter Selector File
""", output)

    def test_runner_command_line_heupath_or_heuname_only(self):
        # Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl -heuModName PredicateDistanceToGoal -heuPath Solver/Heuristics/distance_to_goal.py
        os.chdir("../..")

        error_raised = False
        try:
            res = subprocess.check_output("python ./runner.py Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl -heuModName PredicateDistanceToGoal",
                                          stderr=subprocess.PIPE)
            output, error = res.communicate()
        except Exception as e:
            msg = e.stderr.decode("utf-8")
            self.assertEqual("""usage: runner.py [-h] [-w W] [-heuModName HEUMODNAME] [-heuPath HEUPATH]\r
                 [-paramSelectName PARAMSELECTNAME]\r
                 [-paramSelectPath PARAMSELECTPATH]\r
                 [D] [P]\r
runner.py: error: Incorrect Usage. Either both '-heuModName' and '-heuPath' need to be set of both need to be empty\r
""", msg)
            error_raised = True
        self.assertTrue(error_raised, "An Error Was not Raised When Running the Command")

        error_raised = False
        try:
            res = subprocess.check_output("python ./runner.py Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl -heuPath Solver/Heuristics/distance_to_goal.py",
                                          stderr=subprocess.PIPE)
            output, error = res.communicate()
        except Exception as e:
            msg = e.stderr.decode("utf-8")
            self.assertEqual("""usage: runner.py [-h] [-w W] [-heuModName HEUMODNAME] [-heuPath HEUPATH]\r
                 [-paramSelectName PARAMSELECTNAME]\r
                 [-paramSelectPath PARAMSELECTPATH]\r
                 [D] [P]\r
runner.py: error: Incorrect Usage. Either both '-heuModName' and '-heuPath' need to be set of both need to be empty\r
""", msg)
            error_raised = True
        self.assertTrue(error_raised, "An Error Was not Raised When Running the Command")

    def test_runner_setting_heuristic_from_path(self):
        controller = Runner(self.basic_domain_path, self.basic_pb1_path)
        controller.parse_domain()
        controller.parse_problem()
        controller.set_heuristic_from_file('PredicateDistanceToGoal', '../../Solver/Heuristics/distance_to_goal.py')
        self.assertEqual(PredicateDistanceToGoal.__name__, type(controller.solver.search_models.heuristic).__name__)

        controller.set_heuristic_from_file('TreeDistance', '../../Solver/Heuristics/tree_distance.py')
        self.assertEqual(TreeDistance.__name__, type(controller.solver.search_models.heuristic).__name__)

    def test_runner_setting_heuristic_from_command_line(self):
        original_dir = os.getcwd()
        os.chdir("../..")
        error_raised = False
        try:
            res = subprocess.check_output("python ./runner.py Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl -heuModName PredicateDistanceToGoal"
                                          "  -heuPath Solver/Heuristics/distance_to_goal.py",
                                          stderr=subprocess.PIPE)
        except Exception as e:
            msg = e.stderr.decode("utf-8")  # This is for debugger inspection only
            print(msg)
            error_raised = True
        self.assertFalse(error_raised, "An Error Was Raised When Running the Command")
        os.chdir(original_dir)

    def test_runner_setting_parameter_selector_from_path(self):
        controller = Runner(self.basic_domain_path, self.basic_pb1_path)
        controller.parse_domain()
        controller.parse_problem()
        controller.set_parameter_selector_from_file('AllParameters', '../../Solver/Parameter_Selection/All_Parameters.py')
        self.assertEqual(AllParameters.__name__, type(controller.solver.parameter_selector).__name__)

        controller.set_parameter_selector_from_file('RequirementSelection', '../../Solver/Parameter_Selection/Requirement_Selection.py')
        self.assertEqual(RequirementSelection.__name__, type(controller.solver.parameter_selector).__name__)

    def test_runner_setting_parameter_selector_from_command_line(self):
        original_dir = os.getcwd()
        os.chdir("../..")
        error_raised = False
        try:
            res = subprocess.check_output("python ./runner.py Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl -paramSelectName RequirementSelection"
                                          " -paramSelectPath Solver/Parameter_Selection/Requirement_Selection.py",
                                          stderr=subprocess.PIPE)
        except Exception as e:
            msg = e.stderr.decode("utf-8")  # This is for debugger inspection only
            print(msg)
            error_raised = True
        self.assertFalse(error_raised, "An Error Was Raised When Running the Command")
        os.chdir(original_dir)

    def test_runner_command_line_heupath_or_heuname_only(self):
        # Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl -heuModName PredicateDistanceToGoal -heuPath Solver/Heuristics/distance_to_goal.py
        os.chdir("../..")

        error_raised = False
        try:
            res = subprocess.check_output(
                "python ./runner.py Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl -paramSelectName PredicateDistanceToGoal",
                stderr=subprocess.PIPE)
            output, error = res.communicate()
        except Exception as e:
            msg = e.stderr.decode("utf-8")
            self.assertEqual("""usage: runner.py [-h] [-w W] [-heuModName HEUMODNAME] [-heuPath HEUPATH]\r
                 [-paramSelectName PARAMSELECTNAME]\r
                 [-paramSelectPath PARAMSELECTPATH]\r
                 [D] [P]\r
runner.py: error: Incorrect Usage. Either both '-paramSelectName' and '-paramSelectPath' need to be set of both need to be empty\r
""", msg)
            error_raised = True
        self.assertTrue(error_raised, "An Error Was not Raised When Running the Command")

        error_raised = False
        try:
            res = subprocess.check_output(
                "python ./runner.py Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl -paramSelectPath Solver/Heuristics/distance_to_goal.py",
                stderr=subprocess.PIPE)
            output, error = res.communicate()
        except Exception as e:
            msg = e.stderr.decode("utf-8")
            self.assertEqual("""usage: runner.py [-h] [-w W] [-heuModName HEUMODNAME] [-heuPath HEUPATH]\r
                 [-paramSelectName PARAMSELECTNAME]\r
                 [-paramSelectPath PARAMSELECTPATH]\r
                 [D] [P]\r
runner.py: error: Incorrect Usage. Either both '-paramSelectName' and '-paramSelectPath' need to be set of both need to be empty\r
""", msg)
            error_raised = True
        self.assertTrue(error_raised, "An Error Was not Raised When Running the Command")
