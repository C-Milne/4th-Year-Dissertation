import unittest
from Tests.UnitTests.TestTools.env_setup import env_setup
from Parsers.JSHOP_Parser import JSHOPParser


class JSHOPParsingTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_path = "../Examples/JShop/basic/"

    def test_parsing_basic_domain(self):
        domain, problem, parser, solver = env_setup(False)
        parser.parse_domain(self.basic_path + "basic")

        self.assertEqual(1, 2)
