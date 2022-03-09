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
        self.assertIsNotNone(plan)
        self.assertEqual(1, len(plan.actions_taken))

    def test_3_forall1(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.IPC_Tests_path + "test03_forall1/domain.hddl")
        parser.parse_problem(self.IPC_Tests_path + "test03_forall1/problem.hddl")
        solver = Solver(domain, problem)
        plan = solver.solve()
        solver.output(plan)
        self.assertEqual(1, len(plan.actions_taken))
        self.assertEqual(1, len(plan.actions_taken[0].parameters_used))
        self.assertEqual(problem.objects['f'], plan.actions_taken[0].parameters_used['?b'])

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

    def test_5_constants_in_domain(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.IPC_Tests_path + "test05_constants_in_domain/domain.hddl")
        parser.parse_problem(self.IPC_Tests_path + "test05_constants_in_domain/problem.hddl")
        solver = Solver(domain, problem)
        plan = solver.solve()
        solver.output(plan)
        self.assertEqual(1, len(plan.actions_taken))
        self.assertEqual(domain.actions['noop'], plan.actions_taken[0].action)
        self.assertEqual(1, len(plan.actions_taken[0].parameters_used))
        self.assertEqual(problem.objects['a'], plan.actions_taken[0].parameters_used['?a'])

    def test_6_synonymes(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.IPC_Tests_path + "test06_synonymes/domain.hddl")
        parser.parse_problem(self.IPC_Tests_path + "test06_synonymes/problem.hddl")
        solver = Solver(domain, problem)
        plan = solver.solve()
        solver.output(plan)
        self.assertEqual(8, len(plan.actions_taken))
        for i in range(4):
            self.assertEqual(domain.actions['noop1'], plan.actions_taken[i * 2].action)
            self.assertEqual(domain.actions['noop2'], plan.actions_taken[(i * 2) + 1].action)

    def test_7_arguments(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.IPC_Tests_path + "test07_arguments/domain.hddl")
        parser.parse_problem(self.IPC_Tests_path + "test07_arguments/problem.hddl")
        solver = Solver(domain, problem)

        self.assertEqual(2, len(domain.actions['noop'].parameters))
        for p in domain.actions['noop'].parameters:
            self.assertEqual(domain.types['a'], p.type)

        plan = solver.solve()
        solver.output(plan)
        self.assertEqual(1, len(plan.actions_taken))
        self.assertEqual(domain.actions['noop'], plan.actions_taken[0].action)
        self.assertEqual(2, len(plan.actions_taken[0].parameters_used))
        self.assertEqual(problem.objects['b'], plan.actions_taken[0].parameters_used[0])
        self.assertEqual(problem.objects['b'], plan.actions_taken[0].parameters_used[1])

    @unittest.skip
    def test_satellite01(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.IPC_Tests_path + "satellite01/domain2.hddl")
        parser.parse_problem(self.IPC_Tests_path + "satellite01/1obs-1sat-1mod.hddl")
        solver = Solver(domain, problem)
        plan = solver.solve()
        solver.output(plan)
        self.assertEqual(1, 2)

    @unittest.skip
    def test_transport01(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.IPC_Tests_path + "transport01/domain.hddl")
        parser.parse_problem(self.IPC_Tests_path + "transport01/pfile01.hddl")
        solver = Solver(domain, problem)

        # I think this one is not solvable
        # plan = solver.solve()
        # solver.output(plan)
        self.assertEqual(1, 2)

    @unittest.skip
    def test_um_translog01(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.IPC_Tests_path + "um-translog01/domain.hddl")
        parser.parse_problem(self.IPC_Tests_path + "um-translog01/problem.hddl")
        solver = Solver(domain, problem)
        plan = solver.solve()
        solver.output(plan)
        self.assertEqual(1, 2)
