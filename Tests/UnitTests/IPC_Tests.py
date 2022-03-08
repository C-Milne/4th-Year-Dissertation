import unittest
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Parsers.HDDL_Parser import HDDLParser
from Solver.solver import Solver
from TestTools.env_setup import env_setup


class IPCTests(unittest.TestCase):

    def setUp(self) -> None:
        self.IPC_Tests_path = "../Examples/IPC_Tests/"

    def test_1_empty_method(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.IPC_Tests_path + "test01_empty_method/domain.hddl")
        parser.parse_problem(self.IPC_Tests_path + "test01_empty_method/problem.hddl")
        solver = Solver(domain, problem)
        plan = solver.solve()
        solver.output(plan)

        self.assertEqual(0, len(plan.actions_taken))
        self.assertEqual("State is empty.", str(plan.current_state))
        self.assertEqual(0, len(plan.search_modifiers))

    def test_2_forall(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.IPC_Tests_path + "test02_forall/domain.hddl")
        parser.parse_problem(self.IPC_Tests_path + "test02_forall/problem.hddl")
        solver = Solver(domain, problem)
        plan = solver.solve()
        solver.output(plan)
        self.assertEqual(1, 2)

    def test_3_forall1(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.IPC_Tests_path + "test03_forall1/domain.hddl")
        parser.parse_problem(self.IPC_Tests_path + "test03_forall1/problem.hddl")
        solver = Solver(domain, problem)
        plan = solver.solve()
        solver.output(plan)
        self.assertEqual(1, 2)

    def test_4_no_abstracts(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.IPC_Tests_path + "test04_no_abstracts/domain.hddl")
        parser.parse_problem(self.IPC_Tests_path + "test04_no_abstracts/problem.hddl")
        solver = Solver(domain, problem)
        plan = solver.solve()
        solver.output(plan)

        self.assertEqual(1, len(plan.actions_taken))
        self.assertEqual(1, len(plan.operations_taken))
        self.assertEqual(domain.actions['noop'], plan.actions_taken[0].action)
        self.assertEqual(domain.actions['noop'], plan.operations_taken[0].action)
        self.assertEqual("State is empty.", str(plan.current_state))
        self.assertEqual(0, len(plan.search_modifiers))
