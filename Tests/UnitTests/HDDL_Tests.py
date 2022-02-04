import unittest
import os
from runner import Runner

SHOW_ERROR_MESSAGES = True


class HDDLTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"
        self.test_tools_path = "TestTools/"

    def test_load_uknown_domain(self):
        # Test loading unknown domain file
        with self.assertRaises(FileNotFoundError) as error:
            Runner("../Examples/WrongBasic/basic.hddl", self.basic_pb1_path)
        self.assertEqual("Domain file entered could not be found. ({})".format("../Examples/WrongBasic/basic.hddl"),
                         str(error.exception))

    def test_load_unknown_problem(self):
        # Test loading unknown problem file
        with self.assertRaises(FileNotFoundError) as error:
            Runner(self.basic_domain_path, "../Examples/WrongBasic/pb1.hddl")
        self.assertEqual("Problem file entered could not be found. ({})".format("../Examples/WrongBasic/pb1.hddl"),
                         str(error.exception))

    def test_load_unknown_domain_problem(self):
        # Test loading unknown domain and problem files
        with self.assertRaises(FileNotFoundError) as error:
            Runner("../Examples/WrongBasic/basic.hddl", "../Examples/WrongBasic/pb1.hddl")
        self.assertEqual("Domain file entered could not be found. ({})".format("../Examples/WrongBasic/basic.hddl"),
                         str(error.exception))

    def test_load_known_file(self):
        # Test loading basic domain and basic pb1
        Runner(self.basic_domain_path, self.basic_pb1_path)

    def test_load_one_file(self):
        # Test only passing in one file path
        with self.assertRaises(Exception) as error:
            Runner(self.basic_domain_path)
        print(str(error.exception))
        self.assertEqual("__init__() missing 1 required positional argument: 'problem_path'", str(error.exception))

    def test_load_incompatible_files(self):
        # Test loading incompatible files
        with self.assertRaises(TypeError) as error:
            Runner(self.basic_domain_path, self.basic_pb1_path_SHOP)
        self.assertEqual("Problem file type (shop) does not match domain file type (hddl)", str(error.exception))

    def test_load_unknown_file_type(self):
        # Test loading a txt file
        with self.assertRaises(TypeError) as error:
            Runner("TestTools/fakeDomain.txt", self.basic_pb1_path)
        self.assertEqual("Unknown descriptor type (txt)", str(error.exception))

        # Load file with no suffix
        with self.assertRaises(IOError) as error:
            Runner("TestTools/fakeDomain2", self.basic_pb1_path)
        self.assertEqual("File type not identified. (TestTools/fakeDomain2)", str(error.exception))

    def test_basic_pb1(self):
        # Test running basic pb1 - Check final state and actions taken
        runner = Runner(self.basic_domain_path, self.basic_pb1_path)

        # Check number of tasks
        self.assertEqual(1, len(runner.parser.tasks))
        # Check number of predicates
        self.assertEqual(1, len(runner.parser.predicates.keys()))
        # Check number of actions
        self.assertEqual(2, len(runner.parser.actions))
        # Check number of methods
        self.assertEqual(2, len(runner.parser.methods))
        # Check state of model after planning
        self.assertEqual({'have': ['banjo']}, runner.solver.initial_model.current_state)
        # Check number of steps taken in plan
        self.assertEqual(2, len(runner.solver.initial_model.actions_taken))

    def test_method_same_name(self):
        # Test setting actions / methods with same name
        with self.assertRaises(Exception) as error:
            Runner(self.test_tools_path + "basic_domain_test_1.hddl", self.basic_pb1_path)
        self.assertEqual("Test", str(error.exception))

    def test_modify_method_task(self):
        # Test setting method task after it has already been set
        with self.assertRaises(KeyError) as error:
            Runner(self.test_tools_path + "basic_domain_test_2.hddl", self.basic_pb1_path)
        self.assertEqual("Task has already been set for method 'have_first'. Please check your domain file.",
                         str(error.exception).replace("\"", ""))

        # Test again with task that is not defined at all
        with self.assertRaises(KeyError) as error:
            Runner(self.test_tools_path + "basic_domain_test_3.hddl", self.basic_pb1_path)
        self.assertEqual("Task 'swap' is not defined. Please check your domain file.",
                         str(error.exception).replace("\"", ""))

    def test_method_no_name(self):
        # Define method with no name
        with self.assertRaises(SyntaxError) as error:
            Runner(self.test_tools_path + "basic_domain_test_4.hddl", self.basic_pb1_path)
        self.assertEqual("Error with Method name. Must be a string not beginning with ':'."
                         "\nPlease check your domain file.",
                         str(error.exception).replace("\"", ""))

    # Test preconditions
        # And
        # Not
        # Or

    # Test any other error raising events

    # Test :htn :subtasks

    # Test putting wrong type into things

    # Test loading some big domains and count number of actions etc

    def tearDown(self) -> None:
        pass
