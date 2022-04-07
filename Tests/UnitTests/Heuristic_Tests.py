import unittest
from Tests.UnitTests.TestTools.rover_execution import execution_prep
from Tests.UnitTests.TestTools.env_setup import env_setup
from Solver.Heuristics.tree_distance import TreeDistance
from Solver.Heuristics.delete_relaxed import DeleteRelaxed
from Internal_Representation.conditions import PredicateCondition


class HeuristicTests(unittest.TestCase):
    def setUp(self) -> None:
        self.transport_path = "../Examples/IPC_Tests/transport01/"
        self.rover_path = "../Examples/Rover/"
        self.basic_path = "../Examples/Basic/"

    def test_tree_distance_preprocessing(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.transport_path + "domain.hddl")
        parser.parse_problem(self.transport_path + "pfile01.hddl")
        solver.set_heuristic(TreeDistance)
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

    def test_tree_distance_execution(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.rover_path + "domain.hddl")
        parser.parse_problem(self.rover_path + "p03.hddl")
        solver.set_heuristic(TreeDistance)
        res = solver.solve()
        self.assertNotEqual(None, res)

    def test_delete_relaxed_preprocessing_basic_alt_domain(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.basic_path + "basic.hddl")
        parser.parse_problem(self.basic_path + "pb1.hddl")
        solver.set_heuristic(DeleteRelaxed)
        solver.search_models.heuristic.presolving_processing()
        heu = solver.search_models.heuristic
        alt_domain = heu.alt_domain

        # Check actions
        self.assertIn("pickup-banjo", alt_domain.actions)
        self.assertIn("pickup-kiwi", alt_domain.actions)
        self.assertIn("drop-banjo", alt_domain.actions)
        self.assertIn("drop-kiwi", alt_domain.actions)
        self.assertEqual(4, len(alt_domain.actions))

        self.assertEqual(domain.actions['pickup'].preconditions, alt_domain.actions['pickup-banjo'].preconditions)
        self.assertEqual(domain.actions['pickup'].preconditions, alt_domain.actions['pickup-kiwi'].preconditions)

        self.assertEqual(domain.actions['pickup'].parameters, alt_domain.actions['pickup-banjo'].parameters)
        self.assertEqual(domain.actions['pickup'].parameters, alt_domain.actions['pickup-kiwi'].parameters)

        self.assertEqual(domain.actions['drop'].preconditions, alt_domain.actions['drop-banjo'].preconditions)
        self.assertEqual(domain.actions['drop'].preconditions, alt_domain.actions['drop-kiwi'].preconditions)

        self.assertEqual(domain.actions['drop'].parameters, alt_domain.actions['drop-banjo'].parameters)
        self.assertEqual(domain.actions['drop'].parameters, alt_domain.actions['drop-kiwi'].parameters)

        # Check methods
        self.assertIn("have_first-banjo-banjo", alt_domain.methods)
        self.assertIn("have_first-banjo-kiwi", alt_domain.methods)
        self.assertIn("have_first-kiwi-banjo", alt_domain.methods)
        self.assertIn("have_first-kiwi-kiwi", alt_domain.methods)
        self.assertIn("have_second-banjo-banjo", alt_domain.methods)
        self.assertIn("have_second-banjo-kiwi", alt_domain.methods)
        self.assertIn("have_second-kiwi-banjo", alt_domain.methods)
        self.assertIn("have_second-kiwi-kiwi", alt_domain.methods)
        self.assertEqual(8, len(alt_domain.methods))

        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['pickup-banjo']),
                      alt_domain.methods["have_first-banjo-banjo"].preconditions.head.children)
        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['drop-banjo']),
                      alt_domain.methods["have_first-banjo-banjo"].preconditions.head.children)

        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['drop-banjo']),
                      alt_domain.methods["have_first-banjo-kiwi"].preconditions.head.children)
        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['pickup-kiwi']),
                      alt_domain.methods["have_first-banjo-kiwi"].preconditions.head.children)

        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['drop-kiwi']),
                      alt_domain.methods["have_first-kiwi-banjo"].preconditions.head.children)
        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['pickup-banjo']),
                      alt_domain.methods["have_first-kiwi-banjo"].preconditions.head.children)

        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['drop-kiwi']),
                      alt_domain.methods["have_first-kiwi-kiwi"].preconditions.head.children)
        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['pickup-kiwi']),
                      alt_domain.methods["have_first-kiwi-kiwi"].preconditions.head.children)

        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['drop-banjo']),
                      alt_domain.methods["have_second-banjo-banjo"].preconditions.head.children)
        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['pickup-banjo']),
                      alt_domain.methods["have_second-banjo-banjo"].preconditions.head.children)

        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['drop-kiwi']),
                      alt_domain.methods["have_second-banjo-kiwi"].preconditions.head.children)
        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['pickup-banjo']),
                      alt_domain.methods["have_second-banjo-kiwi"].preconditions.head.children)

        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['drop-banjo']),
                      alt_domain.methods["have_second-kiwi-banjo"].preconditions.head.children)
        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['pickup-kiwi']),
                      alt_domain.methods["have_second-kiwi-banjo"].preconditions.head.children)

        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['drop-kiwi']),
                      alt_domain.methods["have_second-kiwi-kiwi"].preconditions.head.children)
        self.assertIn(PredicateCondition(alt_domain.predicates["U"], ['pickup-kiwi']),
                      alt_domain.methods["have_second-kiwi-kiwi"].preconditions.head.children)

    def test_delete_relaxed_preprocessing_basic_alt_problem(self):
        domain, problem, parser, solver = env_setup(True)
        parser.parse_domain(self.basic_path + "basic.hddl")
        parser.parse_problem(self.basic_path + "pb1.hddl")
        solver.set_heuristic(DeleteRelaxed)
        solver.search_models.heuristic.presolving_processing()
        heu = solver.search_models.heuristic
        alt_problem = heu.alt_problem
        self.assertEqual(1, 2)
