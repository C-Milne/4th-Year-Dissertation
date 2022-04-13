import argparse
import os
import pickle
import sys
import importlib.util
import inspect
from Parsers.HDDL_Parser import HDDLParser
from Parsers.JSHOP_Parser import JSHOPParser
from Solver.solver import Solver
from Solver.Heuristics.Heuristic import Heuristic
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem


class Runner:
    def __init__(self, domain_path, problem_path, **kwargs):
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

    def set_heuristic(self, heuristic: type(Heuristic)):
        self.solver.set_heuristic(heuristic)

    def set_heuristic_from_file(self, module_name: str, file_path: str):
        # Load Class
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and name == module_name:
                self.set_heuristic(obj)
                break

    def set_early_task_precon_checker(self, v: bool):
        self.solver.task_expansion_given_param_check = v

    def solve(self):
        return self.solver.solve()

    def output_result(self, search_result):
        self.solver.output(search_result)

    @staticmethod
    def output_result_file(result, write_file):
        # Check output folder exists
        if not os.path.isdir("output"):
            os.mkdir("output")

        # Pickle output and write to file
        file = open("output/" + write_file, "wb")
        file.write(pickle.dumps(result))
        file.close()

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
    argparser = argparse.ArgumentParser()
    argparser.add_argument("Domain_File", metavar='D', type=str, nargs="?", help='File path to Domain File', default=None)
    argparser.add_argument("Problem_File", metavar='P', type=str, nargs="?", help='File path to Problem File', default=None)
    argparser.add_argument("-w", type=str, help='File path to Write Resulting Plan File', default=None)
    argparser.add_argument("-heuModName", type=str, help='File path to Heuristic File', default=None)
    argparser.add_argument("-heuPath", type=str, help='File path to Heuristic File', default=None)
    argparser.format_help()
    args = argparser.parse_args()

    domain_file = args.Domain_File
    problem_file = args.Problem_File
    write_file = args.w
    heuristic_mod_name = args.heuModName
    heuristic_file = args.heuPath

    if heuristic_mod_name is not None and heuristic_file is None or \
            heuristic_mod_name is None and heuristic_file is not None:
        argparser.error("Incorrect Usage. Either both '-heuModName' and '-heuPath' need to be set of both need to be empty")

    if domain_file is not None and problem_file is not None:
        # Setup runner object
        controller = Runner(domain_file, problem_file)

        # Parse domain and problem
        controller.parse_domain()
        controller.parse_problem()

        # Heuristic selection
        if heuristic_mod_name is not None and heuristic_file is not None:
            controller.set_heuristic_from_file(heuristic_mod_name, heuristic_file)

        # Initiate solving
        result = controller.solve()

        # Print result
        controller.output_result(result)

        # Check if we need to write to file
        if write_file is not None:
            controller.output_result_file(result, write_file)
    else:
        # Incorrect usage of program
        argparser.error("Incorrect Usage. Correct usage 'python runner.py <domain.suffix> <problem.suffix>'")
