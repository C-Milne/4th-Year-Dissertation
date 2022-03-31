import unittest
from Tests.UnitTests.TestTools.rover_execution import execution_prep
from Tests.UnitTests.TestTools.env_setup import env_setup
from Solver.Heuristics.delete_relaxed import DeleteRelaxed


class HeuristicTests(unittest.TestCase):
    def setUp(self) -> None:
        self.transport_path = "../Examples/IPC_Tests/transport01/"
        self.rover_path = "../Examples/Rover/"

    def test_delete_relaxed_preprocessing(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.transport_path + "domain.hddl")
        parser.parse_problem(self.transport_path + "pfile01.hddl")
        solver.set_heuristic(DeleteRelaxed)
        solver.search_models.heuristic.presolving_processing()
        heu = solver.search_models.heuristic
        self.assertEqual(8, len(heu.tree.nodes))

        node = heu.tree.nodes['deliver']
        self.assertEqual(8, node.distance)

        node = heu.tree.nodes['get_to']
        self.assertEqual(3, node.distance)

        node = heu.tree.nodes['unload']
        self.assertEqual(2, node.distance)

        node = heu.tree.nodes['load']
        self.assertEqual(2, node.distance)

    def test_delete_relaxed_execution(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.rover_path + "domain.hddl")
        parser.parse_problem(self.rover_path + "p03.hddl")
        solver.set_heuristic(DeleteRelaxed)
        res = solver.solve()
        self.assertNotEqual(None, res)
