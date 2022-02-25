import unittest
from runner import Runner
from Internal_Representation.precondition import Precondition
from Solver.model import Model
from Parsers.HDDL_Parser import HDDLParser
from Internal_Representation.method import Method
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Internal_Representation.modifier import Modifier
from Solver.solver import Solver


class HDDLGroundingTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"
        self.test_tools_path = "TestTools/"
        self.blocksworld_path = "../Examples/Blocksworld/"
        self.rover_path = "../Examples/IPC_Tests/Rover/"

    def test_blocksworld_pb1_initial_state(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.blocksworld_path + "domain.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        solver = Solver(domain, problem)
        model = Model(solver.problem, solver, solver._available_modifiers)

        # Check all values are correct before execution of action
        blocksworld_pb1_initial_state = ['hand-empty', ['clear', 'b3'],
                                              ['on-table', 'b2'], ['on', 'b3', 'b5'], ['on', 'b5', 'b4'],
                                              ['on', 'b4', 'b2'],
                                              ['clear', 'b1'], ['on-table', 'b1'], ['goal_clear', 'b2'],
                                              ['goal_on-table', 'b4'],
                                              ['goal_on', 'b2', 'b5'], ['goal_on', 'b5', 'b4'], ['goal_clear', 'b1'],
                                              ['goal_on-table', 'b3'], ['goal_on', 'b1', 'b3']]
        blocksworld_pb1_initial_state_index = {'hand-empty': [0], 'clear': [1, 6], 'goal_clear': [8, 12],
                                                    'goal_on': [10, 11, 14], 'goal_on-table': [9, 13],
                                                    'on': [3, 4, 5], 'on-table': [2, 7]}
        self.assertEqual(blocksworld_pb1_initial_state, model.current_state.elements)
        self.assertEqual(blocksworld_pb1_initial_state_index, model.current_state._index)

    def test_precondition_complex(self):
        # Devise a complex precondition and test it
        precon_list = ['and',
                       ['not',
                            ['and',['have','?y'],['have','?a']]
                        ],
                       ['and',
                            ['have', '?x'], ['or', ['have', '?b'], ['have', '?c']]
                        ],
                       ['or',
                            ['hate','?z'], ['hate', '?d']
                        ]
                       ]
        precons = Precondition(precon_list)
        # Set up model
        state_dict = {'have': ['ham', 'irn-bru', 'car'], 'hate': []}
        model = Model(state_dict)
        param_dict = {"?z": "ham", "?x": "irn-bru", "?y": "car", "?a": "bike", "?b": "popcorn", "?c": "crisps", "?d": "dark"}

        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

        state_dict = {'have': ['ham', 'irn-bru', 'car', 'popcorn'], 'hate': ['dark']}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

    def test_method_requirements(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld_test_domain_2.hddl")

        # Add some assertions for this - seems too work (perhaps not for 'forall' methods)
        self.assertEqual(1, 2)

    def test_forall_preconditions(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld_test_domain_1.hddl")
        parser.parse_problem(self.test_tools_path + "Blocksworld_test_problem_1.hddl")
        method = domain.methods['setdone']
        model = Model(problem, None, [])
        result = method.evaluate_preconditions(model, {})
        self.assertEqual(False, result)

        # Test for True
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Blocksworld_test_domain_1.hddl")
        parser.parse_problem(self.test_tools_path + "Blocksworld_test_problem_1_1.hddl")
        method = domain.methods['setdone']
        model = Model(problem, None, [])
        result = method.evaluate_preconditions(model, {})
        self.assertEqual(True, result)

    def test_complex_method_requirements(self):
        # Test a huge method requirements with and, or, not, and forall
        self.assertEqual(1, 2)

    def test_precondition_and(self):
        # Test the 'and' functionality for preconditions
        # Set up precondition object
        precon_list = ['and', ['have','?x'], ['have','?y'], ['have', '?z']]
        precons = Precondition(precon_list)
        # Set up model
        state_dict = {'have': ['ham', 'irn-bru', 'car']}
        model = Model(state_dict)
        param_dict = {"?z": "ham", "?x":"irn-bru", "?y": "car"}

        # Testing for True
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        # Testing for False
        state_dict = {'have': ['irn-bru', 'car']}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

    def test_precondition_or(self):
        # Test the 'or' functionality for preconditions
        # Set up precondition object
        precon_list = ['or', ['have', '?x'], ['have', '?y'], ['have', '?z']]
        precons = Precondition(precon_list)
        # Set up model
        state_dict = {'have': ['ham', 'irn-bru', 'car']}
        model = Model(state_dict)
        param_dict = {"?z": "ham", "?x": "irn-bru", "?y": "car"}

        # Testing for True
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        # Testing for True
        state_dict = {'have': ['irn-bru', 'car']}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        state_dict = {'have': ['irn-bru']}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

        state_dict = {'have': []}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

    def test_precondition_not(self):
        # Test the 'not' functionality for preconditions
        # Set up precondition object
        precon_list = ['not', ['have', '?x']]
        precons = Precondition(precon_list)
        # Set up model
        state_dict = {'have': ['ham', 'irn-bru', 'car']}
        model = Model(state_dict)
        param_dict = {"?z": "ham", "?x": "irn-bru", "?y": "car"}

        # Testing for False
        result = precons.evaluate(model, param_dict)
        self.assertEqual(False, result)

        # Testing for True
        state_dict = {'have': ['ham', 'car']}
        model = Model(state_dict)
        result = precons.evaluate(model, param_dict)
        self.assertEqual(True, result)

    def test_action_requirements(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.test_tools_path + "Rover/domain2.hddl")

        # Check action requirements
        self.assertEqual(1, 2)

    def test_task_method_grounding(self):
        # Check that methods corresponding to a task are being stored
        self.assertEqual(1, 2)

    def test_method_subtask_grounding(self):
        # Check that method subtasks hold reference to action/task not only string
        # rover domain
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.rover_path + "rover-domain.hddl")

        method_keys = list(domain.methods.keys())
        for m in method_keys:
            subtasks = domain.methods[m].subtasks
            if subtasks is not None:
                for t in subtasks.tasks:
                    print("Method: {}\tSubtask: {}".format(m, t.task))
                    self.assertIsInstance(t.task, Modifier)

