import unittest
from unittest import mock
from io import StringIO
from Tests.UnitTests.HDDL_Parser_Tests import HDDLParsingTests
from Tests.UnitTests.HDDL_Grounding_Tests import HDDLGroundingTests
from Tests.UnitTests.Solving_Tests import SolvingTests
from Tests.UnitTests.IPC_Tests import IPCTests
from Tests.UnitTests.JSHOP_Parser_Tests import JSHOPParsingTests
from Tests.UnitTests.JSHOP_Solving_Tests import JSHOPSolvingTests

"""https://stackoverflow.com/questions/12011091/trying-to-implement-python-testsuite"""


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(HDDLParsingTests))
    test_suite.addTest(unittest.makeSuite(HDDLGroundingTests))
    test_suite.addTest(unittest.makeSuite(JSHOPParsingTests))
    test_suite.addTest(unittest.makeSuite(JSHOPSolvingTests))
    test_suite.addTest(unittest.makeSuite(SolvingTests))
    test_suite.addTest(unittest.makeSuite(IPCTests))
    return test_suite


if __name__ == "__main__":
    test_suite = suite()

    with mock.patch('sys.stdout', new=StringIO()) as std_out:
        runner = unittest.TextTestRunner()
        runner.run(test_suite)
