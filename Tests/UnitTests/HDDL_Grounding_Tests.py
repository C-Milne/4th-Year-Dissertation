import unittest
from runner import Runner
from Internal_Representation.precondition import Precondition
from Solver.model import Model
from Parsers.HDDL_Parser import HDDLParser
from Internal_Representation.method import Method
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Internal_Representation.modifier import Modifier
from Solver.solver import Solver
from Internal_Representation.predicate import Predicate
from Internal_Representation.state import State
from Internal_Representation.problem_predicate import ProblemPredicate
from Internal_Representation.parameter import Parameter
from Internal_Representation.Object import Object


class HDDLGroundingTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"
        self.test_tools_path = "TestTools/"
        self.blocksworld_path = "../Examples/Blocksworld/"
        self.rover_path = "../Examples/IPC_Tests/Rover/"

    # def test_blocksworld_pb1_initial_state(self):
    #     domain = Domain(None)
    #     problem = Problem(domain)
    #     domain.add_problem(problem)
    #
    #     # Test preconditions
    #     parser = HDDLParser(domain, problem)
    #     parser.parse_domain(self.blocksworld_path + "domain.hddl")
    #     parser.parse_problem(self.blocksworld_path + "pb1.hddl")
    #
    #     solver = Solver(domain, problem)
    #     model = Model(solver.problem, solver, solver._available_modifiers)
    #
    #     # Check all values are correct before execution of action
    #     blocksworld_pb1_initial_state = ['hand-empty', ['clear', 'b3'],
    #                                      ['on-table', 'b2'], ['on', 'b3', 'b5'], ['on', 'b5', 'b4'],
    #                                      ['on', 'b4', 'b2'],
    #                                      ['clear', 'b1'], ['on-table', 'b1'], ['goal_clear', 'b2'],
    #                                      ['goal_on-table', 'b4'],
    #                                      ['goal_on', 'b2', 'b5'], ['goal_on', 'b5', 'b4'], ['goal_clear', 'b1'],
    #                                      ['goal_on-table', 'b3'], ['goal_on', 'b1', 'b3']]
    #     blocksworld_pb1_initial_state_index = {'hand-empty': [0], 'clear': [1, 6], 'goal_clear': [8, 12],
    #                                            'goal_on': [10, 11, 14], 'goal_on-table': [9, 13],
    #                                            'on': [3, 4, 5], 'on-table': [2, 7]}
    #     self.assertEqual(blocksworld_pb1_initial_state, model.current_state.elements)
    #     self.assertEqual(blocksworld_pb1_initial_state_index, model.current_state._index)

    def test_precondition_complex(self):
        # Devise a complex precondition and test it
        precon_list = ['and',
                       ['not',
                        ['and', ['have', '?y'], ['have', '?a']]
                        ],
                       ['and',
                        ['have', '?x'], ['or', ['have', '?b'], ['have', '?c']]
                        ],
                       ['or',
                        ['hate', '?z'], ['hate', '?d']
                        ]
                       ]
        precons = Precondition(precon_list)

        # Set up values
        have_pred = Predicate('have', [Parameter('?x')])
        hate_pred = Predicate('hate', [Parameter('?a')])

        ob_ham = Object("ham")
        ob_irnbru = Object('irn-bru')
        ob_car = Object('car')
        ob_bike = Object('bike')
        ob_popcorn = Object('popcorn')
        ob_crisps = Object('crisps')
        ob_dark = Object('dark')

        # Set up model - {'have': ['ham', 'irn-bru', 'car'], 'hate': []}
        state = State()
        state.add_element(ProblemPredicate(have_pred, [ob_ham]))
        state.add_element(ProblemPredicate(have_pred, [ob_irnbru]))
        state.add_element(ProblemPredicate(have_pred, [ob_car]))

        model = Model(state, [])
        param_dict = {"?z": ob_ham, "?x": ob_irnbru, "?y": ob_car, "?a": ob_bike, "?b": ob_popcorn,
                      "?c": ob_crisps, "?d": ob_dark}

        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

        # Set up next model - {'have': ['ham', 'irn-bru', 'car', 'popcorn'], 'hate': ['dark']}
        state.add_element(ProblemPredicate(have_pred, [ob_popcorn]))
        state.add_element(ProblemPredicate(hate_pred, [ob_dark]))
        model = Model(state, [])
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

    def test_method_requirements(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld/Blocksworld_test_domain_2.hddl")

        # Add some assertions for this - seems too work (perhaps not for 'forall' methods)
        self.assertEqual(2, len(domain.methods['pickup-ready-block'].requirements))
        self.assertEqual({'type': None, 'predicates': {'and': {'clear': 1, 'not': {'done': 1}, 'goal_on': 1}}},
                         domain.methods['pickup-ready-block'].requirements['?b'])
        self.assertEqual({'type': domain.types['block'],
                          'predicates': {'and': {'goal_on': 2, 'done': 1, 'clear': 1}}},
                         domain.methods['pickup-ready-block'].requirements['?d'])

    def test_forall_preconditions(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld/Blocksworld_test_domain_1.hddl")
        parser.parse_problem(self.test_tools_path + "Blocksworld/Blocksworld_test_problem_1.hddl")
        method = domain.methods['setdone']
        model = Model(problem.initial_state, [], None, problem)
        result = method.evaluate_preconditions(model, {})
        self.assertEqual(False, result)

        # Test for True
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld/Blocksworld_test_domain_1.hddl")
        parser.parse_problem(self.test_tools_path + "Blocksworld/Blocksworld_test_problem_1_1.hddl")
        method = domain.methods['setdone']
        model = Model(problem.initial_state, [], None, problem)
        result = method.evaluate_preconditions(model, {})
        self.assertEqual(True, result)

    def test_precondition_and(self):
        # Test the 'and' functionality for preconditions
        # Set up values
        have_pred = Predicate('have', [Parameter('?x')])
        ob_ham = Object("ham")
        ob_irnbru = Object('irn-bru')
        ob_car = Object('car')

        # Set up precondition object
        precon_list = ['and', ['have', '?x'], ['have', '?y'], ['have', '?z']]
        precons = Precondition(precon_list)

        # Set up model - {'have': ['ham', 'irn-bru', 'car']}
        state = State()
        state.add_element(ProblemPredicate(have_pred, [ob_ham]))
        state.add_element(ProblemPredicate(have_pred, [ob_irnbru]))
        state.add_element(ProblemPredicate(have_pred, [ob_car]))
        model = Model(state, [])
        param_dict = {"?z": ob_ham, "?x": ob_irnbru, "?y": ob_car}

        # Testing for True
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        # Testing for False - {'have': ['irn-bru', 'car']}
        state = State()
        state.add_element(ProblemPredicate(have_pred, [ob_irnbru]))
        state.add_element(ProblemPredicate(have_pred, [ob_car]))
        model = Model(state, [])
        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

    def test_precondition_or(self):
        # Test the 'or' functionality for preconditions
        # Set up precondition object
        precon_list = ['or', ['have', '?x'], ['have', '?y'], ['have', '?z']]
        precons = Precondition(precon_list)

        # Set up values
        have_pred = Predicate('have', [Parameter('?x')])
        ob_ham = Object("ham")
        ob_irnbru = Object('irn-bru')
        ob_car = Object('car')

        # Set up model - {'have': ['ham', 'irn-bru', 'car']}
        state = State()
        state.add_element(ProblemPredicate(have_pred, [ob_ham]))
        state.add_element(ProblemPredicate(have_pred, [ob_irnbru]))
        state.add_element(ProblemPredicate(have_pred, [ob_car]))
        model = Model(state, [])
        param_dict = {"?z": ob_ham, "?x": ob_irnbru, "?y": ob_car}

        # Testing for True
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        # Testing for True - {'have': ['irn-bru', 'car']}
        state = State()
        state.add_element(ProblemPredicate(have_pred, [ob_irnbru]))
        state.add_element(ProblemPredicate(have_pred, [ob_car]))
        model = Model(state, [])
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        # {'have': ['irn-bru']}
        state = State()
        state.add_element(ProblemPredicate(have_pred, [ob_irnbru]))
        model = Model(state, [])
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        # {'have': []}
        state = State()
        model = Model(state, [])
        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

    def test_precondition_not(self):
        # Test the 'not' functionality for preconditions
        # Set up precondition object
        precon_list = ['not', ['have', '?x']]
        precons = Precondition(precon_list)

        # Set up values
        have_pred = Predicate('have', [Parameter('?x')])
        ob_ham = Object("ham")
        ob_irnbru = Object('irn-bru')
        ob_car = Object('car')

        # Set up model - {'have': ['ham', 'irn-bru', 'car']}
        state = State()
        state.add_element(ProblemPredicate(have_pred, [ob_ham]))
        state.add_element(ProblemPredicate(have_pred, [ob_irnbru]))
        state.add_element(ProblemPredicate(have_pred, [ob_car]))
        model = Model(state, [])
        param_dict = {"?z": ob_ham, "?x": ob_irnbru, "?y": ob_car}

        # Testing for False
        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

        # Testing for True - {'have': ['ham', 'car']}
        state = State()
        state.add_element(ProblemPredicate(have_pred, [ob_ham]))
        state.add_element(ProblemPredicate(have_pred, [ob_car]))
        model = Model(state, [])
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

    def test_action_requirements(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Rover/domain2.hddl")

        # Check action requirements
        self.assertEqual(domain.types['rover'], domain.actions['take_image'].requirements['?r']['type'])
        self.assertEqual({'and': {'calibrated': 2, 'on_board': 2, 'equipped_for_imaging': 1, 'at': 1}},
                         domain.actions['take_image'].requirements['?r']['predicates'])

        self.assertEqual(domain.types['waypoint'], domain.actions['take_image'].requirements['?p']['type'])
        self.assertEqual({'and': {'visible_from': 2, 'at': 2}},
                         domain.actions['take_image'].requirements['?p']['predicates'])

        self.assertEqual(domain.types['objective'], domain.actions['take_image'].requirements['?o']['type'])
        self.assertEqual({'and': {'visible_from': 1}}, domain.actions['take_image'].requirements['?o']['predicates'])

        self.assertEqual(domain.types['camera'], domain.actions['take_image'].requirements['?i']['type'])
        self.assertEqual({'and': {'calibrated': 1, 'on_board': 1, 'supports': 1}},
                         domain.actions['take_image'].requirements['?i']['predicates'])

        self.assertEqual(domain.types['mode'], domain.actions['take_image'].requirements['?m']['type'])
        self.assertEqual({'and': {'supports': 2}}, domain.actions['take_image'].requirements['?m']['predicates'])

    def test_task_method_grounding(self):
        # Check that methods corresponding to a task are being stored correctly
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.rover_path + "rover-domain.hddl")
        t = domain.get_task('calibrate_abs')
        self.assertIn(domain.get_method('m_calibrate_abs_ordering_0'), t.methods)

        t = domain.get_task('empty_store')
        self.assertIn(domain.get_method('m_empty_store_1_ordering_0'), t.methods)
        self.assertIn(domain.get_method('m_empty_store_2_ordering_0'), t.methods)

        t = domain.get_task('get_image_data')
        self.assertIn(domain.get_method('m_get_image_data_ordering_0'), t.methods)

        t = domain.get_task('get_rock_data')
        self.assertIn(domain.get_method('m_get_rock_data_ordering_0'), t.methods)

        t = domain.get_task('get_soil_data')
        self.assertIn(domain.get_method('m_get_soil_data_ordering_0'), t.methods)

        t = domain.get_task('navigate_abs')
        self.assertIn(domain.get_method('m_navigate_abs_1_ordering_0'), t.methods)
        self.assertIn(domain.get_method('m_navigate_abs_2_ordering_0'), t.methods)
        self.assertIn(domain.get_method('m_navigate_abs_3_ordering_0'), t.methods)
        self.assertIn(domain.get_method('m_navigate_abs_4_ordering_0'), t.methods)

        t = domain.get_task('send_image_data')
        self.assertIn(domain.get_method('m_send_image_data_ordering_0'), t.methods)

        t = domain.get_task('send_rock_data')
        self.assertIn(domain.get_method('m_send_rock_data_ordering_0'), t.methods)

        t = domain.get_task('send_soil_data')
        self.assertIn(domain.get_method('m_send_soil_data_ordering_0'), t.methods)

    def test_method_subtask_grounding(self):
        # Check that method subtasks hold reference to action/task not only string
        # rover domain
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.rover_path + "rover-domain.hddl")

        method_keys = list(domain.methods.keys())
        for m in method_keys:
            subtasks = domain.methods[m].subtasks
            if subtasks is not None:
                for t in subtasks.tasks:
                    # print("Method: {}\tSubtask: {}".format(m, t.task))
                    self.assertIsInstance(t.task, Modifier)

    def test_action_effects(self):
        # basic domain
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.basic_domain_path)

        self.assertEqual(Predicate, type(domain.actions['pickup'].effects.effects[0].predicate))
        self.assertEqual(False, domain.actions['pickup'].effects.effects[0].negated)
        self.assertEqual(Predicate, type(domain.actions['drop'].effects.effects[0].predicate))
        self.assertEqual(True, domain.actions['drop'].effects.effects[0].negated)

    # Ground objects to types? - would make for quicker look-ups in problem.get_objects_of_type()
