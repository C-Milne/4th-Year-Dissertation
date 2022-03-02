import unittest
from Tests.UnitTests.HDDL_Parser_Tests import HDDLParsingTests
from Tests.UnitTests.HDDL_Grounding_Tests import HDDLGroundingTests


def suite():
    """
        Gather all the tests from this module in a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(HDDLParsingTests))
    test_suite.addTest(unittest.makeSuite(HDDLGroundingTests))
    return test_suite


if __name__ == "__main__":
    test_suite = suite()

    runner = unittest.TextTestRunner()
    runner.run(test_suite)