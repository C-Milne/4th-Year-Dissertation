import sys
import os
from Parsers.HDDL_Parser import HDDLParser
from Parsers.JSHOP_Parser import JSHOPParser
from Solver.solver import Solver
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem


class Runner:
    def __init__(self, domain_path, problem_path):
        # Necessary variables
        self.parser = None
        self.suffix = None
        self.domain = Domain(None)
        self.problem = Problem(self.domain)
        self.domain.add_problem(self.problem)
        self.solver = Solver(self.domain, self.problem)
        self.domain_path = domain_path
        self.problem_path = problem_path

    def parse_domain(self):
        self.__check_file_exists(self.domain_path, "Domain")
        # Check for valid suffix
        self.suffix = self.__get_suffix(self.domain_path)
        if self.suffix == "hddl":
            self.parser = HDDLParser(self.domain, self.problem)
        elif self.suffix is None:
            self.parser = JSHOPParser(self.domain, self.problem)
        else:
            raise TypeError("Unknown descriptor type ({})".format(self.suffix))
        self.parser.parse_domain(self.domain_path)

    def parse_problem(self):
        self.__check_file_exists(self.problem_path, "Problem")
        suffix = self.__get_suffix(self.problem_path)
        if suffix == self.suffix:
            self.parser.parse_problem(self.problem_path)
        else:
            raise TypeError("Problem file type ({}) does not match domain file type ({})".format(suffix, self.suffix))

    def set_heuristic(self, heuristic):
        self.solver.set_heuristic(heuristic)

    def set_early_task_precon_checker(self, v: bool):
        self.solver.task_expansion_given_param_check = v

    def solve(self):
        return self.solver.solve()

    def output_result(self, search_result):
        self.solver.output(search_result)

    @staticmethod
    def __check_file_exists(file_path, file_purpose=None):
        if not os.path.exists(file_path):
            if file_purpose is None:
                raise FileNotFoundError("File {} could not be found".format(file_path))
            else:
                raise FileNotFoundError("{} file entered could not be found. ({})".format(file_purpose, file_path))


    @staticmethod
    def __get_suffix(path):
        try:
            return path[path.rindex(".") + 1:]
        except ValueError:
            return None


if __name__ == "__main__":
    if len(sys.argv) == 3:
        controller = Runner(sys.argv[1], sys.argv[2])
        controller.parse_domain()
        controller.parse_problem()
        result = controller.solve()
        controller.output_result(result)
    else:
        # Incorrect usage of program
        raise IOError("Expected 3 arguments, got {}.\nCorrect usage 'python runner.py <domain.suffix> <problem.suffix>'"
                      .format(len(sys.argv)))
