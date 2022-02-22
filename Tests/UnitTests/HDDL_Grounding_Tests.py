import unittest
from runner import Runner
from Internal_Representation.precondition import Precondition
from Solver.model import Model
from Parsers.HDDL_Parser import HDDLParser
from Internal_Representation.method import Method
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem


class HDDLGroundingTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_domain_path = "../Examples/Basic/basic.hddl"
        self.basic_pb1_path = "../Examples/Basic/pb1.hddl"
        self.basic_pb1_path_SHOP = "../Examples/Basic/pb1.shop"
        self.test_tools_path = "TestTools/"
        self.blocksworld_path = "../Examples/Blocksworld/"