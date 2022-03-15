import re
from Internal_Representation.domain import Domain
from Internal_Representation.problem import Problem
from Internal_Representation.reg_parameter import RegParameter
from Internal_Representation.precondition import Precondition
from Internal_Representation.subtasks import Subtasks
from Internal_Representation.task import Task
from Internal_Representation.Object import Object
from Internal_Representation.list_parameter import ListParameter


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

    def parse_domain(self, *args):
        raise NotImplementedError

    def parse_problem(self, *args):
        raise NotImplementedError

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

    def _parse_parameters(self, params) -> list[RegParameter]:
        def __add_t_param_list(t=None):
            for i in param_names:
                param_list.append(RegParameter(i, t))

        """Parses list of parameters and returns a list of parameters
        params  - params : ['?a', '-', 'ob1', '?b', '?c', '-', 'ob2' ...]"""
        i = 0
        l = len(params)
        param_list = []
        param_names = []
        while i < l:
            p = params[i]
            if type(p) == list:
                raise TypeError("This method does not accept a list within a list")
            elif p == "-":
                param_type_name = params[i + 1]
                param_type = self.domain.get_type(param_type_name)
                if param_type is None or params == False:
                    raise TypeError("Invalid type {}".format(param_type_name))
                __add_t_param_list(param_type)
                param_names = []
                i += 1
            elif type(p) == str:
                param_names.append(p)
            else:
                raise TypeError("Unexpected token {}".format(p))
            i += 1
        __add_t_param_list()
        return param_list

    def _parse_precondition(self, params):
        return Precondition(params)

    def _parse_subtasks(self, params):
        """:params  params  : ['and', ['task0', ['drop', '?rover', '?s']]]
                            : ['swap', 'banjo', 'kiwi']"""
        if len(params) == 0:
            return None
        else:
            subtasks = Subtasks()
            i = 0
            l = len(params)
            while i < l:
                task_label, task_modifier, task_parameters = None, None, None
                if params[i] == "and":
                    pass
                else:
                    # Check if there is a list within a list
                    if len(params[i]) > 1 and type(params[i][1]) == list:
                        task_label = params[i][0]
                        task_modifier = params[i][1][0]

                        task_parameters = self._parse_parameters(params[i][1][1:])
                    elif type(params[i]) == list:
                        # No task Label
                        task_modifier = params[i][0]
                        task_parameters = self._parse_parameters(params[i][1:])

                    elif all([type(x) == str for x in params]):
                        task_modifier = params[0]
                        task_parameters = self._parse_parameters(params[1:])
                        i += len(params)
                    else:
                        raise SyntaxError("Unrecognised Format {}".format(params))

                    task_modifier_ob = self.domain.get_modifier(task_modifier)
                    if not task_modifier_ob is None:
                        task_modifier = task_modifier_ob
                    subtasks.add_subtask(task_label, task_modifier, task_parameters)

                    if type(task_modifier) == str:
                        # Mark this method for grounding after parsing has finished
                        self._requires_grounding.append(subtasks.tasks[len(subtasks) - 1])
                i += 1
        return subtasks

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

    def _post_problem_parsing_grounding(self):
        for item in self._requires_grounding:
            if type(item) == Subtasks:
                # Subtask parameter type should be object
                for t in item.tasks:
                    i = 0
                    if type(t.parameters) == ListParameter:
                        continue
                    l = len(t.parameters)
                    while i < l:
                        if type(t.parameters[i]) == RegParameter:
                            t.parameters[i] = self.problem.get_object(t.parameters[i].name)
                        elif type(t.parameters[i]) == Object:
                            pass
                        else:
                            raise AttributeError("Grounding process for subtask with type {} unknown".format(type(t.parameters[i])))
                        i += 1
            elif type(item) == Subtasks.Subtask:
                # Parameters must be objects
                i = 0
                l = len(item.parameters)
                while i < l:
                    if type(item.parameters[i]) == RegParameter:
                        item.parameters[i] = self.problem.get_object(item.parameters[i].name)
                    elif type(item.parameters[i]) == Object:
                        pass
                    else:
                        raise AttributeError(
                            "Grounding process for subtask with type {} unknown".format(type(item.parameters[i])))
                    i += 1

                # Task must be a task instance not a string
                if type(item.task) != Task:
                    assert type(item.task) == str
                    item.task = self.domain.get_task(item.task)
            else:
                raise NotImplementedError("Functionality for post problem grounding of {} is not implemented".format(type(item)))
        self._requires_grounding = []
