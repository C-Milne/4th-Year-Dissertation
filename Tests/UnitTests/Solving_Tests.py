import unittest
from runner import Runner
from Internal_Representation.precondition import Precondition
from Solver.model import Model
from Solver.solver import Solver
from Parsers.HDDL_Parser import HDDLParser
from Internal_Representation.method import Method
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem


class SolvingTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"
        self.test_tools_path = "TestTools/"
        self.blocksworld_path = "../Examples/Blocksworld/"

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

    def test_model_requirement_satisfier_2(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld_test_domain_4.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        model = Model(problem, None, [domain.methods["pickup-ready-block"]])
        self.assertEqual(0, len(model.ready_modifiers))

    def test_action_execution(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.blocksworld_path + "domain.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        solver = Solver(domain, problem)
        model = Model(solver.problem, solver, solver._available_modifiers)
        action = domain.get_action("pickup") # b1

        solver._Solver__execute(model, action, {'?b': problem.get_object("b1")})

        # Check model.current_state.elements
        self.assertEqual([['clear', 'b3'],['on-table', 'b2'], ['on', 'b3', 'b5'],
        ['on', 'b5', 'b4'], ['on', 'b4', 'b2'],
        ['goal_clear', 'b2'], ['goal_on-table', 'b4'],['goal_on', 'b2', 'b5'],
        ['goal_on', 'b5', 'b4'], ['goal_clear', 'b1'],['goal_on-table', 'b3'],
        ['goal_on', 'b1', 'b3'], ['holding', 'b1']], model.current_state.elements)
        # Check model.current_state._index
        self.assertEqual({'clear': [0],'goal_clear': [5, 9],
        'goal_on': [7, 8, 11],'goal_on-table': [6, 10],'on': [2, 3, 4],
        'on-table': [1],'holding':[12]}, model.current_state._index)

    def test_action_execution_2(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.blocksworld_path + "domain.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        solver = Solver(domain, problem)
        model = Model(solver.problem, solver, solver._available_modifiers)
        action = domain.get_action("mark_done") # b3
        solver._Solver__execute(model, action, {'?b': problem.get_object("b3")})

        # Check elements list
        expected_elements = ['hand-empty', ['clear', 'b3'],
                          ['on-table', 'b2'], ['on', 'b3', 'b5'], ['on', 'b5', 'b4'],['on', 'b4', 'b2'],
                          ['clear', 'b1'], ['on-table', 'b1'], ['goal_clear', 'b2'],['goal_on-table', 'b4'],
                          ['goal_on', 'b2', 'b5'], ['goal_on', 'b5', 'b4'], ['goal_clear', 'b1'],
                          ['goal_on-table', 'b3'], ['goal_on', 'b1', 'b3'], ['done', 'b3']]
        self.assertEqual(expected_elements, model.current_state.elements)

        expected_index = {'hand-empty': [0], 'clear': [1, 6], 'goal_clear': [8, 12],
                            'goal_on': [10, 11, 14], 'goal_on-table': [9, 13],
                            'on': [3, 4, 5], 'on-table': [2, 7], 'done': [15]}
        # Check _index dictionary
        self.assertEqual(expected_index, model.current_state._index)

    def test_action_execution_3(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.blocksworld_path + "domain.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        solver = Solver(domain, problem)
        model = Model(solver.problem, solver, solver._available_modifiers)

        action = domain.get_action("pickup")  # b1
        solver._Solver__execute(model, action, {'?b': problem.get_object("b1")})

        action = domain.get_action("stack")
        solver._Solver__execute(model, action, {'?top': problem.get_object("b1"),
                                                '?bottom': problem.get_object("b3")})

        # Check elements list
        expected_elements = [['on-table', 'b2'], ['on', 'b3', 'b5'],
        ['on', 'b5', 'b4'], ['on', 'b4', 'b2'],
        ['goal_clear', 'b2'], ['goal_on-table', 'b4'],['goal_on', 'b2', 'b5'],
        ['goal_on', 'b5', 'b4'], ['goal_clear', 'b1'],['goal_on-table', 'b3'],
        ['goal_on', 'b1', 'b3'], 'hand-empty', ['on', 'b1', 'b3'], ['clear', 'b1']]
        self.assertEqual(expected_elements, model.current_state.elements)

        expected_index = {'goal_clear': [4, 8],
        'goal_on': [6, 7, 10],'goal_on-table': [5, 9],'on': [1, 2, 3, 12],
        'on-table': [0], 'hand-empty':[11], 'clear':[13]}
        # Check _index dictionary
        self.assertEqual(expected_index, model.current_state._index)

    def test_action_execution_4(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.blocksworld_path + "domain.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        solver = Solver(domain, problem)
        model = Model(solver.problem, solver, solver._available_modifiers)
        action = domain.get_action("unstack")
        solver._Solver__execute(model, action, {'?top': problem.get_object("b3"),
                                                '?bottom' : problem.get_object("b5")})

        # Check elements list
        expected_elements = [['on-table', 'b2'], ['on', 'b5', 'b4'], ['on', 'b4', 'b2'],
                             ['clear', 'b1'], ['on-table', 'b1'], ['goal_clear', 'b2'],
                             ['goal_on-table', 'b4'],['goal_on', 'b2', 'b5'],
                             ['goal_on', 'b5', 'b4'], ['goal_clear', 'b1'],
                             ['goal_on-table', 'b3'], ['goal_on', 'b1', 'b3'],
                             ['holding', 'b3'], ['clear', 'b5']]
        self.assertEqual(expected_elements, model.current_state.elements)

        expected_index = {'clear': [3, 13], 'goal_clear': [5, 9],
                          'goal_on': [7, 8, 11], 'goal_on-table': [6, 10],
                          'on': [1, 2], 'on-table': [0, 4], 'holding': [12]}
        # Check _index dictionary
        self.assertEqual(expected_index, model.current_state._index)

    def test_precondition_evaluation(self):
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