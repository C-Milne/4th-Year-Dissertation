import unittest
from Tests.UnitTests.TestTools.rover_execution import execution_prep
from Tests.UnitTests.TestTools.env_setup import env_setup


class JSHOPSolvingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.basic_path = "../Examples/JShop/basic/"
        self.block_path = "../Examples/JShop/blocks/"
        # self.block_path = "Tests/Examples/JShop/blocks/"

    @unittest.skip
    def test_derived_predicate_processing_1(self):
        # Test 'same' axiom from blocks domain
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.block_path + "blocks")
        parser.parse_problem(self.block_path + "problem")
        execution_prep(problem, solver)

        model = solver.search_models._SearchQueue__Q.pop(0)

        solver.compute_derived_predicates(model)
        self.assertEqual(1, 2)
