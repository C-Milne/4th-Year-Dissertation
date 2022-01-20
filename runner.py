import sys
from Parsers.HDDL.HDDL_Parser import HDDLParser


class Runner:
    def __init__(self, domain_path, problem_path):
        # Parse domain
        self.parser = None
        self.__parse_domain(domain_path)
        # Parse problem
        # Solve
        pass

    def __parse_domain(self, domain_path):
        # Check for valid suffix
        suffix = self.__get_suffix(domain_path)
        if suffix == "hddl":
            self.parser = HDDLParser()
        elif suffix == "jshop":
            pass
        else:
            raise TypeError("Unknown domain type ({})".format(suffix))
        self.parser.parse_domain(domain_path)

    def __get_suffix(self, path):
        return path[path.rindex(".") + 1:]


if __name__ == "__main__":
    if len(sys.argv) == 3:
        Runner(sys.argv[1], sys.argv[2])
