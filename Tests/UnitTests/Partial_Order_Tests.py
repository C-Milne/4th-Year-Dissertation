import unittest
from Tests.UnitTests.TestTools.rover_execution import execution_prep
from Tests.UnitTests.TestTools.env_setup import env_setup


class PartialOrderTests(unittest.TestCase):

    def setUp(self) -> None:
        self.rover_path = "../Examples/Partial_Order/Rover/"

    def test_rover(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.rover_path + "domain.hddl")
        parser.parse_problem(self.rover_path + "pfile01.hddl")
        res = solver.solve()
        self.assertEqual(1, 2)
