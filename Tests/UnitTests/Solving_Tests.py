import unittest
from runner import Runner
from Internal_Representation.precondition import Precondition
from Solver.model import Model
from Solver.solver import Solver
from Parsers.HDDL_Parser import HDDLParser
from Internal_Representation.method import Method
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
import Tests.UnitTests.TestTools.rover_execution as RovEx


class SolvingTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"
        self.test_tools_path = "TestTools/"
        self.blocksworld_path = "../Examples/Blocksworld/"
        self.rover_path = "../Examples/IPC_Tests/Rover/"

    def test_model_requirement_satisfier(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld_test_domain_3.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        model = Model(problem, None, [domain.methods["unstack-block"]])
        self.assertEqual(1, len(model.ready_modifiers))
        self.assertEqual({'unstack-block':[{'?b': problem.objects['b3']}]}, model.ready_modifiers)

    def test_model_requirement_satisfier_2(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld_test_domain_4.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        model = Model(problem, None, [domain.methods["pickup-ready-block"]])
        self.assertEqual(0, len(model.ready_modifiers))

    def test_action_execution(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.blocksworld_path + "domain.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        solver = Solver(domain, problem)
        model = Model(solver.problem, solver, solver._available_modifiers)
        action = domain.get_action("pickup") # b1

        solver._Solver__execute(model, action, {'?b': problem.get_object("b1")})

        # Check model.current_state.elements
        self.assertEqual([['clear', 'b3'],['on-table', 'b2'], ['on', 'b3', 'b5'],
        ['on', 'b5', 'b4'], ['on', 'b4', 'b2'],
        ['goal_clear', 'b2'], ['goal_on-table', 'b4'],['goal_on', 'b2', 'b5'],
        ['goal_on', 'b5', 'b4'], ['goal_clear', 'b1'],['goal_on-table', 'b3'],
        ['goal_on', 'b1', 'b3'], ['holding', 'b1']], model.current_state.elements)

        # Check model.current_state._index
        self.assertEqual({'clear': [0],'goal_clear': [5, 9],
        'goal_on': [7, 8, 11],'goal_on-table': [6, 10],'on': [2, 3, 4],
        'on-table': [1],'holding':[12]}, model.current_state._index)

    def test_action_execution_2(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.blocksworld_path + "domain.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        solver = Solver(domain, problem)
        model = Model(solver.problem, solver, solver._available_modifiers)
        action = domain.get_action("mark_done") # b3
        solver._Solver__execute(model, action, {'?b': problem.get_object("b3")})

        # Check elements list
        expected_elements = ['hand-empty', ['clear', 'b3'],
                          ['on-table', 'b2'], ['on', 'b3', 'b5'], ['on', 'b5', 'b4'],['on', 'b4', 'b2'],
                          ['clear', 'b1'], ['on-table', 'b1'], ['goal_clear', 'b2'],['goal_on-table', 'b4'],
                          ['goal_on', 'b2', 'b5'], ['goal_on', 'b5', 'b4'], ['goal_clear', 'b1'],
                          ['goal_on-table', 'b3'], ['goal_on', 'b1', 'b3'], ['done', 'b3']]
        self.assertEqual(expected_elements, model.current_state.elements)

        expected_index = {'hand-empty': [0], 'clear': [1, 6], 'goal_clear': [8, 12],
                            'goal_on': [10, 11, 14], 'goal_on-table': [9, 13],
                            'on': [3, 4, 5], 'on-table': [2, 7], 'done': [15]}
        # Check _index dictionary
        self.assertEqual(expected_index, model.current_state._index)

    def test_action_execution_3(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.blocksworld_path + "domain.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        solver = Solver(domain, problem)
        model = Model(solver.problem, solver, solver._available_modifiers)

        action = domain.get_action("pickup")  # b1
        solver._Solver__execute(model, action, {'?b': problem.get_object("b1")})

        action = domain.get_action("stack")
        solver._Solver__execute(model, action, {'?top': problem.get_object("b1"),
                                                '?bottom': problem.get_object("b3")})

        # Check elements list
        expected_elements = [['on-table', 'b2'], ['on', 'b3', 'b5'],
        ['on', 'b5', 'b4'], ['on', 'b4', 'b2'],
        ['goal_clear', 'b2'], ['goal_on-table', 'b4'],['goal_on', 'b2', 'b5'],
        ['goal_on', 'b5', 'b4'], ['goal_clear', 'b1'],['goal_on-table', 'b3'],
        ['goal_on', 'b1', 'b3'], 'hand-empty', ['on', 'b1', 'b3'], ['clear', 'b1']]
        self.assertEqual(expected_elements, model.current_state.elements)

        expected_index = {'goal_clear': [4, 8],
        'goal_on': [6, 7, 10],'goal_on-table': [5, 9],'on': [1, 2, 3, 12],
        'on-table': [0], 'hand-empty':[11], 'clear':[13]}
        # Check _index dictionary
        self.assertEqual(expected_index, model.current_state._index)

    def test_action_execution_4(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.blocksworld_path + "domain.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        solver = Solver(domain, problem)
        model = Model(solver.problem, solver, solver._available_modifiers)
        action = domain.get_action("unstack")
        solver._Solver__execute(model, action, {'?top': problem.get_object("b3"),
                                                '?bottom' : problem.get_object("b5")})

        # Check elements list
        expected_elements = [['on-table', 'b2'], ['on', 'b5', 'b4'], ['on', 'b4', 'b2'],
                             ['clear', 'b1'], ['on-table', 'b1'], ['goal_clear', 'b2'],
                             ['goal_on-table', 'b4'],['goal_on', 'b2', 'b5'],
                             ['goal_on', 'b5', 'b4'], ['goal_clear', 'b1'],
                             ['goal_on-table', 'b3'], ['goal_on', 'b1', 'b3'],
                             ['holding', 'b3'], ['clear', 'b5']]
        self.assertEqual(expected_elements, model.current_state.elements)

        expected_index = {'clear': [3, 13], 'goal_clear': [5, 9],
                          'goal_on': [7, 8, 11], 'goal_on-table': [6, 10],
                          'on': [1, 2], 'on-table': [0, 4], 'holding': [12]}
        # Check _index dictionary
        self.assertEqual(expected_index, model.current_state._index)

    def test_basic_execution(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.basic_domain_path)
        parser.parse_problem(self.basic_pb1_path)

        task = problem.subtasks.get_tasks()[0]
        self.assertEqual(domain.tasks['swap'], task.task)
        self.assertEqual([problem.objects['banjo'], problem.objects['kiwi']], task.parameters)

        # Initialise solver
        solver = Solver(domain, problem)

        # Create initial model
        solver.search_models.clear()
        param_dict = solver._Solver__generate_param_dict(task.task, task.parameters)
        initial_model = Model(problem.initial_state, [task.task], param_dict, problem)
        solver.search_models.add(initial_model)

        # Execute Step 1
        solver._Solver__search(True)

        # Expect task to be expanded
        self.assertEqual(1, len(solver.search_models._SearchQueue__Q))
        self.assertEqual(1, len(solver.search_models._SearchQueue__Q[0].search_modifiers))
        self.assertEqual(domain.methods['have_second'], solver.search_models._SearchQueue__Q[0].search_modifiers[0])
        self.assertEqual(domain.predicates['have'],
                         solver.search_models._SearchQueue__Q[0].current_state.elements[0].predicate)
        self.assertEqual(1, len(solver.search_models._SearchQueue__Q[0].current_state.elements[0].objects))
        self.assertEqual(problem.objects['kiwi'], solver.search_models._SearchQueue__Q[0].current_state.elements[0].objects[0])
        self.assertEqual(None, solver.search_models._SearchQueue__Q[0].current_state.elements[0].objects[0].type)

        # Execute step 2
        solver._Solver__search(True)

        # Expect method to be expanded - should be tasks drop and pickup in the place of the method
        self.assertEqual(1, len(solver.search_models._SearchQueue__Q))
        self.assertEqual(2, len(solver.search_models._SearchQueue__Q[0].search_modifiers))

        self.assertEqual(domain.actions['drop'], solver.search_models._SearchQueue__Q[0].search_modifiers[0].task)
        self.assertEqual(domain.actions['pickup'], solver.search_models._SearchQueue__Q[0].search_modifiers[1].task)

        self.assertEqual(domain.predicates['have'],
                         solver.search_models._SearchQueue__Q[0].current_state.elements[0].predicate)
        self.assertEqual(1, len(solver.search_models._SearchQueue__Q[0].current_state.elements[0].objects))
        self.assertEqual(problem.objects['kiwi'], solver.search_models._SearchQueue__Q[0].current_state.elements[0].
                         objects[0])
        self.assertEqual(None, solver.search_models._SearchQueue__Q[0].current_state.elements[0].objects[0].type)

        # Execute step 3
        solver._Solver__search(True)

        # Expect the drop action to be carried out
        self.assertEqual(1, len(solver.search_models._SearchQueue__Q))
        model = solver.search_models._SearchQueue__Q[0]
        self.assertEqual(1, len(model.search_modifiers))
        self.assertEqual(domain.actions['pickup'], model.search_modifiers[0].task)
        self.assertEqual([], model.current_state.elements)

        # Execute step 4
        solver._Solver__search(True)

        # Expect the pickup action to be carried out
        self.assertEqual(0, len(solver.search_models._SearchQueue__Q))
        self.assertEqual(1, len(solver.search_models._SearchQueue__completed_models))
        model = solver.search_models._SearchQueue__completed_models[0]
        self.assertEqual(0, len(model.search_modifiers))
        self.assertEqual(1, len(model.current_state.elements))
        self.assertEqual(domain.predicates['have'], model.current_state.elements[0].predicate)
        self.assertEqual(1, len(model.current_state.elements[0].objects))
        self.assertEqual(problem.objects['banjo'], model.current_state.elements[0].objects[0])

    def test_compare_parameters(self):
        domain, problem, solver = RovEx.setup()
        model = solver.search_models._SearchQueue__Q[0]

        response = solver._Solver__compare_parameters(domain.methods['m_get_image_data_ordering_0'], model.given_params)
        self.assertEqual(list, type(response))
        self.assertEqual(2, len(response))
        self.assertEqual(bool, type(response[0]))
        self.assertEqual(list, type(response[1]))
        self.assertEqual(False, response[0])
        self.assertEqual(["?camera", "?rover", "?waypoint"], response[1])

    def test_finding_parameters(self):
        domain, problem, solver = RovEx.setup()
        model = solver.search_models.pop()
        method = domain.methods['m_get_image_data_ordering_0']
        found_params = solver._Solver__find_satisfying_parameters(model, method, model.given_params)
        self.assertEqual(4, len(found_params))
        for combo in found_params:
            self.assertEqual(problem.objects['objective1'], combo['?objective'])
            self.assertEqual(problem.objects['high_res'], combo['?mode'])
            self.assertEqual(problem.objects['camera0'], combo['?camera'])
            self.assertEqual(problem.objects['rover0'], combo['?rover'])
        self.assertEqual(problem.objects['waypoint0'], found_params[0]['?waypoint'])
        self.assertEqual(problem.objects['waypoint1'], found_params[1]['?waypoint'])
        self.assertEqual(problem.objects['waypoint2'], found_params[2]['?waypoint'])
        self.assertEqual(problem.objects['waypoint3'], found_params[3]['?waypoint'])

    def test_rover_execution_beginning(self):
        domain, problem, solver = RovEx.setup()
        self.assertEqual(1, len(solver.search_models._SearchQueue__Q))
        model = solver.search_models._SearchQueue__Q[0]
        self.assertEqual(1, len(model.search_modifiers))
        self.assertEqual(domain.tasks['get_image_data'], model.search_modifiers[0])
        self.assertEqual(2, len(model.given_params))
        self.assertEqual(problem.objects['objective1'], model.given_params['?objective'])
        self.assertEqual(problem.objects['high_res'], model.given_params['?mode'])

    def test_rover_execution_1(self):
        domain, problem, solver = RovEx.setup()
        solver._Solver__search(True)
        # Check searchModels has 4 search nodes each with a different ?waypoint parameter
        self.assertEqual(4, len(solver.search_models._SearchQueue__Q))
        for i in range(4):
            model = solver.search_models._SearchQueue__Q[i]
            self.assertEqual(1, len(model.search_modifiers))
            self.assertEqual(domain.methods['m_get_image_data_ordering_0'], model.search_modifiers[0])
            self.assertEqual(problem.objects["waypoint" + str(i)], model.given_params['?waypoint'])
