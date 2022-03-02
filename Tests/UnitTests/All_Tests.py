import unittest
from Tests.UnitTests.HDDL_Parser_Tests import HDDLParsingTests
from Tests.UnitTests.HDDL_Grounding_Tests import HDDLGroundingTests
from Tests.UnitTests.Solving_Tests import SolvingTests

"""https://stackoverflow.com/questions/12011091/trying-to-implement-python-testsuite"""


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(HDDLParsingTests))
    test_suite.addTest(unittest.makeSuite(HDDLGroundingTests))
    test_suite.addTest(unittest.makeSuite(SolvingTests))
    return test_suite


if __name__ == "__main__":
    test_suite = suite()

    runner = unittest.TextTestRunner()
    runner.run(test_suite)
