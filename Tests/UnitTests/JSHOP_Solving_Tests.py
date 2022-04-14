import unittest
from Internal_Representation.precondition import Precondition
from Tests.UnitTests.TestTools.rover_execution import execution_prep
from Tests.UnitTests.TestTools.env_setup import env_setup
from Internal_Representation.problem_predicate import ProblemPredicate
from Solver.action_tracker import ActionTracker


class JSHOPSolvingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.basic_path = "../Examples/JShop/basic/"
        self.block_path = "../Examples/JShop/blocks/"
        # self.block_path = "Tests/Examples/JShop/blocks/"
        self.forall_test_path = "../Examples/JShop/foralltest/"
        self.forall_path = "../Examples/JShop/forall/"
        self.rover_test_path = "TestTools/J-Rover/"

    @unittest.skip
    def test_derived_predicate_processing_1(self):
        """This test takes ages to process. For one of the derived predicates there is 84100 parameter options"""
        # Test 'same' axiom from blocks domain
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.block_path + "blocks")
        parser.parse_problem(self.block_path + "problem")
        execution_prep(problem, solver)

        model = solver.search_models._SearchQueue__Q.pop(0)

        solver.compute_derived_predicates(model)
        self.assertEqual(1, 2)

    def test_forall_1(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.forall_test_path + "forall")
        parser.parse_problem(self.forall_test_path + "problem")
        execution_prep(problem, solver)

        self.assertEqual(['forall', ['?v'], [['p', '?v']], [['q', '?v'], ['q', '?v'], ['not', ['w', '?v']]]],
                         domain.methods['method0'].preconditions.conditions)

        model = solver.search_models._SearchQueue__Q.pop(0)
        res = domain.methods['method0'].preconditions.evaluate({}, model, problem)

        # Test Running this example
        self.assertEqual(False, res)

    def test_forall_satisfier_selection(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.forall_test_path + "forall")
        parser.parse_problem(self.forall_test_path + "problem")
        execution_prep(problem, solver)

        model = solver.search_models._SearchQueue__Q.pop(0)

        method = domain.methods['method0']
        cons = method.preconditions.head
        satisfying_obs = cons._collect_objects({}, model, problem)
        self.assertEqual(1, len(satisfying_obs))
        self.assertEqual('y', satisfying_obs[0].name)
        self.assertEqual(problem.objects['y'], satisfying_obs[0])

    def test_forall_2(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.forall_path + "forall")
        parser.parse_problem(self.forall_path + "problem")
        execution_prep(problem, solver)
        solver.parameter_selector.presolving_processing(domain, problem)

        model = solver.search_models._SearchQueue__Q.pop(0)

        # Test applying forall effect method
        self.assertIn(ProblemPredicate(domain.predicates['in'], [problem.objects['p3'], problem.objects['t2']]),
                      model.current_state.elements)

        subT = model.search_modifiers.pop(0)
        solver._Solver__expand_task(subT, model)

        model = solver.search_models._SearchQueue__Q.pop(0)
        subT = model.search_modifiers.pop(0)
        solver._Solver__expand_method(subT, model)

        model = solver.search_models._SearchQueue__Q.pop(0)
        subT = model.search_modifiers.pop(0)
        solver._Solver__expand_task(subT, model)

        search_models = solver.search_models._SearchQueue__Q
        self.assertEqual(2, len(search_models))

        model = search_models[0]
        self.assertEqual(2, len(model.search_modifiers))
        mod = model.search_modifiers[0]
        self.assertEqual(domain.methods['method2'], mod.task)
        self.assertEqual({'?x': problem.objects['city2'], '?t': problem.objects['t2'], '?z': problem.objects['p1']}, mod.given_params)

        mod = model.search_modifiers[1]
        self.assertEqual(domain.actions['!drive'], mod.task)
        self.assertEqual({'?x': problem.objects['city2'], '?y': problem.objects['city1'], '?t': problem.objects['t2']},
                         mod.given_params)

        model = search_models[1]
        self.assertEqual(2, len(model.search_modifiers))
        mod = model.search_modifiers[0]
        self.assertEqual(domain.methods['method2'], mod.task)
        self.assertEqual({'?x': problem.objects['city2'], '?t': problem.objects['t2'], '?z': problem.objects['p4']},
                         mod.given_params)

        mod = model.search_modifiers[1]
        self.assertEqual(domain.actions['!drive'], mod.task)
        self.assertEqual({'?x': problem.objects['city2'], '?y': problem.objects['city1'], '?t': problem.objects['t2']},
                         mod.given_params)

    def test_forall_example_execution(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.forall_path + "forall")
        parser.parse_problem(self.forall_path + "problem")
        res = solver.solve()

        self.assertNotEqual(None, res)
        self.assertIn(ActionTracker(domain.actions['!load'], {'?z': problem.objects['p1'], '?t': problem.objects['t2']}),
                      res.actions_taken)
        self.assertIn(
            ActionTracker(domain.actions['!load'], {'?z': problem.objects['p4'], '?t': problem.objects['t2']}),
            res.actions_taken)
        self.assertIn(
            ActionTracker(domain.actions['!drive'], {'?t': problem.objects['t2'], '?x': problem.objects['city2'],
                                                     '?y': problem.objects['city1']}), res.actions_taken)
        self.assertIn(ProblemPredicate(domain.predicates['at'], [problem.objects['p1'], problem.objects['city1']]),
                      res.current_state.elements)
        self.assertIn(ProblemPredicate(domain.predicates['at'], [problem.objects['p3'], problem.objects['city1']]),
                      res.current_state.elements)
        self.assertIn(ProblemPredicate(domain.predicates['at'], [problem.objects['p4'], problem.objects['city1']]),
                      res.current_state.elements)
        self.assertIn(ProblemPredicate(domain.predicates['at'], [problem.objects['p2'], problem.objects['city1']]),
                      res.current_state.elements)

    @unittest.skip
    def test_forall_example_execution_2(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.forall_test_path + "forall")
        parser.parse_problem(self.forall_test_path + "problem")
        res = solver.solve()

        self.assertEqual(1, 2)

    def test_basic_execution(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.basic_path + "basic")
        parser.parse_problem(self.basic_path + "problem")
        res = solver.solve()

        self.assertNotEqual(None, res)
        self.assertIn(ActionTracker(domain.actions['!drop'], {'?a': problem.objects['kiwi']}), res.actions_taken)
        self.assertIn(ActionTracker(domain.actions['!pickup'], {'?a': problem.objects['banjo']}), res.actions_taken)

    def test_rover_execution_part_guided(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.rover_test_path + "rover")
        parser.parse_problem(self.rover_test_path + "problem")

        execution_prep(problem, solver)
        solver.parameter_selector.presolving_processing(domain, problem)
        # res = solver.solve()

        solver._Solver__search(True)
        solver._Solver__search(True)
        solver._Solver__search(True)
        solver.search_models._SearchQueue__Q = [solver.search_models._SearchQueue__Q[0]]
        solver.search_models._SearchQueue__Q[0].search_modifiers[0].given_params['?to'] = problem.objects['waypoint5']
        search_models = solver.search_models._SearchQueue__Q
        solver._Solver__search(True)
        solver._Solver__search(True)
        solver._Solver__search(True)
        res = solver._Solver__search()
        # solver._Solver__search(True)
        # solver._Solver__search(True)
        search_models = solver.search_models._SearchQueue__Q
        self.assertNotEqual(None, res)
        solver.output(res)

    def test_rover_execution(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.rover_test_path + "rover")
        parser.parse_problem(self.rover_test_path + "problem")

        execution_prep(problem, solver)
        solver.parameter_selector.presolving_processing(domain, problem)
        res = solver.solve()
        search_models = solver.search_models._SearchQueue__Q
        self.assertNotEqual(None, res)
        solver.output(res)

    @unittest.skip
    def test_evaluating_goal_precondition(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.block_path + "blocks")
        parser.parse_problem(self.block_path + "problem")
        self.assertEqual(1, 2)
