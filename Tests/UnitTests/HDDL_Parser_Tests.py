import unittest
from runner import Runner
from Internal_Representation.precondition import Precondition
from Solver.model import Model
from Parsers.HDDL_Parser import HDDLParser
from Internal_Representation.method import Method
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Internal_Representation.parameter import Parameter
from Internal_Representation.Object import Object


class HDDLTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"
        self.test_tools_path = "TestTools/"
        self.blocksworld_path = "../Examples/Blocksworld/"
        self.rover_path = "../Examples/IPC_Tests/Rover/"

    def test_load_unknown_domain(self):
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
        print(str(error.exception))
        self.assertEqual("Runner.__init__() missing 1 required positional argument: 'problem_path'", str(error.exception))

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

    def test_set_unknown_task_method(self):
        # Test again with task that is not defined at all
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)
        parser = HDDLParser(domain, problem)

        with self.assertRaises(KeyError) as error:
            parser.parse_domain(self.test_tools_path + "basic/basic_domain_test_3.hddl")
        self.assertEqual("Task 'swap' is not defined. Please check your domain file.",
                         str(error.exception).replace("\"", ""))

    def test_method_no_name(self):
        # Define method with no name
        with self.assertRaises(SyntaxError) as error:
            Runner(self.test_tools_path + "basic/basic_domain_test_4.hddl", self.basic_pb1_path)
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
        # Rover Domain
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

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

    def test_parsing_predicates_1(self):
        # Blocks world domain
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld/Blocksworld_test_domain_1.hddl")

        self.assertIn('hand-empty', domain.predicates.keys())
        self.assertEqual('hand-empty', domain.predicates['hand-empty'].name)
        self.assertEqual(None, domain.predicates['hand-empty'].parameters)

        self.assertEqual('goal_on', domain.predicates['goal_on'].name)
        self.assertEqual('?t', domain.predicates['goal_on'].parameters[0].name)
        self.assertEqual(domain.types['block'], domain.predicates['goal_on'].parameters[0].type)
        self.assertEqual('?b', domain.predicates['goal_on'].parameters[1].name)
        self.assertEqual(domain.types['block'], domain.predicates['goal_on'].parameters[1].type)

        self.assertEqual(9, len(domain.predicates))

    def test_parsing_predicates_2(self):
        # Basic Domain
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.basic_domain_path)

        self.assertEqual('have', domain.predicates['have'].name)
        self.assertEqual(1, len(domain.predicates['have'].parameters))
        self.assertEqual('?a', domain.predicates['have'].parameters[0].name)
        self.assertEqual(None, domain.predicates['have'].parameters[0].type)
        self.assertEqual(1, len(domain.predicates.keys()))

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
        # Basic
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.basic_domain_path)

        self.assertEqual(['and', ['have', '?x'], ['not', ['have', '?y']]], domain.methods['have_first'].preconditions.conditions)
        self.assertEqual(['and', ['have', '?y'], ['not', ['have', '?x']]], domain.methods['have_second'].preconditions.conditions)
        self.assertEqual(['have', '?a'], domain.actions['drop'].preconditions.conditions)

        # Rover
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.rover_path + "rover-domain.hddl")

        self.assertEqual(['and', ['at', '?r', '?x'], ['at_lander', '?l', '?y'], ['have_soil_analysis', '?r', '?p'],
                          ['visible', '?x', '?y'], ['available', '?r'], ['channel_free', '?l']],
                         domain.actions['communicate_soil_data'].preconditions.conditions)
        self.assertEqual(['and', ['equipped_for_imaging', '?rover'], ['on_board', '?camera', '?rover'],
                          ['supports', '?camera', '?mode'], ['visible_from', '?objective', '?waypoint']],
                         domain.methods['m_get_image_data_ordering_0'].preconditions.conditions)

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
        self.assertEqual("rover", action.parameters[0].type.name)
        self.assertEqual("?p", action.parameters[1].name)
        self.assertEqual("waypoint", action.parameters[1].type.name)
        self.assertEqual("?o", action.parameters[2].name)
        self.assertEqual("objective", action.parameters[2].type.name)
        self.assertEqual("?i", action.parameters[3].name)
        self.assertEqual("camera", action.parameters[3].type.name)
        self.assertEqual("?m", action.parameters[4].name)
        self.assertEqual("mode", action.parameters[4].type.name)

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
        self.assertEqual(domain.actions['navigate'], domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[0].task)
        self.assertEqual("?rover", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[0].parameters[0].name)
        self.assertEqual("?from", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[0].parameters[1].name)
        self.assertEqual("?mid", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[0].parameters[2].name)

        self.assertEqual(domain.actions['visit'], domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[1].task)
        self.assertEqual("?mid", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[1].parameters[0].name)

        self.assertEqual(domain.actions['navigate'], domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[2].task)
        self.assertEqual("?rover", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[2].parameters[0].name)
        self.assertEqual("?mid", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[2].parameters[1].name)
        self.assertEqual("?mid", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[2].parameters[1].name)

        self.assertEqual(domain.actions['unvisit'], domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[3].task)
        self.assertEqual("?mid", domain.methods["m_navigate_abs_4_ordering_0"].subtasks.tasks[3].parameters[0].name)

    def test_parsing_effects(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.basic_domain_path)

        self.assertIn('pickup', domain.actions.keys())
        self.assertEqual(1, len(domain.actions['pickup'].effects.effects))
        self.assertEqual(False, domain.actions['pickup'].effects.effects[0].negated)
        self.assertEqual('have', domain.actions['pickup'].effects.effects[0].predicate)
        self.assertEqual(['?a'], domain.actions['pickup'].effects.effects[0].parameters)

    def test_parsing_effects_2(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.rover_path + "rover-domain.hddl")

        self.assertEqual(2, len(domain.actions['navigate'].effects.effects))
        self.assertEqual(True, domain.actions['navigate'].effects.effects[0].negated)
        self.assertEqual('at', domain.actions['navigate'].effects.effects[0].predicate)
        self.assertEqual(['?x', '?y'], domain.actions['navigate'].effects.effects[0].parameters)
        self.assertEqual(False, domain.actions['navigate'].effects.effects[1].negated)
        self.assertEqual('at', domain.actions['navigate'].effects.effects[1].predicate)
        self.assertEqual(['?x', '?z'], domain.actions['navigate'].effects.effects[1].parameters)

        self.assertEqual(4, len(domain.actions['sample_soil'].effects.effects))
        self.assertEqual(True, domain.actions['sample_soil'].effects.effects[0].negated)
        self.assertEqual('empty', domain.actions['sample_soil'].effects.effects[0].predicate)
        self.assertEqual(['?s'], domain.actions['sample_soil'].effects.effects[0].parameters)
        self.assertEqual(True, domain.actions['sample_soil'].effects.effects[1].negated)
        self.assertEqual('at_soil_sample', domain.actions['sample_soil'].effects.effects[1].predicate)
        self.assertEqual(['?p'], domain.actions['sample_soil'].effects.effects[1].parameters)
        self.assertEqual(False, domain.actions['sample_soil'].effects.effects[2].negated)
        self.assertEqual('full', domain.actions['sample_soil'].effects.effects[2].predicate)
        self.assertEqual(['?s'], domain.actions['sample_soil'].effects.effects[2].parameters)
        self.assertEqual(False, domain.actions['sample_soil'].effects.effects[3].negated)
        self.assertEqual('have_soil_analysis', domain.actions['sample_soil'].effects.effects[3].predicate)
        self.assertEqual(['?x', '?p'], domain.actions['sample_soil'].effects.effects[3].parameters)

        self.assertEqual(4, len(domain.actions['sample_rock'].effects.effects))
        self.assertEqual(True, domain.actions['sample_rock'].effects.effects[0].negated)
        self.assertEqual('empty', domain.actions['sample_rock'].effects.effects[0].predicate)
        self.assertEqual(['?s'], domain.actions['sample_rock'].effects.effects[0].parameters)
        self.assertEqual(True, domain.actions['sample_rock'].effects.effects[1].negated)
        self.assertEqual('at_rock_sample', domain.actions['sample_rock'].effects.effects[1].predicate)
        self.assertEqual(['?p'], domain.actions['sample_rock'].effects.effects[1].parameters)
        self.assertEqual(False, domain.actions['sample_rock'].effects.effects[2].negated)
        self.assertEqual('full', domain.actions['sample_rock'].effects.effects[2].predicate)
        self.assertEqual(['?s'], domain.actions['sample_rock'].effects.effects[2].parameters)
        self.assertEqual(False, domain.actions['sample_rock'].effects.effects[3].negated)
        self.assertEqual('have_rock_analysis', domain.actions['sample_rock'].effects.effects[3].predicate)
        self.assertEqual(['?x', '?p'], domain.actions['sample_rock'].effects.effects[3].parameters)

        self.assertEqual(2, len(domain.actions['drop'].effects.effects))
        self.assertEqual(True, domain.actions['drop'].effects.effects[0].negated)
        self.assertEqual('full', domain.actions['drop'].effects.effects[0].predicate)
        self.assertEqual(['?y'], domain.actions['drop'].effects.effects[0].parameters)
        self.assertEqual(False, domain.actions['drop'].effects.effects[1].negated)
        self.assertEqual('empty', domain.actions['drop'].effects.effects[1].predicate)
        self.assertEqual(['?y'], domain.actions['drop'].effects.effects[1].parameters)

        self.assertEqual(1, len(domain.actions['calibrate'].effects.effects))
        self.assertEqual(False, domain.actions['calibrate'].effects.effects[0].negated)
        self.assertEqual('calibrated', domain.actions['calibrate'].effects.effects[0].predicate)
        self.assertEqual(['?i', '?r'], domain.actions['calibrate'].effects.effects[0].parameters)

        self.assertEqual(2, len(domain.actions['take_image'].effects.effects))
        self.assertEqual(True, domain.actions['take_image'].effects.effects[0].negated)
        self.assertEqual('calibrated', domain.actions['take_image'].effects.effects[0].predicate)
        self.assertEqual(['?i', '?r'], domain.actions['take_image'].effects.effects[0].parameters)
        self.assertEqual(False, domain.actions['take_image'].effects.effects[1].negated)
        self.assertEqual('have_image', domain.actions['take_image'].effects.effects[1].predicate)
        self.assertEqual(['?r', '?o', '?m'], domain.actions['take_image'].effects.effects[1].parameters)

        self.assertEqual(3, len(domain.actions['communicate_soil_data'].effects.effects))
        self.assertEqual(False, domain.actions['communicate_soil_data'].effects.effects[0].negated)
        self.assertEqual('channel_free', domain.actions['communicate_soil_data'].effects.effects[0].predicate)
        self.assertEqual(['?l'], domain.actions['communicate_soil_data'].effects.effects[0].parameters)
        self.assertEqual(False, domain.actions['communicate_soil_data'].effects.effects[1].negated)
        self.assertEqual('communicated_soil_data', domain.actions['communicate_soil_data'].effects.effects[1].predicate)
        self.assertEqual(['?p'], domain.actions['communicate_soil_data'].effects.effects[1].parameters)
        self.assertEqual(False, domain.actions['communicate_soil_data'].effects.effects[2].negated)
        self.assertEqual('available', domain.actions['communicate_soil_data'].effects.effects[2].predicate)
        self.assertEqual(['?r'], domain.actions['communicate_soil_data'].effects.effects[2].parameters)

        self.assertEqual(3, len(domain.actions['communicate_rock_data'].effects.effects))
        self.assertEqual(False, domain.actions['communicate_rock_data'].effects.effects[0].negated)
        self.assertEqual('channel_free', domain.actions['communicate_rock_data'].effects.effects[0].predicate)
        self.assertEqual(['?l'], domain.actions['communicate_rock_data'].effects.effects[0].parameters)
        self.assertEqual(False, domain.actions['communicate_rock_data'].effects.effects[1].negated)
        self.assertEqual('communicated_rock_data', domain.actions['communicate_rock_data'].effects.effects[1].predicate)
        self.assertEqual(['?p'], domain.actions['communicate_rock_data'].effects.effects[1].parameters)
        self.assertEqual(False, domain.actions['communicate_rock_data'].effects.effects[2].negated)
        self.assertEqual('available', domain.actions['communicate_rock_data'].effects.effects[2].predicate)
        self.assertEqual(['?r'], domain.actions['communicate_rock_data'].effects.effects[2].parameters)

        self.assertEqual(3, len(domain.actions['communicate_image_data'].effects.effects))
        self.assertEqual(False, domain.actions['communicate_image_data'].effects.effects[0].negated)
        self.assertEqual('channel_free', domain.actions['communicate_image_data'].effects.effects[0].predicate)
        self.assertEqual(['?l'], domain.actions['communicate_image_data'].effects.effects[0].parameters)
        self.assertEqual(False, domain.actions['communicate_image_data'].effects.effects[1].negated)
        self.assertEqual('communicated_image_data', domain.actions['communicate_image_data'].effects.effects[1].predicate)
        self.assertEqual(['?o', '?m'], domain.actions['communicate_image_data'].effects.effects[1].parameters)
        self.assertEqual(False, domain.actions['communicate_image_data'].effects.effects[2].negated)
        self.assertEqual('available', domain.actions['communicate_image_data'].effects.effects[2].predicate)
        self.assertEqual(['?r'], domain.actions['communicate_image_data'].effects.effects[2].parameters)

        self.assertEqual(1, len(domain.actions['visit'].effects.effects))
        self.assertEqual(False, domain.actions['visit'].effects.effects[0].negated)
        self.assertEqual('visited', domain.actions['visit'].effects.effects[0].predicate)
        self.assertEqual(['?waypoint'], domain.actions['visit'].effects.effects[0].parameters)

        self.assertEqual(1, len(domain.actions['unvisit'].effects.effects))
        self.assertEqual(True, domain.actions['unvisit'].effects.effects[0].negated)
        self.assertEqual('visited', domain.actions['unvisit'].effects.effects[0].predicate)
        self.assertEqual(['?waypoint'], domain.actions['unvisit'].effects.effects[0].parameters)

    def test_parsing_subtasks(self):
        # Basic
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.basic_domain_path)

        self.assertEqual(2, len(domain.methods['have_first'].subtasks.tasks))
        self.assertEqual('drop', domain.methods['have_first'].subtasks.tasks[0].task.name)
        self.assertEqual(1, len(domain.methods['have_first'].subtasks.tasks[0].task.parameters))
        self.assertEqual('?x', domain.methods['have_first'].subtasks.tasks[0].parameters[0].name)
        self.assertEqual('pickup', domain.methods['have_first'].subtasks.tasks[1].task.name)
        self.assertEqual(1, len(domain.methods['have_first'].subtasks.tasks[1].parameters))
        self.assertEqual('?y', domain.methods['have_first'].subtasks.tasks[1].parameters[0].name)

        self.assertEqual(2, len(domain.methods['have_second'].subtasks.tasks))
        self.assertEqual('drop', domain.methods['have_second'].subtasks.tasks[0].task.name)
        self.assertEqual(1, len(domain.methods['have_second'].subtasks.tasks[0].parameters))
        self.assertEqual('?y', domain.methods['have_second'].subtasks.tasks[0].parameters[0].name)
        self.assertEqual('pickup', domain.methods['have_second'].subtasks.tasks[1].task.name)
        self.assertEqual(1, len(domain.methods['have_second'].subtasks.tasks[1].parameters))
        self.assertEqual('?x', domain.methods['have_second'].subtasks.tasks[1].parameters[0].name)

    def test_parsing_subtasks_2(self):
        # Rover
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.rover_path + "rover-domain.hddl")

        self.assertEqual(None, domain.methods['m_empty_store_1_ordering_0'].subtasks)

        self.assertEqual(1, len(domain.methods['m_empty_store_2_ordering_0'].subtasks.tasks))
        self.assertEqual(1, len(domain.methods['m_empty_store_2_ordering_0'].subtasks.labelled_tasks))
        self.assertEqual(['task0'], list(domain.methods['m_empty_store_2_ordering_0'].subtasks.labelled_tasks.keys()))
        self.assertEqual(domain.methods['m_empty_store_2_ordering_0'].subtasks.tasks[0],
                         domain.methods['m_empty_store_2_ordering_0'].subtasks.labelled_tasks['task0'])
        self.assertEqual(domain.actions['drop'], domain.methods['m_empty_store_2_ordering_0'].subtasks.tasks[0].task)
        self.assertEqual(2, len(domain.methods['m_empty_store_2_ordering_0'].subtasks.tasks[0].parameters))
        self.assertEqual('?rover', domain.methods['m_empty_store_2_ordering_0'].subtasks.tasks[0].parameters[0].name)
        self.assertEqual('?s', domain.methods['m_empty_store_2_ordering_0'].subtasks.tasks[0].parameters[1].name)

        self.assertEqual(3, len(domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks))
        self.assertEqual(3, len(domain.methods['m_navigate_abs_1_ordering_0'].subtasks.labelled_tasks))
        self.assertEqual(['task0', 'task1', 'task2'], list(domain.methods['m_navigate_abs_1_ordering_0'].subtasks.labelled_tasks.keys()))
        self.assertEqual(domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[0],
                         domain.methods['m_navigate_abs_1_ordering_0'].subtasks.labelled_tasks['task0'])
        self.assertEqual(domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[1],
                         domain.methods['m_navigate_abs_1_ordering_0'].subtasks.labelled_tasks['task1'])
        self.assertEqual(domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[2],
                         domain.methods['m_navigate_abs_1_ordering_0'].subtasks.labelled_tasks['task2'])
        self.assertEqual(domain.actions['visit'], domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[0].task)
        self.assertEqual(1, len(domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[0].parameters))
        self.assertEqual('?from', domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[0].parameters[0].name)
        self.assertEqual(domain.actions['navigate'], domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[1].task)
        self.assertEqual(3, len(domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[1].parameters))
        self.assertEqual('?rover', domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[1].parameters[0].name)
        self.assertEqual('?from', domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[1].parameters[1].name)
        self.assertEqual('?to', domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[1].parameters[2].name)
        self.assertEqual(1, len(domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[2].parameters))
        self.assertEqual('?from', domain.methods['m_navigate_abs_1_ordering_0'].subtasks.tasks[2].parameters[0].name)

    def test_parsing_basic_pb1(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.basic_domain_path)
        parser.parse_problem(self.basic_pb1_path)

        # Check initial state
        self.assertEqual(1, len(problem.initial_state.elements))
        self.assertEqual('have', problem.initial_state.elements[0].predicate.name)
        self.assertEqual(1, len(problem.initial_state.elements[0].objects))
        self.assertEqual('kiwi', problem.initial_state.elements[0].objects[0].name)
        self.assertEqual(None, problem.initial_state.elements[0].objects[0].type)

        # Check objects
        self.assertEqual(2, len(problem.objects))
        self.assertEqual('kiwi', problem.objects['kiwi'].name)
        self.assertEqual(None, problem.objects['kiwi'].type)
        self.assertEqual('banjo', problem.objects['banjo'].name)
        self.assertEqual(None, problem.objects['banjo'].type)

        # Check subtasks - must be subtask object
        self.assertEqual(1, len(problem.subtasks.tasks))
        self.assertEqual('swap', problem.subtasks.tasks[0].task.name)
        self.assertEqual(2, len(problem.subtasks.tasks[0].parameters))
        self.assertEqual('banjo', problem.subtasks.tasks[0].parameters[0].name)
        self.assertEqual(None, problem.subtasks.tasks[0].parameters[0].type)
        self.assertEqual(Object, type(problem.subtasks.tasks[0].parameters[0]))
        self.assertEqual('kiwi', problem.subtasks.tasks[0].parameters[1].name)
        self.assertEqual(None, problem.subtasks.tasks[0].parameters[1].type)
        self.assertEqual(Object, type(problem.subtasks.tasks[0].parameters[1]))

    def test_parsing_rover_pb1(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.rover_path + "rover-domain.hddl")
        parser.parse_problem(self.rover_path + "pfile01.hddl")

        # Check initial state
        self.assertEqual(45, len(problem.initial_state.elements))
        self.assertEqual('visible', problem.initial_state.elements[0].predicate.name)
        self.assertEqual(2, len(problem.initial_state.elements[0].objects))
        self.assertEqual('waypoint1', problem.initial_state.elements[0].objects[0].name)
        self.assertEqual(domain.types['waypoint'], problem.initial_state.elements[0].objects[0].type)
        self.assertEqual('waypoint0', problem.initial_state.elements[0].objects[1].name)
        self.assertEqual(domain.types['waypoint'], problem.initial_state.elements[0].objects[1].type)

        self.assertEqual('at_soil_sample', problem.initial_state.elements[12].predicate.name)
        self.assertEqual(1, len(problem.initial_state.elements[12].objects))
        self.assertEqual('waypoint0', problem.initial_state.elements[12].objects[0].name)
        self.assertEqual(domain.types['waypoint'], problem.initial_state.elements[12].objects[0].type)

        self.assertEqual('at_rock_sample', problem.initial_state.elements[17].predicate.name)
        self.assertEqual(1, len(problem.initial_state.elements[17].objects))
        self.assertEqual('waypoint3', problem.initial_state.elements[17].objects[0].name)
        self.assertEqual(domain.types['waypoint'], problem.initial_state.elements[17].objects[0].type)

        self.assertEqual('can_traverse', problem.initial_state.elements[27].predicate.name)
        self.assertEqual(3, len(problem.initial_state.elements[27].objects))
        self.assertEqual('rover0', problem.initial_state.elements[27].objects[0].name)
        self.assertEqual(domain.types['rover'], problem.initial_state.elements[27].objects[0].type)
        self.assertEqual('waypoint3', problem.initial_state.elements[27].objects[1].name)
        self.assertEqual(domain.types['waypoint'], problem.initial_state.elements[27].objects[1].type)
        self.assertEqual('waypoint0', problem.initial_state.elements[27].objects[2].name)
        self.assertEqual(domain.types['waypoint'], problem.initial_state.elements[27].objects[2].type)

        # Check objects
        self.assertEqual(13, len(problem.objects))
        self.assertEqual('waypoint0', problem.objects['waypoint0'].name)
        self.assertEqual(domain.types['waypoint'], problem.objects['waypoint0'].type)
        self.assertEqual('waypoint1', problem.objects['waypoint1'].name)
        self.assertEqual(domain.types['waypoint'], problem.objects['waypoint1'].type)
        self.assertEqual('waypoint2', problem.objects['waypoint2'].name)
        self.assertEqual(domain.types['waypoint'], problem.objects['waypoint2'].type)
        self.assertEqual('waypoint3', problem.objects['waypoint3'].name)
        self.assertEqual(domain.types['waypoint'], problem.objects['waypoint3'].type)

        self.assertEqual('colour', problem.objects['colour'].name)
        self.assertEqual(domain.types['mode'], problem.objects['colour'].type)
        self.assertEqual('high_res', problem.objects['high_res'].name)
        self.assertEqual(domain.types['mode'], problem.objects['high_res'].type)
        self.assertEqual('low_res', problem.objects['low_res'].name)
        self.assertEqual(domain.types['mode'], problem.objects['low_res'].type)

        self.assertEqual('rover0store', problem.objects['rover0store'].name)
        self.assertEqual(domain.types['store'], problem.objects['rover0store'].type)
        self.assertEqual('rover0', problem.objects['rover0'].name)
        self.assertEqual(domain.types['rover'], problem.objects['rover0'].type)
        self.assertEqual('camera0', problem.objects['camera0'].name)
        self.assertEqual(domain.types['camera'], problem.objects['camera0'].type)
        self.assertEqual('general', problem.objects['general'].name)
        self.assertEqual(domain.types['lander'], problem.objects['general'].type)

        self.assertEqual('objective0', problem.objects['objective0'].name)
        self.assertEqual(domain.types['objective'], problem.objects['objective0'].type)
        self.assertEqual('objective1', problem.objects['objective1'].name)
        self.assertEqual(domain.types['objective'], problem.objects['objective1'].type)

        # Check subtasks and orderings
        self.assertEqual(3, len(problem.subtasks.tasks))
        self.assertEqual('get_image_data', problem.subtasks.tasks[0].task.name)
        self.assertEqual(2, len(problem.subtasks.tasks[0].parameters))
        self.assertEqual('objective1', problem.subtasks.tasks[0].parameters[0].name)
        self.assertEqual(domain.types['objective'], problem.subtasks.tasks[0].parameters[0].type)
        self.assertEqual(Object, type(problem.subtasks.tasks[0].parameters[0]))
        self.assertEqual('high_res', problem.subtasks.tasks[0].parameters[1].name)
        self.assertEqual(domain.types['mode'], problem.subtasks.tasks[0].parameters[1].type)
        self.assertEqual(Object, type(problem.subtasks.tasks[0].parameters[1]))
        self.assertEqual(problem.subtasks.tasks[0], problem.subtasks.labelled_tasks['task2'])

        self.assertEqual('get_soil_data', problem.subtasks.tasks[1].task.name)
        self.assertEqual(1, len(problem.subtasks.tasks[1].parameters))
        self.assertEqual('waypoint2', problem.subtasks.tasks[1].parameters[0].name)
        self.assertEqual(domain.types['waypoint'], problem.subtasks.tasks[1].parameters[0].type)
        self.assertEqual(Object, type(problem.subtasks.tasks[1].parameters[0]))
        self.assertEqual(problem.subtasks.tasks[1], problem.subtasks.labelled_tasks['task0'])

        self.assertEqual('get_rock_data', problem.subtasks.tasks[2].task.name)
        self.assertEqual(1, len(problem.subtasks.tasks[2].parameters))
        self.assertEqual('waypoint3', problem.subtasks.tasks[2].parameters[0].name)
        self.assertEqual(domain.types['waypoint'], problem.subtasks.tasks[2].parameters[0].type)
        self.assertEqual(Object, type(problem.subtasks.tasks[2].parameters[0]))
        self.assertEqual(problem.subtasks.tasks[2], problem.subtasks.labelled_tasks['task1'])

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
