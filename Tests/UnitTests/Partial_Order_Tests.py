import unittest
from Tests.UnitTests.TestTools.rover_execution import execution_prep
from Tests.UnitTests.TestTools.env_setup import env_setup


class PartialOrderTests(unittest.TestCase):

    def setUp(self) -> None:
        self.rover_path = "../Examples/Partial_Order/Rover/"
        self.satelite_path = "../Examples/IPC_Tests/satellite01/"

    def test_rover(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.rover_path + "domain.hddl")
        parser.parse_problem(self.rover_path + "pfile01.hddl")
        res = solver.solve()
        self.assertEqual(1, 2)

    def test_ordering_total_ordered_problem(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.satelite_path + "domain2.hddl")
        method = domain.methods['method0']
        self.assertEqual(1, len(method.subtasks.task_orderings))
        self.assertEqual(3, len(method.subtasks.task_orderings[0]))
        self.assertEqual(domain.tasks['activate_instrument'], method.subtasks.task_orderings[0][0].task)
        self.assertEqual(domain.get_modifier('turn_to'), method.subtasks.task_orderings[0][1].task)
        self.assertEqual(domain.get_modifier('take_image'), method.subtasks.task_orderings[0][2].task)

    def test_ordering_creation(self):
        # Test ordering creation function with partial orderings that yield multiple orderings
        self.assertEqual(1, 2)
