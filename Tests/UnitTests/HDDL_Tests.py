import unittest
import os
from runner import Runner

SHOW_ERROR_MESSAGES = True


class HDDLTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"

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

    # Test running basic pb1 - Check final state and actions taken ; Check what is stored in the parser
    # Test setting actions / methods with same name
    # Test setting actions / method names after they have already been set

    # Test precondtions
        # And
        # Not
        # Or

    # Test any other error raising events

    # Test :htn :subtasks

    # Test putting wrong type into things

    # Test loading some big domains and count number of actions etc

    def tearDown(self) -> None:
        pass
