import re
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem


class Parser:
    def __init__(self, domain, problem):
        assert type(domain) == Domain
        self.domain = domain
        assert type(problem) == Problem
        self.problem = problem

        self.requirements = []
        self._requires_grounding = []

        self.domain_name = None
        self.domain_path = None
        self.problem_name = None
        self.problem_path = None

    def _parse_type(self, *args):
        raise NotImplementedError

    def _parse_predicate(self, *args):
        raise NotImplementedError

    def _parse_action(self, *args):
        raise NotImplementedError

    def _parse_method(self, *args):
        raise NotImplementedError

    def _parse_task(self, *args):
        raise NotImplementedError

    def _parse_predicates(self, *args):
        raise NotImplementedError

    def _parse_type(self, *args):
        raise NotImplementedError

    def _parse_constraint(self, *args):
        raise NotImplementedError

    def _post_domain_parsing_grounding(self, *args):
        raise NotImplementedError

    def _set_problem_name(self, *args):
        raise NotImplementedError

    def _check_domain_name(self, *args):
        raise NotImplementedError

    def _parse_objects(self, *args):
        raise NotImplementedError

    def _parse_initial_state(self, *args):
        raise NotImplementedError

    def _parse_goal_state(self, *args):
        raise NotImplementedError

    def _parse_htn_tag(self, *args):
        raise NotImplementedError

    def _parse_constant(self, *args):
        raise NotImplementedError

    def _scan_tokens(self, file_path):
        """ Taken with permission from:
        https://github.com/pucrs-automated-planning/heuristic-planning/blob/master/pddl/pddl_parser.py"""
        with open(file_path, 'r') as f:
            # Remove single line comments
            str = re.sub(r';.*$', '', f.read(), flags=re.MULTILINE).lower()
        # Tokenize
        stack = []
        sections = []
        for t in re.findall(r'[()]|[^\s()]+', str):
            if t == '(':
                stack.append(sections)
                sections = []
            elif t == ')':
                if stack:
                    l = sections
                    sections = stack.pop()
                    sections.append(l)
                else:
                    raise Exception('Missing open parentheses')
            else:
                sections.append(t)
        if stack:
            raise Exception('Missing close parentheses')
        if len(sections) != 1:
            raise Exception('Malformed expression')
        return sections[0]
