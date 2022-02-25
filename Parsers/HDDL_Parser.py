from Internal_Representation.action import Action
from Internal_Representation.method import Method
from Internal_Representation.predicate import Predicate
from Internal_Representation.task import Task
from Internal_Representation.Type import Type
from Internal_Representation.Object import Object
from Internal_Representation.precondition import Precondition
from Parsers.parser import Parser
from Internal_Representation.parameter import Parameter
from Internal_Representation.effects import Effects
from Internal_Representation.subtasks import Subtasks


class HDDLParser(Parser):
    def __init__(self, domain, problem):
        super().__init__(domain, problem)

    def parse_domain(self, domain_path):
        self.domain_path = domain_path
        tokens = self._scan_tokens(domain_path)
        if type(tokens) is list and tokens.pop(0) == 'define':
            while tokens:
                group = tokens.pop(0)
                lead = group.pop(0)

                if lead == ":action":
                    action = self._parse_action(group)
                    self.domain.add_action(action)
                elif lead == ":method":
                    method = self._parse_method(group)
                    self.domain.add_method(method)
                elif lead == ":task":
                    task = self._parse_task(group)
                    self.domain.add_task(task)
                elif lead == "domain":
                    self.domain_name = group[0]
                elif lead == ":requirements":
                    self.requirements = group
                elif lead == ":predicates":
                    self._parse_predicates(group)
                elif lead == ":types":
                    self._parse_type(group)
                elif lead == ":constraints":
                    self._parse_constraints(group)
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

    def __check_domain_name(self, name):
        """Returns True - if param: name is equal to self.domain_name"""
        if type(name) == list:
            name = name[0]
        if name == self.domain_name:
            return True
        else:
            raise NameError("Domain specified in problem file {} ({}). Does not match domain specified in {} ({})"
                            .format(self.problem_path, name, self.domain_path, self.domain_name))

    def _parse_type(self, params):
        i = 0
        l = len(params)
        while i < l:
            if i + 1 < l:
                if params[i + 1] == "-":
                    super_type_name = params[i + 2]
                    # Check if super type is already a registered type
                    super_type = self.domain.get_type(super_type_name)
                    if super_type is False:
                        self.domain.add_type(Type(super_type_name))
                        super_type = self.domain.get_type(super_type_name)
                    self.domain.add_type(Type(params[i], super_type))
                    i += 2
                else:
                    self.domain.add_type(Type(params[i]))
            else:
                self.domain.add_type(Type(params[i]))
            i += 1

    def _parse_predicates(self, params):
        for i in params:
            predicate_name = i[0]
            if len(i) > 1:
                parameter_list = self._parse_parameters(i[1:])
                self.domain.add_predicate(Predicate(predicate_name, parameter_list))

    def _parse_parameters(self, params):
        """TODO : test this - check parameter name not already in use"""
        """Parses list of parameters and returns a list of parameters
        params  - params : ['?a', '-', 'ob1', '?b', '?c', '-', 'ob2' ...]"""
        i = 0
        l = len(params)
        param_list = []
        while i < l:
            p = params[i]
            if type(p) == list:
                raise TypeError("This method does not accept a list within a list")
            param_type = None
            if i + 1 < l:
                if params[i + 1] == "-":
                    param_type = self.domain.get_type(params[i + 2])
                    i += 2
            if type(p) == str and (type(param_type) == Type or param_type is None):
                param_list.append(Parameter(p, param_type))
            else:
                raise TypeError("Task Parameters Must be a String")
            i += 1
        return param_list

    def _parse_action(self, params):
        i = 0
        l = len(params)
        action_name, parameters, precon, effects = None, None, None, None
        while i < l:
            if i == 0:
                action_name = params[i]
            elif params[i] == ":parameters":
                parameters = self._parse_parameters(params[i + 1])
                i += 1
            elif params[i] == ":precondition":
                precon = self._parse_precondition(params[i + 1])
                i += 1
            elif params[i] == ":effect":
                effects = self._parse_effects(params[i + 1])
                i += 1
            else:
                raise TypeError("Unknown identifier {}".format(params[i]))
            i += 1
        return Action(action_name, parameters, precon, effects)

    def _parse_precondition(self, params):
        return Precondition(params)

    def _parse_effects(self, params):
        def __extract_effect_values(params):
            if len(params) > 1:
                return params[0], params[1:]
            return params[0], []
        i = 0
        l = len(params)
        effects = Effects()
        while i < l:
            negated, predicate_name, parameters = False, None, []
            if params[i] == "and":
                pass
            else:
                e = 0
                while e < len(params[i]):
                    if params[i][e] == "not":
                        negated = True
                        assert type(params[i][e + 1]) == list
                        predicate_name, parameters = __extract_effect_values(params[i][e+1])
                        e += 1
                    else:
                        predicate_name, parameters = __extract_effect_values(params[i])
                        e += len(parameters) + 1
                    e += 1
                effects.add_effect(predicate_name, parameters, negated)
            i += 1
        return effects

    def _parse_task(self, params):
        """Returns  : Task"""
        i = 0
        l = len(params)
        task_name, parameters = None, []
        while i < l:
            if i == 0:
                task_name = params[i]
            elif params[i] == ":parameters":
                assert i + 1 < l
                parameters = self._parse_parameters(params[i + 1])
                i += 1
            else:
                raise TypeError
            i += 1
        return Task(task_name, parameters)

    def _parse_method(self, params):
        i = 0
        l = len(params)
        method_name, parameters, precon, task, subtasks = None, None, None, None, None
        while i < l:
            if i == 0:
                assert type(params[i]) == str
                method_name = params[i]
            elif params[i] == ":parameters":
                parameters = self._parse_parameters(params[i + 1])
                i += 1
            elif params[i] == ":precondition":
                precon = self._parse_precondition(params[i + 1])
                i += 1
            elif params[i] == ":task":
                if len(params[i + 1]) == 1:
                    task = {"task": self.domain.get_task(params[i + 1][0])}
                else:
                    task = {"task": self.domain.get_task(params[i + 1][0]), "params": self._parse_parameters(params[i + 1][1:])}
                i += 1
            elif params[i] == ":ordered-subtasks" or params[i] == ":ordered-tasks" or params[i] == ":subtasks" or \
                        params[i] == ":tasks":
                subtasks = self._parse_subtasks(params[i + 1])
                i += 1
            elif params[i] == ":ordering":
                assert not subtasks is None
                subtasks.order_subtasks(params[i + 1])
                i += 1
            else:
                raise SyntaxError("Unknown token {}".format(params[i]))
            i += 1
        return Method(method_name, parameters, precon, task, subtasks)

    def _parse_subtasks(self, params):
        """:params  params  : ['and', ['task0', ['drop', '?rover', '?s']]]"""
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
                elif type(params[i]) == list:
                    # Check if there is a list within a list
                    if len(params[i]) > 1 and type(params[i][1]) == list:
                        task_label = params[i][0]
                        task_modifier = params[i][1][0]

                        task_modifier_ob = self.domain.get_modifier(task_modifier)
                        if not task_modifier_ob is None:
                            task_modifier = task_modifier_ob

                        task_parameters = self._parse_parameters(params[i][1][1:])
                    subtasks.add_subtask(task_label, task_modifier, task_parameters)

                    if type(task_modifier) == str:
                        # Mark this method for grounding after parsing has finished
                        self._requires_grounding.append(subtasks.tasks[len(subtasks) - 1])
                i += 1
        return subtasks
    
    def _scan_tokens(self, file_path):
        return super(HDDLParser, self)._scan_tokens(file_path)
