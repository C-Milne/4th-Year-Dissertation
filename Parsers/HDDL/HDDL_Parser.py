import re
from Parsers.HDDL.action import Action


class HDDLParser:
    def __init__(self):
        self.states = {}
        self.objects = []
        self.actions = []
        self.methods = []
        self.predicates = {}
        self.types = []
        self.requirements = []
        self.foralls = []
        self.domain_name = None

    def parse_domain(self, domain_path):
        tokens = self.__scan_tokens(domain_path)
        if type(tokens) is list and tokens.pop(0) == 'define':
            while tokens:
                group = tokens.pop(0)
                lead = group.pop(0)

                if lead == ":action":
                    self.__parse_action(group)
                elif lead == ":method":
                    self.__parse_methods(group)
                elif lead == ":task":
                    pass
                elif lead == "domain":
                    self.domain_name = group[0]
                elif lead == ":requirements":
                    pass
                elif lead == "predicates":
                    pass
                elif lead == ":types":
                    pass
                elif lead == ":constraints":
                    pass

    def parse_problem(self, problem_path):
        pass

    def name_assigned(self, str):
        print("TODO: Implement name_assigned")
        return False

    def __parse_action(self, params):
        action = Action(params, self)
        self.actions.append(action)

    def __scan_tokens(self, file_path):
        with open(file_path,'r') as f:
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

    def __parse_predicates(self):
        pass

    def __parse_method(self, params):
        pass
