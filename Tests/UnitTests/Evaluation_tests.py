import unittest
from Tests.Evaluation.Heuristic_Evaluation.problem_size_calculator import calculate_size


class IPCTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_path = "../Examples/Basic/"
        self.rover_path = "../Examples/Rover/"
        self.write_path = "../Evaluation/Heuristic_Evaluation/problem_sizes.pickle"

    def test_calculating_basic_size(self):
        res = calculate_size(self.basic_path + "basic.hddl", self.basic_path + "pb1.hddl", self.write_path)
        print(res)

    def test_calculating_rover_1_size(self):
        res = calculate_size(self.rover_path + "domain.hddl", self.rover_path + "p01.hddl", self.write_path)
        print(res)

    def test_calculating_rover_3_size(self):
        res = calculate_size(self.rover_path + "domain.hddl", self.rover_path + "p03.hddl", self.write_path)
        print(res)

    def test_calculating_rover_2_size(self):
        res = calculate_size(self.rover_path + "domain.hddl", self.rover_path + "p02.hddl", self.write_path)
        print(res)

    def test_calculating_rover_4_size(self):
        res = calculate_size(self.rover_path + "domain.hddl", self.rover_path + "p04.hddl", self.write_path)
        print(res)

    def test_calculating_rover_5_size(self):
        res = calculate_size(self.rover_path + "domain.hddl", self.rover_path + "p05.hddl", self.write_path)
        print(res)

    def test_calculating_rover_6_size(self):
        res = calculate_size(self.rover_path + "domain.hddl", self.rover_path + "p06.hddl", self.write_path)
        print(res)

    def test_calculating_rover_7_size(self):
        res = calculate_size(self.rover_path + "domain.hddl", self.rover_path + "p07.hddl", self.write_path)
        print(res)
