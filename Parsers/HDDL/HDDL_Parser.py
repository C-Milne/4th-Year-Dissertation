import re
from Parsers.HDDL.action import Action
from Parsers.HDDL.method import Method
from Parsers.HDDL.predicate import Predicate
from Parsers.HDDL.task import Task
from Parsers.HDDL.Type import Type


class HDDLParser:
    def __init__(self):
        self.initial_state = {}
        self.goal_state = {}
        self.objects = []
        self.actions = {}
        self.methods = {}
        self.tasks = {}
        self.predicates = {}
        self.types = {}
        self.requirements = []
        self.foralls = []
        self.subtasks_to_execute = []
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

    def name_assigned(self, str):
        """:param   - str : string being checked
            :returns    - True : if str is already in use
                        - False : otherwise"""
        if str in self.methods.keys() or str in self.tasks.keys() or str in self.actions.keys():
            return True
        return False

    def is_goal_empty(self):
        if self.goal_state == {}:
            return True
        return False

    def get_action(self, action_name):
        """Return an actions object
        :params     - action_name : name of object to be returned
        :returns    - action object : if can be found
                    - False : otherwise"""
        try:
            return self.actions[action_name]
        except:
            # Could not find action
            pass
        return False

    def get_task(self, name, *args):
        if name in self.tasks.keys():
            # Compare parameters given with parameters of task
            task = self.tasks[name]
            if len(args) > 0:
                if task.compare_params_soft(args):
                    return task
                else:
                    raise SyntaxError("Parameters Given for Task {} ({}), Do Not Match Parameters on Record ({})"
                                      .format(name, args[0], task.get_parameter_names()))
            else:
                # No parameters given
                if len(task.parameters) == 0:
                    return task
                else:
                    raise SyntaxError("Could not find Task {} with no Parameters.".format(name))

    def get_type(self, name):
        if name in self.types:
            return self.types[name]
        else:
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
        action = Action(params, self)
        self.actions[action.name] = action

    def __scan_tokens(self, file_path):
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
            self.predicates[i[0]] = Predicate(params)

    def __parse_method(self, params):
        method = Method(params, self)
        self.methods[method.name] = method

    def __parse_task(self, params):
        if type(params[0]) == str:
            self.tasks[params[0]] = Task(params, self)
        else:
            raise SyntaxError("Incorrect Definition of Task. A task needs a name.")

    def __parse_type(self, params):
        """TODO - Implement Type hierarchy"""
        i = 0
        l = len(params)
        while i < l:
            if i + 1 < l:
                if params[i + 1] == "-":
                    raise NotImplementedError("This is not implemented yet")

            self.types[params[i]] = Type(params[i])
            i += 1

    def __parse_constraints(self, params):
        """TODO - Implement constraints"""
        raise NotImplementedError("Constraints are not supported yet")

    """Methods for parsing problems"""
    def __set_problem_name(self, name):
        self.problem_name = name

    def __parse_objects(self, group):
        """TODO - Implement object Types?"""
        for ob in group:
            self.objects.append(ob)

    def __parse_initial_state(self, params):
        """TODO - check params are valid predicates"""
        for i in params:
            if type(i) != list:
                raise TypeError("{} is not a valid predicate for initial state".format(i))
            if i[0] in self.initial_state.keys():
                self.initial_state[i[0]].append(i[1])
            else:
                if len(i) > 1:
                    self.initial_state[i[0]] = [i[1]]
                    del i[1]
                    while len(i) > 2:
                        self.initial_state[i[0]].append(i[1])
                        del i[1]
                elif len(i) == 1:
                    self.initial_state[i[0]] = True
                else:
                    raise NotImplementedError("This case is not implemented")

    def __parse_goal_state(self, params):
        """TODO - Implement this"""
        raise NotImplementedError("Parsing Goal state not yet implemented")

    def __parse_htn_tag(self, params):
        """TODO - Implement this. Also do tests on this"""
        while params:
            lead = params.pop(0)

            if lead == ":subtasks" or lead == ":ordered-subtasks" or lead == ":tasks" or lead == ":ordered-tasks":
                self.__parse_subtasks_to_execute(params.pop(0))
            elif lead == ":parameters":
                raise NotImplementedError("Not implemented yet")
            else:
                raise TypeError("Unknown keyword {}".format(lead))

    def __parse_subtasks_to_execute(self, params):
        """TODO - Do some tests on this"""
        self.subtasks_to_execute.append(params)
