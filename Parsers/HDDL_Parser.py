from Internal_Representation.action import Action
from Internal_Representation.method import Method
from Internal_Representation.predicate import Predicate
from Internal_Representation.task import Task
from Internal_Representation.Type import Type
from Internal_Representation.Object import Object
from Parsers.parser import Parser
from Internal_Representation.reg_parameter import RegParameter
from Internal_Representation.effects import Effects
from Internal_Representation.subtasks import Subtasks
from Internal_Representation.modifier import Modifier
from Internal_Representation.problem_predicate import ProblemPredicate
from Internal_Representation.precondition import Precondition


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
                    self._parse_constraint(group)
                elif lead == ":constants":
                    self._parse_constant(group)
                else:
                    raise AttributeError("Unknown tag; {}".format(lead))
        self._post_domain_parsing_grounding()

    def parse_problem(self, problem_path):
        self.problem_path = problem_path
        tokens = self._scan_tokens(problem_path)
        if type(tokens) is list and tokens.pop(0) == 'define':
            while tokens:
                group = tokens.pop(0)
                lead = group.pop(0)

                if lead == "problem":
                    self._set_problem_name(group)
                elif lead == ":domain":
                    self._check_domain_name(group)
                elif lead == ":objects":
                    self._parse_objects(group)
                elif lead == ":init":
                    self._parse_initial_state(group)
                elif lead == ":goal":
                    self._parse_goal_state(group)
                elif lead == ":htn":
                    self._parse_htn_tag(group)
        self._post_problem_parsing_grounding()

    """Methods for parsing domains"""
    def _parse_type(self, params):
        def _add_types_to_domain(t=None):
            for o in new_types:
                self.domain.add_type(Type(o, t))

        i = 0
        l = len(params)
        new_types = []
        while i < l:
            if params[i] != "-":
                new_types.append(params[i])
                i += 1
            else:
                parent_type = self.domain.get_type(params[i + 1])

                if parent_type is False:
                    self.domain.add_type(Type(params[i + 1]))
                    parent_type = self.domain.get_type(params[i + 1])

                _add_types_to_domain(parent_type)
                new_types = []
                i += 2
        _add_types_to_domain()

    def _parse_predicates(self, params):
        for i in params:
            predicate_name = i[0]
            if len(i) > 1:
                parameter_list = self._parse_parameters(i[1:])
                self.domain.add_predicate(Predicate(predicate_name, parameter_list))
            else:
                self.domain.add_predicate(Predicate(i[0]))

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
                return self._parse_effects(params[1:])
            elif type(params[i]) == str and params[i] != "not":
                predicate_name, parameters = __extract_effect_values(params)
                i += len(params)
            elif type(params[i]) == list:
                # [['not', ['at', '?x', '?y']], ['at', '?x', '?z']]
                if params[i][0] == "not":
                    negated = True
                    assert len(params[i]) == 2 and type(params[i][1]) == list
                    predicate_name, parameters = __extract_effect_values(params[i][1])
                else:
                    for v in params[i]:
                        assert type(v) == str
                    predicate_name, parameters = __extract_effect_values(params[i])
            else:
                # ['not', ['have', '?a']]
                if params[i] == "not":
                    negated = True
                    assert type(params[i + 1]) == list
                    predicate_name, parameters = __extract_effect_values(params[i + 1])
                    i += 1
                else:
                    predicate_name, parameters = __extract_effect_values(params[i])

            predicate = self.domain.get_predicate(predicate_name)
            effects.add_effect(predicate, parameters, negated)
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
        method_name, parameters, precon, task, subtasks, constraints = None, None, None, None, None, None
        while i < l:
            if i == 0:
                if type(params[i]) != str or params[i][0] == ":":
                    raise SyntaxError("Error with Method name. Must be a string not beginning with ':'."
                         "\nPlease check your domain file.")
                method_name = params[i]
            elif params[i] == ":parameters":
                parameters = self._parse_parameters(params[i + 1])
                i += 1
            elif params[i] == ":precondition":
                precon = self._parse_precondition(params[i + 1])
                i += 1
            elif params[i] == ":constraints":
                constraints = self._parse_precondition(params[i + 1])
                i += 1
            elif params[i] == ":task":
                task_ob = self.domain.get_task(params[i + 1][0])
                if task_ob is None:
                    raise KeyError("Task 'swap' is not defined. Please check your domain file.")
                elif len(params[i + 1]) == 1:
                    task = {"task": task_ob, "params": []}
                else:
                    task = {"task": task_ob, "params": self._parse_parameters(params[i + 1][1:])}
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
        return Method(method_name, parameters, precon, task, subtasks, constraints)

    def _parse_constant(self, params):
        def __add_constants_to_problem(t=None):
            for c in new_constants:
                self.problem.add_object(Object(c, t))

        i = 0
        l = len(params)
        new_constants = []
        while i < l:
            v = params[i]
            if v == "-":
                v = params[i + 1]
                const_type = self.domain.get_type(v)
                if const_type is None or const_type == False:
                    raise TypeError("Type {} not found when parsing constants. Please check your domain file.".format(v))
                __add_constants_to_problem(const_type)
                new_constants = []
                i += 1
            else:
                new_constants.append(v)
            i += 1
        __add_constants_to_problem()
        new_constants = []

    def _post_domain_parsing_grounding(self):
        for item in self._requires_grounding:
            if type(item) == Subtasks.Subtask:
                # Make sure item.task is a modifier and not a string
                if type(item.task) != Modifier and type(item.task) == str:
                    retrieved = self.domain.get_modifier(item.task)
                    if not isinstance(retrieved, Modifier):
                        raise TypeError("No valid modifier found for {}".format(item.task))
                    item.task = retrieved
        self._requires_grounding = []

    """Methods for parsing problems"""
    def _set_problem_name(self, params):
        if type(params) == list and len(params) == 1 and type(params[0]) == str:
            params = params[0]
        elif type(params) == str:
            pass
        else:
            raise TypeError("Given value must be a string or a list with one string inside. Given {}".format(params))
        assert type(params) == str
        self.problem.set_name(params)

    def _check_domain_name(self, name):
        """Returns True - if param: name is equal to self.domain_name"""
        if type(name) == list:
            name = name[0]
        if name == self.domain_name:
            return True
        else:
            raise NameError("Domain specified in problem file {} ({}). Does not match domain specified in {} ({})"
                            .format(self.problem_path, name, self.domain_path, self.domain_name))

    def _parse_objects(self, params):
        def _add_objects_to_problem(t=None):
            for o in new_obs:
                self.problem.add_object(Object(o, t))
        i = 0
        l = len(params)
        new_obs = []
        while i < l:
            if params[i] != "-":
                new_obs.append(params[i])
                i += 1
            else:
                obs_type = self.domain.get_type(params[i + 1])
                _add_objects_to_problem(obs_type)
                new_obs = []
                i += 2
        _add_objects_to_problem()

    def _parse_initial_state(self, params):
        for i in params:
            # Create ProblemPredicate
            obs = [self.problem.get_object(x) for x in i[1:]]
            self.problem.add_to_initial_state(ProblemPredicate(self.domain.get_predicate(i[0]), obs))

    def _parse_htn_tag(self, params):
        while params:
            lead = params.pop(0)

            if lead == ":subtasks" or lead == ":ordered-subtasks" or lead == ":tasks" or lead == ":ordered-tasks":
                subtasks = self._parse_subtasks(params.pop(0))
                self.problem.add_subtasks(subtasks)
                self._requires_grounding.append(subtasks)
            elif lead == ":parameters":
                if params.pop(0) != []:
                    raise NotImplementedError
            elif lead == ":ordering":
                self.problem.order_subtasks(params.pop(0))
            else:
                raise TypeError("Unknown keyword {}".format(lead))

    def _parse_goal_state(self, params):
        if type(params) == list and len(params) == 1 and type(params[0]) == list and len(params[0]) > 1:
            params = params[0]
        cons = self._parse_precondition(params)
        self.problem.add_goal_conditions(cons)
    
    def _scan_tokens(self, file_path):
        return super(HDDLParser, self)._scan_tokens(file_path)
