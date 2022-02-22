import unittest
from runner import Runner
from Internal_Representation.precondition import Precondition
from Solver.model import Model
from Solver.solver import Solver
from Parsers.HDDL_Parser import HDDLParser
from Internal_Representation.method import Method
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem


class SolvingTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"
        self.test_tools_path = "TestTools/"
        self.blocksworld_path = "../Examples/Blocksworld/"

    def test_model_requirement_satisfier(self):
        domain = Domain(None)
        problem = Problem(domain)
        domain.add_problem(problem)

        # Test preconditions
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

        # Test preconditions
        parser = HDDLParser(domain, problem)
        parser.parse_domain(self.blocksworld_path + "domain.hddl")
        parser.parse_problem(self.blocksworld_path + "pb1.hddl")

        solver = Solver(domain, problem)
        model = Model(solver.problem, solver, solver._available_modifiers)
        action = domain.get_action("pickup") # b1
        solver._Solver__execute(model, action, {'?b': problem.get_object("b1")})
        self.assertEqual(1, 2)

        model = Model(solver.problem, solver, solver._available_modifiers)
        action = domain.get_action("mark_done") # b3
        solver._Solver__execute(model, action, {'?b': problem.get_object("b3")})
        self.assertEqual(1, 2)

        model = Model(solver.problem, solver, solver._available_modifiers)
        action = domain.get_action("stack")
        solver._Solver__execute(model, action, {'?b': problem.get_object("")})
        self.assertEqual(1, 2)

        model = Model(solver.problem, solver, solver._available_modifiers)
        action = domain.get_action("unstack")
        solver._Solver__execute(model, action, {'?b': problem.get_object("")})
        self.assertEqual(1, 2)
