import re
from Internal_Representation.action import Action
from Internal_Representation.method import Method
from Internal_Representation.predicate import Predicate
from Internal_Representation.task import Task
from Internal_Representation.Type import Type
from Internal_Representation.Object import Object
from Internal_Representation.precondition import Precondition


class HDDLParser:
    def __init__(self, domain, problem):
        self.domain = domain
        self.problem = problem

        self.requirements = []

        self.domain_name = None
        self.domain_path = None
        self.problem_name = None
        self.problem_path = None

    def parse_domain(self, domain_path):
        self.domain_path = domain_path
        tokens = self.__scan_tokens(domain_path)
        if type(tokens) is list and tokens.pop(0) == 'define':
            while tokens:
                group = tokens.pop(0)
                lead = group.pop(0)

                if lead == ":action":
                    self.__parse_action(group)
                elif lead == ":method":
                    self.__parse_method(group)
                elif lead == ":task":
                    self.__parse_task(group)
                elif lead == "domain":
                    self.domain_name = group[0]
                elif lead == ":requirements":
                    self.requirements = group
                elif lead == ":predicates":
                    self.__parse_predicate(group)
                elif lead == ":types":
                    self.__parse_type(group)
                elif lead == ":constraints":
                    self.__parse_constraints(group)
                else:
                    raise AttributeError("Unknown tag; {}".format(lead))

    def parse_problem(self, problem_path):
        self.problem_path = problem_path
        tokens = self.__scan_tokens(problem_path)
        if type(tokens) is list and tokens.pop(0) == 'define':
            while tokens:
                group = tokens.pop(0)
                lead = group.pop(0)

                if lead == "problem":
                    self.__set_problem_name(group)
                elif lead == ":domain":
                    self.__check_domain_name(group)
                elif lead == ":objects":
                    self.__parse_objects(group)
                elif lead == ":init":
                    self.__parse_initial_state(group)
                elif lead == ":goal":
                    self.__parse_goal_state(group)
                elif lead == ":htn":
                    self.__parse_htn_tag(group)

    def is_goal_empty(self):
        if self.goal_state == {}:
            return True
        return False

    def __check_domain_name(self, name):
        """Returns True - if param: name is equal to self.domain_name"""
        if type(name) == list:
            name = name[0]
        if name == self.domain_name:
            return True
        else:
            raise NameError("Domain specified in problem file {} ({}). Does not match domain specified in {} ({})"
                            .format(self.problem_path, name, self.domain_path, self.domain_name))

    """Methods for parsing domains"""
    def __parse_action(self, params):
        action = Action(params, self.domain)
        self.domain.add_action(action)

    @staticmethod
    def __scan_tokens(file_path):
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

    def __parse_predicate(self, params):
        for i in params:
            self.domain.add_predicate(Predicate(params))

    def __parse_method(self, params):
        method = Method(params, self.domain)
        self.domain.add_method(method)

    def __parse_task(self, params):
        if type(params[0]) == str:
            self.domain.add_task(Task(params, self.domain))
        else:
            raise SyntaxError("Incorrect Definition of Task. A task needs a name.")

    def __parse_type(self, params):
        i = 0
        l = len(params)
        while i < l:
            if i + 1 < l:
                if params[i + 1] == "-":
                    super_type_name = params[i + 1]
                    # Check if super type is a registered type
                    super_type = self.domain.get_type(super_type_name)
                    if super_type is False:
                        self.domain.add_type(Type(super_type_name))
                        super_type = self.domain.get_type(super_type_name)
                    self.domain.add_type(Type(params[i], super_type))
                else:
                    self.domain.add_type(Type(params[i]))
            else:
                self.domain.add_type(Type(params[i]))
            i += 1

    def __parse_constraints(self, params):
        """TODO - Implement constraints"""
        raise NotImplementedError("Constraints are not supported yet")

    """Methods for parsing problems"""
    def __set_problem_name(self, name):
        self.problem_name = name

    def __parse_objects(self, group):
        new_obs = []
        i = 0
        while i < len(group):
            if group[i] != "-":
                new_obs.append(Object(group[i]))
                i += 1
            else:
                obs_type = group[i + 1]
                obs_type = self.domain.get_type(obs_type)
                for j in new_obs:
                    j.set_type(obs_type)
                self.problem.add_object(new_obs)
                new_obs = []
                i += 2
        self.problem.add_object(new_obs)

    def __parse_initial_state(self, params):
        """TODO - check params are valid predicates"""
        for i in params:
            if type(i) != list:
                raise TypeError("{} is not a valid predicate for initial state".format(i))
            self.problem.add_to_initial_state(i)

    def __parse_goal_state(self, params):
        if len(params) == 1 and type(params[0]) == list:
            params = params[0]
        self.problem.add_goal_conditions(Precondition(params, self.domain)) # Goal state is just a list of conditions to be satisfied

    def __parse_htn_tag(self, params):
        """TODO - Do tests on this"""
        while params:
            lead = params.pop(0)

            if lead == ":subtasks" or lead == ":ordered-subtasks" or lead == ":tasks" or lead == ":ordered-tasks":
                self.__parse_subtasks_to_execute(params.pop(0))
            elif lead == ":parameters":
                if len(params.pop(0)) > 0:
                    raise NotImplementedError("Not implemented yet")
            elif lead == ":ordering":
                self.problem.order_subtasks(params.pop(0))
            else:
                raise TypeError("Unknown keyword {}".format(lead))

    def __parse_subtasks_to_execute(self, params):
        """TODO - Do some tests on this"""
        self.problem.add_subtasks_execute(params)
