import unittest
from Tests.UnitTests.TestTools.env_setup import env_setup
from Parsers.JSHOP_Parser import JSHOPParser


class JSHOPParsingTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_path = "../Examples/JShop/basic/"

    def test_parsing_basic_domain(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.basic_path + "basic")

        self.assertEqual(1, len(domain.predicates))
        self.assertIn('have', domain.predicates)
        self.assertEqual(1, len(domain.predicates['have'].parameters))

        self.assertEqual(2, len(domain.actions))
        self.assertIn('!pickup', domain.actions)
        self.assertIn('!drop', domain.actions)

        self.assertEqual(1, len(domain.actions['!pickup'].parameters))
        self.assertEqual('?a', domain.actions['!pickup'].parameters[0].name)
        self.assertEqual(None, domain.actions['!pickup'].parameters[0].type)
        self.assertEqual([], domain.actions['!pickup'].preconditions.conditions)
        self.assertEqual(1, len(domain.actions['!pickup'].effects.effects))
        self.assertEqual(False, domain.actions['!pickup'].effects.effects[0].negated)
        self.assertEqual(['?a'], domain.actions['!pickup'].effects.effects[0].parameters)
        self.assertEqual(domain.predicates['have'], domain.actions['!pickup'].effects.effects[0].predicate)

        self.assertEqual(1, len(domain.actions['!drop'].parameters))
        self.assertEqual('?a', domain.actions['!drop'].parameters[0].name)
        self.assertEqual(None, domain.actions['!drop'].parameters[0].type)
        self.assertEqual(['and', ['have', '?a']], domain.actions['!drop'].preconditions.conditions)
        self.assertEqual(1, len(domain.actions['!drop'].effects.effects))
        self.assertEqual(True, domain.actions['!drop'].effects.effects[0].negated)
        self.assertEqual(['?a'], domain.actions['!drop'].effects.effects[0].parameters)
        self.assertEqual(domain.predicates['have'], domain.actions['!drop'].effects.effects[0].predicate)

        self.assertEqual(1, len(domain.tasks))
        self.assertIn('swap', domain.tasks)
        self.assertEqual(2, len(domain.tasks['swap'].methods))
        self.assertIn(domain.methods['method0'], domain.tasks['swap'].methods)
        self.assertIn(domain.methods['method1'], domain.tasks['swap'].methods)
        self.assertEqual(2, len(domain.tasks['swap'].parameters))
        self.assertEqual('?x', domain.tasks['swap'].parameters[0].name)
        self.assertEqual(None, domain.tasks['swap'].parameters[0].type)
        self.assertEqual('?y', domain.tasks['swap'].parameters[1].name)
        self.assertEqual(None, domain.tasks['swap'].parameters[1].type)

        self.assertEqual(2, len(domain.methods))
        self.assertIn('method0', domain.methods)
        self.assertEqual(['and', ['have', '?x'], ['not', ['have', '?y']]], domain.methods['method0'].preconditions.conditions)
        self.assertIn('method1', domain.methods)
        self.assertEqual(['and', ['have', '?y'], ['not', ['have', '?x']]], domain.methods['method1'].preconditions.conditions)
