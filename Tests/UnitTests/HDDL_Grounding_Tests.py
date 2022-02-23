import unittest
from runner import Runner
from Internal_Representation.precondition import Precondition
from Solver.model import Model
from Parsers.HDDL_Parser import HDDLParser
from Internal_Representation.method import Method
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Solver.solver import Solver


class HDDLGroundingTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"
        self.test_tools_path = "TestTools/"
        self.blocksworld_path = "../Examples/Blocksworld/"

    def test_blocksworld_pb1_initial_state(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.blocksworld_path + "domain.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        solver = Solver(domain, problem)
        model = Model(solver.problem, solver, solver._available_modifiers)

        # Check all values are correct before execution of action
        blocksworld_pb1_initial_state = ['hand-empty', ['clear', 'b3'],
                                              ['on-table', 'b2'], ['on', 'b3', 'b5'], ['on', 'b5', 'b4'],
                                              ['on', 'b4', 'b2'],
                                              ['clear', 'b1'], ['on-table', 'b1'], ['goal_clear', 'b2'],
                                              ['goal_on-table', 'b4'],
                                              ['goal_on', 'b2', 'b5'], ['goal_on', 'b5', 'b4'], ['goal_clear', 'b1'],
                                              ['goal_on-table', 'b3'], ['goal_on', 'b1', 'b3']]
        blocksworld_pb1_initial_state_index = {'hand-empty': [0], 'clear': [1, 6], 'goal_clear': [8, 12],
                                                    'goal_on': [10, 11, 14], 'goal_on-table': [9, 13],
                                                    'on': [3, 4, 5], 'on-table': [2, 7]}
        self.assertEqual(blocksworld_pb1_initial_state, model.current_state.elements)
        self.assertEqual(blocksworld_pb1_initial_state_index, model.current_state._index)