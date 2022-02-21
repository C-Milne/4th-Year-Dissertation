import unittest
from runner import Runner
from Internal_Representation.precondition import Precondition
from Solver.model import Model
from Parsers.HDDL_Parser import HDDLParser
from Internal_Representation.method import Method
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem


class HDDLTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"
        self.test_tools_path = "TestTools/"
        self.blocksworld_path = "../Examples/Blocksworld/"

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
        # Test setting methods with same name
        with self.assertRaises(Exception) as error:
            Runner(self.test_tools_path + "basic_domain_test_1.hddl", self.basic_pb1_path)
        self.assertEqual("Name 'swap_ob_1' is already assigned", str(error.exception))

    def test_modify_method_task(self):
        # Test setting method task after it has already been set
        with self.assertRaises(KeyError) as error:
            Runner(self.test_tools_path + "basic_domain_test_2.hddl", self.basic_pb1_path)
        self.assertEqual("Task has already been set for method 'have_first'. Please check your domain file.",
                         str(error.exception).replace("\"", ""))

    def test_set_unknown_task_method(self):
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

    def test_precondition_and(self):
        # Test the 'and' functionality for preconditions
        # Set up precondition object
        precon_list = ['and', ['have','?x'], ['have','?y'], ['have', '?z']]
        precons = Precondition(precon_list)
        # Set up model
        state_dict = {'have': ['ham', 'irn-bru', 'car']}
        model = Model(state_dict)
        param_dict = {"?z": "ham", "?x":"irn-bru", "?y": "car"}

        # Testing for True
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        # Testing for False
        state_dict = {'have': ['irn-bru', 'car']}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

    def test_precondition_or(self):
        # Test the 'or' functionality for preconditions
        # Set up precondition object
        precon_list = ['or', ['have', '?x'], ['have', '?y'], ['have', '?z']]
        precons = Precondition(precon_list)
        # Set up model
        state_dict = {'have': ['ham', 'irn-bru', 'car']}
        model = Model(state_dict)
        param_dict = {"?z": "ham", "?x": "irn-bru", "?y": "car"}

        # Testing for True
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        # Testing for True
        state_dict = {'have': ['irn-bru', 'car']}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        state_dict = {'have': ['irn-bru']}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        state_dict = {'have': []}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

    def test_precondition_not(self):
        # Test the 'not' functionality for preconditions
        # Set up precondition object
        precon_list = ['not', ['have', '?x']]
        precons = Precondition(precon_list)
        # Set up model
        state_dict = {'have': ['ham', 'irn-bru', 'car']}
        model = Model(state_dict)
        param_dict = {"?z": "ham", "?x": "irn-bru", "?y": "car"}

        # Testing for False
        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

        # Testing for True
        state_dict = {'have': ['ham', 'car']}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

    def test_precondition_parsing(self):
        # Testing parsing with blank predicates
        # Test and
        precon_list = ['and']
        precons = Precondition(precon_list)
        # Set up model
        state_dict = {'have': ['ham', 'irn-bru', 'car']}
        model = Model(state_dict)
        param_dict = {"?z": "ham", "?x": "irn-bru", "?y": "car"}

        with self.assertRaises(SyntaxError) as error:
            precons.evaluate(model, param_dict)
        self.assertEqual("Test", str(error.exception))

        # Test or
        precon_list = ['or']
        precons = Precondition(precon_list)

        with self.assertRaises(SyntaxError) as error:
            precons.evaluate(model, param_dict)
        self.assertEqual("Test", str(error.exception))

        # Test not
        precon_list = ['not']
        precons = Precondition(precon_list)

        with self.assertRaises(SyntaxError) as error:
            precons.evaluate(model, param_dict)
        self.assertEqual("Test", str(error.exception))

        # Test all 3 at once
        precon_list = ['and', ['or'], ['not'], ['and']]
        precons = Precondition(precon_list)

        with self.assertRaises(SyntaxError) as error:
            precons.evaluate(model, param_dict)
        self.assertEqual("Test", str(error.exception))

    def test_precondition_complex(self):
        # Devise a complex precondition and test it
        precon_list = ['and',
                       ['not',
                            ['and',['have','?y'],['have','?a']]
                        ],
                       ['and',
                            ['have', '?x'], ['or', ['have', '?b'], ['have', '?c']]
                        ],
                       ['or',
                            ['hate','?z'], ['hate', '?d']
                        ]
                       ]
        precons = Precondition(precon_list)
        # Set up model
        state_dict = {'have': ['ham', 'irn-bru', 'car'], 'hate': []}
        model = Model(state_dict)
        param_dict = {"?z": "ham", "?x": "irn-bru", "?y": "car", "?a": "bike", "?b": "popcorn", "?c": "crisps", "?d": "dark"}

        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

        state_dict = {'have': ['ham', 'irn-bru', 'car', 'popcorn'], 'hate': ['dark']}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

    def test_method_requirements(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld_test_domain_2.hddl")

        # Add some assertions for this - seems too work (perhaps not for 'forall' methods)
        self.assertEqual(1, 2)

    def test_forall_preconditons(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld_test_domain_1.hddl")
        parser.parse_problem(self.test_tools_path + "Blocksworld_test_problem_1.hddl")
        method = domain.methods['setdone']
        model = Model(problem, None, [])
        result = method.evaluate_preconditions(model, {})
        self.assertEqual(False, result)

        # Test for True
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld_test_domain_1.hddl")
        parser.parse_problem(self.test_tools_path + "Blocksworld_test_problem_1_1.hddl")
        method = domain.methods['setdone']
        model = Model(problem, None, [])
        result = method.evaluate_preconditions(model, {})
        self.assertEqual(True, result)

    def test_complex_method_requirements(self):
        # Test a huge method requirements with and, or, not, and forall
        self.assertEqual(1, 2)

    def test_model_requirement_satisfier(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld_test_domain_3.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        model = Model(problem, None, [domain.methods["unstack-block"]])
        self.assertEqual(1, len(model.ready_modifiers))
        self.assertEqual({'unstack-block':[{'?b': problem.objects['b3']}]}, model.ready_modifiers)

    # Test actions

    # Test actions with the same name

    # Test method with action name

    # Test parameters - 2 ?a's - lists instead of string. - Maybe make a parameter class??
        # Method parameters
        # Action parameters
        # Task parameters

    # Test any other error raising events

    # Test :htn :subtasks

    # Test tasks with multiple types - blocksworld pb1

    # Test putting wrong type into things

    # Test loading some big domains and count number of actions etc

    def tearDown(self) -> None:
        pass
