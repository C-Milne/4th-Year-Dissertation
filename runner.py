import sys
import os
from Parsers.HDDL.HDDL_Parser import HDDLParser
from Solver.solver import Solver


class Runner:
    def __init__(self, domain_path, problem_path):
        # Parse domain
        self.parser = None
        self.suffix = None

        # Check domain file exists
        self.__check_file_exists(domain_path, "Domain")
        self.__parse_domain(domain_path)

        # Parse problem
        self.__check_file_exists(problem_path, "Problem")
        self.__parse_problem(problem_path)

        # Solve
        self.solver = Solver(self.parser)
        self.solver.solve()
        self.solver.output()

    def __parse_domain(self, domain_path):
        # Check for valid suffix
        self.suffix = self.__get_suffix(domain_path)
        if self.suffix == "hddl":
            self.parser = HDDLParser()
        elif self.suffix == "jshop":
            pass
        else:
            raise TypeError("Unknown descriptor type ({})".format(self.suffix))
        self.parser.parse_domain(domain_path)

    def __parse_problem(self, problem_path):
        suffix = self.__get_suffix(problem_path)
        if suffix == self.suffix:
            self.parser.parse_problem(problem_path)
        else:
            raise TypeError("Problem file type ({}) does not match domain file type ({})".format(suffix, self.suffix))

    def __check_file_exists(self, file_path, file_purpose=None):
        if not os.path.exists(file_path):
            if file_purpose is None:
                raise FileNotFoundError("File {} could not be found".format(file_path))
            else:
                raise FileNotFoundError("{} file entered could not be found. ({})".format(file_purpose, file_path))

    @staticmethod
    def __get_suffix(path):
        return path[path.rindex(".") + 1:]


if __name__ == "__main__":
    if len(sys.argv) == 3:
        Runner(sys.argv[1], sys.argv[2])
    else:
        # Incorrect usage of program
        raise IOError("Expected 3 arguments, got {}.\nCorrect usage 'python runner.py <domain.suffix> <problem.suffix>'"
                      .format(len(sys.argv)))
