import unittest
from Tests.UnitTests.TestTools.rover_execution import execution_prep
from Tests.UnitTests.TestTools.env_setup import env_setup
from Internal_Representation.problem_predicate import ProblemPredicate


class JSHOPSolvingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.basic_path = "../Examples/JShop/basic/"
        self.block_path = "../Examples/JShop/blocks/"
        # self.block_path = "Tests/Examples/JShop/blocks/"
        self.freecell_path = "../Examples/JShop/freecell/"
        self.forall_test_path = "../Examples/JShop/foralltest/"
        self.forall_path = "../Examples/JShop/forall/"

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

    @unittest.skip
    def test_derived_predicate_processing_2(self):
        # Test 'same' axiom from blocks domain
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.freecell_path + "freecell")
        parser.parse_problem(self.freecell_path + "problem")
        execution_prep(problem, solver)

        model = solver.search_models._SearchQueue__Q.pop(0)

        solver.compute_derived_predicates(model)
        self.assertEqual(1, 2)

    def test_forall_1(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.forall_test_path + "forall")
        parser.parse_problem(self.forall_test_path + "problem")
        execution_prep(problem, solver)

        self.assertEqual(['and', ['forall', ['?v'], [['p', '?v']], [['q', '?v'], ['q', '?v'], ['not', ['w', '?v']]]]],
                         domain.methods['method0'].preconditions.conditions)

        model = solver.search_models._SearchQueue__Q.pop(0)
        res = domain.methods['method0'].preconditions.evaluate(model, {})

        # Test Running this example
        self.assertEqual(1, 2)

    def test_forall_2(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.forall_path + "forall")
        parser.parse_problem(self.forall_path + "problem")
        execution_prep(problem, solver)

        model = solver.search_models._SearchQueue__Q.pop(0)

        # Test applying forall effect method
        self.assertIn(ProblemPredicate(domain.predicates['in'], [problem.objects['p3'], problem.objects['t2']]),
                      model.current_state.elements)

        subT = model.search_modifiers.pop(0)
        solver._Solver__expand_task(subT, model)

        model = solver.search_models._SearchQueue__Q.pop(0)
        subT = model.search_modifiers.pop(0)
        solver._Solver__expand_method(subT, model)

        search_models = solver.search_models._SearchQueue__Q
        self.assertEqual(1, 2)

    @unittest.skip
    def test_runtime_lists(self):
        # Test popping from a list at run time
        pass
