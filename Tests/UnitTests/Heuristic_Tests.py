import unittest
from Tests.UnitTests.TestTools.rover_execution import execution_prep
from Tests.UnitTests.TestTools.env_setup import env_setup
from Solver.Heuristics.delete_relaxed import DeleteRelaxed


class HeuristicTests(unittest.TestCase):
    def setUp(self) -> None:
        self.transport_path = "../Examples/IPC_Tests/transport01/"

    def test_delete_relaxed_preprocessing(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.transport_path + "domain.hddl")
        parser.parse_problem(self.transport_path + "pfile01.hddl")
        solver.set_heuristic(DeleteRelaxed)
        solver.search_models.heuristic.presolving_processing()
        heu = solver.search_models.heuristic
        self.assertEqual(15, len(heu.tree.nodes))
        self.assertEqual(1, len(heu.tree.root.children))
