import unittest
from Tests.Evaluation.Heuristic_Evaluation.problem_size_calculator import calculate_size


class EvaluationTests(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_path = "../Examples/Basic/"
        self.rover_path = "../Examples/Rover/"
        self.depot_path = "../Examples/Depots/"
        self.translog_path = "../Examples/IPC_Tests/um-translog01/"
        self.factories_path = "../Examples/Factories/"
        self.barman_path = "../Examples/Barman/"
        self.PO_rover_path = "../Examples/Partial_Order/Rover/"
        self.PO_barman_path = "../Examples/Partial_Order/Barman/"
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

    def test_calculating_depot_1_size(self):
        res = calculate_size(self.depot_path + "domain.hddl", self.depot_path + "p01.hddl", self.write_path)
        print(res)

    def test_calculating_depot_2_size(self):
        res = calculate_size(self.depot_path + "domain.hddl", self.depot_path + "p02.hddl", self.write_path)
        print(res)

    def test_calculating_depot_3_size(self):
        res = calculate_size(self.depot_path + "domain.hddl", self.depot_path + "p03.hddl", self.write_path)
        print(res)

    def test_calculating_translog_size(self):
        res = calculate_size(self.translog_path + "domain.hddl", self.translog_path + "problem.hddl", self.write_path)
        print(res)

    def test_calculating_factories_1_size(self):
        res = calculate_size(self.factories_path + "domain.hddl", self.factories_path + "pfile01.hddl", self.write_path)
        print(res)

    def test_calculating_barman_1_size(self):
        res = calculate_size(self.barman_path + "domain.hddl", self.barman_path + "pfile01.hddl", self.write_path)
        print(res)

    def test_calculating_PO_rover_1_size(self):
        res = calculate_size(self.PO_rover_path + "domain.hddl", self.PO_rover_path + "pfile01.hddl", self.write_path)
        print(res)

    def test_calculating_PO_rover_2_size(self):
        res = calculate_size(self.PO_rover_path + "domain.hddl", self.PO_rover_path + "pfile02.hddl", self.write_path)
        print(res)

    def test_calculating_PO_rover_3_size(self):
        res = calculate_size(self.PO_rover_path + "domain.hddl", self.PO_rover_path + "pfile03.hddl", self.write_path)
        print(res)

    def test_calculating_PO_rover_4_size(self):
        res = calculate_size(self.PO_rover_path + "domain.hddl", self.PO_rover_path + "pfile04.hddl", self.write_path)
        print(res)

    def test_calculating_PO_barman_1_size(self):
        res = calculate_size(self.PO_barman_path + "domain.hddl", self.PO_barman_path + "pfile01.hddl", self.write_path)
        print(res)
