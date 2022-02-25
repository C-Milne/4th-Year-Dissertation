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
        self.rover_path = "../Examples/IPC_Tests/Rover/"

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

    def test_parsing_types(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Rover/domain1.hddl")
        self.assertEqual(8, len(domain.types))

        keys = list(domain.types.keys())
        self.assertIn('object', keys)
        self.assertIn('waypoint', keys)
        self.assertIn('mode', keys)
        self.assertIn('store', keys)
        self.assertIn('rover', keys)
        self.assertIn('camera', keys)
        self.assertIn('lander', keys)
        self.assertIn('objective', keys)

        self.assertEqual(None, domain.types['object'].parent)
        for k in keys[1:]:
            self.assertEqual(domain.types['object'], domain.types[k].parent)

    def test_parsing_predicates(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Rover/domain1.hddl")
        self.assertEqual(26, len(domain.predicates))

        self.assertEqual('at', domain.predicates['at'].name)
        self.assertEqual('?arg0', domain.predicates['at'].parameters[0].name)
        self.assertEqual('rover', domain.predicates['at'].parameters[0].type.name)

        self.assertEqual('can_traverse', domain.predicates['can_traverse'].name)
        self.assertEqual('?arg2', domain.predicates['can_traverse'].parameters[2].name)
        self.assertEqual('waypoint', domain.predicates['can_traverse'].parameters[2].type.name)

        self.assertEqual('visible_from', domain.predicates['visible_from'].name)
        self.assertEqual('?arg1', domain.predicates['at'].parameters[1].name)
        self.assertEqual('waypoint', domain.predicates['at'].parameters[1].type.name)

    def test_parsing_action(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Rover/domain2.hddl")

        # Check action values
        self.assertEqual(1, len(domain.actions))
        self.assertIn('take_image', domain.actions.keys())

        self.assertEqual('take_image', domain.actions['take_image'].name)
        self.assertEqual(2, len(domain.actions['take_image'].effects.effects))
        self.assertEqual(True, domain.actions['take_image'].effects.effects[0].negated)
        self.assertEqual(['?i', '?r'], domain.actions['take_image'].effects.effects[0].parameters)
        self.assertEqual('calibrated', domain.actions['take_image'].effects.effects[0].predicate)
        self.assertEqual(False, domain.actions['take_image'].effects.effects[1].negated)
        self.assertEqual(['?r', '?o', '?m'], domain.actions['take_image'].effects.effects[1].parameters)
        self.assertEqual('have_image', domain.actions['take_image'].effects.effects[1].predicate)

        self.assertEqual(5, len(domain.actions['take_image'].parameters))
        self.assertEqual('?r', domain.actions['take_image'].parameters[0].name)
        self.assertEqual('rover', domain.actions['take_image'].parameters[0].type.name)
        self.assertEqual('?p', domain.actions['take_image'].parameters[1].name)
        self.assertEqual('waypoint', domain.actions['take_image'].parameters[1].type.name)
        self.assertEqual('?o', domain.actions['take_image'].parameters[2].name)
        self.assertEqual('objective', domain.actions['take_image'].parameters[2].type.name)
        self.assertEqual('?i', domain.actions['take_image'].parameters[3].name)
        self.assertEqual('camera', domain.actions['take_image'].parameters[3].type.name)
        self.assertEqual('?m', domain.actions['take_image'].parameters[4].name)
        self.assertEqual('mode', domain.actions['take_image'].parameters[4].type.name)

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

    def test_parameter_parsing(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "rover_domain_test.hddl")
        parser.parse_problem(self.rover_path + "pfile01.hddl")

        # Get take-image action
        action = domain.get_action("take_image")
        self.assertEqual(5, len(action.parameters))
        self.assertEqual("?r", action.parameters[0].name)
        self.assertEqual("rover", action.parameters[0].param_type.name)
        self.assertEqual("?p", action.parameters[1].name)
        self.assertEqual("waypoint", action.parameters[1].param_type.name)
        self.assertEqual("?o", action.parameters[2].name)
        self.assertEqual("objective", action.parameters[2].param_type.name)
        self.assertEqual("?i", action.parameters[3].name)
        self.assertEqual("camera", action.parameters[3].param_type.name)
        self.assertEqual("?m", action.parameters[4].name)
        self.assertEqual("mode", action.parameters[4].param_type.name)

    def test_parsing_tasks(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Rover/domain3.hddl")

        self.assertEqual(9, len(domain.tasks))
        keys = list(domain.tasks.keys())
        self.assertIn('calibrate_abs', keys)
        self.assertIn('empty_store', keys)
        self.assertIn('get_image_data', keys)
        self.assertIn('get_rock_data', keys)
        self.assertIn('get_soil_data', keys)
        self.assertIn('navigate_abs', keys)
        self.assertIn('send_image_data', keys)
        self.assertIn('send_rock_data', keys)
        self.assertIn('send_soil_data', keys)

        self.assertEqual(2, len(domain.tasks['calibrate_abs'].parameters))
        self.assertEqual('?rover', domain.tasks['calibrate_abs'].parameters[0].name)
        self.assertEqual('rover', domain.tasks['calibrate_abs'].parameters[0].type.name)
        self.assertEqual(3, len(domain.tasks['send_image_data'].parameters))
        self.assertEqual('?mode', domain.tasks['send_image_data'].parameters[2].name)
        self.assertEqual('mode', domain.tasks['send_image_data'].parameters[2].type.name)

    def test_parsing_method(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.rover_path + "rover-domain.hddl")

        # m_empty_store_1_ordering_0 - no subtasks
        self.assertEqual(13, len(domain.methods))
        self.assertEqual("m_empty_store_1_ordering_0", domain.methods["m_empty_store_1_ordering_0"].name)
        self.assertEqual(None, domain.methods["m_empty_store_1_ordering_0"].subtasks)
        self.assertEqual(domain.get_task("empty_store"), domain.methods["m_empty_store_1_ordering_0"].task['task'])
        self.assertEqual("?s", domain.methods["m_empty_store_1_ordering_0"].task['params'][0].name)
        self.assertEqual("?rover", domain.methods["m_empty_store_1_ordering_0"].task['params'][1].name)

        self.assertEqual("m_navigate_abs_4_ordering_0", domain.methods["m_navigate_abs_4_ordering_0"].name)
        self.assertEqual(4, len(domain.methods["m_navigate_abs_4_ordering_0"].subtasks))
        self.assertEqual(domain.get_task("navigate_abs"), domain.methods["m_navigate_abs_4_ordering_0"].task['task'])
        self.assertEqual("?rover", domain.methods["m_navigate_abs_4_ordering_0"].task['params'][0].name)
        self.assertEqual("?to", domain.methods["m_navigate_abs_4_ordering_0"].task['params'][1].name)

        # Test ordering as well
        self.assertEqual('navigate', domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[0].task)
        self.assertEqual("?rover", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[0].parameters[0].name)
        self.assertEqual("?from", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[0].parameters[1].name)
        self.assertEqual("?mid", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[0].parameters[2].name)

        self.assertEqual('visit', domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[1].task)
        self.assertEqual("?mid", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[1].parameters[0].name)

        self.assertEqual('navigate', domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[2].task)
        self.assertEqual("?rover", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[2].parameters[0].name)
        self.assertEqual("?mid", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[2].parameters[1].name)
        self.assertEqual("?mid", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[2].parameters[1].name)

        self.assertEqual('unvisit', domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[3].task)
        self.assertEqual("?mid", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[3].parameters[0].name)
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
