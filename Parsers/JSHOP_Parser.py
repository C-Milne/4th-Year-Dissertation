from Parsers.parser import Parser
from Internal_Representation.task import Task
from Internal_Representation.method import Method
from Internal_Representation.action import Action
from Internal_Representation.effects import Effects
from Internal_Representation.predicate import Predicate
from Internal_Representation.problem_predicate import ProblemPredicate
from Internal_Representation.Object import Object
from Internal_Representation.reg_parameter import RegParameter
from Internal_Representation.list_parameter import ListParameter
from Internal_Representation.subtasks import Subtasks
from Internal_Representation.derived_predicate import DerivedPredicate


class JSHOPParser(Parser):

    method_counter = 0

    def __init__(self, domain, problem):
        super().__init__(domain, problem)

    def parse_domain(self, domain_path):
        self.domain_path = domain_path
        tokens = self._scan_tokens(domain_path)
        if type(tokens) is list:
            while tokens:
                group = tokens.pop(0)
                if group == "defdomain":
                    self.domain_name = tokens.pop(0)
                else:
                    while len(group) > 0:
                        section = group.pop(0)
                        lead = section.pop(0)

                        if lead == ":operator":
                            """
                            (:operator (Action Name and parameters) (Deletions) (Additions)) - 
                            This is obviously not correct for this example
                            
                            Perhaps (:operator (Action Name and parameters) (precondition) (Deletions) (Additions))??
                            
                            (:operator (!pickup ?a) () () ((have ?a)))
                            (:operator (!drop ?a) ((have ?a)) ((have ?a)) ())
                            """
                            self._parse_action(section)
                        elif lead == ":method":
                            """The format for a method is as follows:
                            (:method (swap ?x ?y)       - this is task name and parameters
                            ((have ?x) (not (have ?y))) - this is preconditions for method1
                            ((!drop ?x) (!pickup ?y))   - this is subtasks for method1
                            ((have ?y) (not (have ?x))) - this is preconditions for method2
                            ((!drop ?y) (!pickup ?x)))  - this is subtasks for method2
                            """
                            self._parse_method(section)
                        elif lead == ":-":
                            """State axioms
                            (need-to-move ?x) - This is true if any of the following are true
                            ((on ?x ?y) (goal (on ?x ?z)) (not (same ?y ?z)))
                            ((on-table ?x) (goal (on ?x ?z)))
                            ((on ?x ?y) (goal (on-table ?x)))
                            ((on ?x ?y) (goal (clear ?y)))
                            ((on ?x ?z) (goal (on ?y ?z)) (not (same ?x ?y)))
                            ((on ?x ?w) (need-to-move ?w))"""
                            self._parse_state_axiom(section)
                        else:
                            raise AttributeError("Unknown tag - {}".format(lead))

    def parse_problem(self, problem_path):
        self.problem_path = problem_path
        tokens = self._scan_tokens(problem_path)

        group = tokens.pop(0)
        assert group == "defproblem"
        tokens.pop(0)
        self.problem_name = tokens.pop(0)

        # Initial state
        self._parse_initial_state(tokens.pop(0))

        # Subtasks
        self._parse_execution_subtasks(tokens.pop(0))

        # Grounding
        self._post_problem_parsing_grounding()

    def _parse_type(self, *args):
        pass

    def _log_predicate(self, pred_name: str, parameters: list[str]) -> Predicate:
        assert type(pred_name) == str
        assert type(parameters) == list
        for p in parameters:
            try:
                assert type(p) == str
            except:
                raise TypeError
        # Check if predicate already exists
        res = self.domain.get_predicate(pred_name)
        if res is None:
            # Add predicate
            pred = Predicate(pred_name, self._parse_parameters(parameters))
            self.domain.add_predicate(pred)
            return pred
        return res

    def _log_object(self, ob_name: str) -> Object:
        assert type(ob_name) == str
        res = self.problem.get_object(ob_name)
        if res is None:
            ob = Object(ob_name)
            self.problem.add_object(ob)
            return ob
        return res

    def _parse_effects(self, params: list[list[str]], negated: bool, effects: Effects):
        """
        :param params: [['have', '?a'], [...], ...]
        :param negated: boolean
        :param effects: Effect object for the new effects to be added to
        :return:
        """
        for p in params:
            if type(p) == list:
                pred_name = p[0]
                if len(p) > 1:
                    parameters = p[1:]
                else:
                    parameters = []
                pred = self._log_predicate(pred_name, parameters)
                effects.add_effect(pred, parameters, negated)
            elif type(p) == str and p[0] == '?':
                effects.add_runtime_effect(p)
            else:
                raise NotImplementedError("Effect {} of type {}".format(p, type(p)))

    def _parse_action(self, params):
        """[['!pickup', '?a'], [], [], [['have', '?a']]]
        [['!drop', '?a'], [['have', '?a']], [['have', '?a']], []]
        (name and params) (preconditions) (deletions) (additions)
        """
        assert len(params) == 4 or len(params) == 5
        if len(params) == 5:
            cost = params[4]
            params = params[:4]

        assert len(params) == 4
        for p in params:
            assert type(p) == list

        action_name = params[0][0]
        if len(params[0]) > 1:
            parameters = self._parse_parameters(params[0][1:])
        else:
            parameters = []

        precons = self._parse_precondition(params[1])

        effects = Effects()
        self._parse_effects(params[2], True, effects)
        self._parse_effects(params[3], False, effects)
        self.domain.add_action(Action(action_name, parameters, precons, effects))

    def _parse_method(self, params):
        """[['swap', '?x', '?y'], [['have', '?x'], ['not', ['have', '?y']]], [['!drop', '?x'], ['!pickup', '?y']],
        [['have', '?y'], ['not', ['have', '?x']]], [['!drop', '?y'], ['!pickup', '?x']]]"""
        task_def = params.pop(0)
        assert len(params) % 2 == 0
        task = self._parse_task(task_def)
        parameters = task.parameters

        for i in range(int(len(params) / 2)):
            name, preconditions, subtasks, constraints = None, None, None, None
            name = "method" + str(self.method_counter)
            self.method_counter += 1

            j = i * 2
            preconditions = self._parse_precondition(params[j])
            subtasks = self._parse_subtasks(params[j + 1])
            self.domain.add_method(Method(name, parameters, preconditions, {'task': task, 'params': parameters}, subtasks, constraints))

    def _parse_task(self, params) -> Task:
        """['swap', '?x', '?y']"""
        i = 0
        l = len(params)
        task_name, parameters = None, []
        while i < l:
            if i == 0:
                task_name = params[i]
            else:
                parameters = self._parse_parameters(params[i:])
                break
            i += 1
        task = Task(task_name, parameters)

        # Check if task already exists with other parameters
        res = self.domain.get_task(task_name)
        if res is None:
            self.domain.add_task(task)
        else:
            assert type(res) == Task
            if res.tasks == []:
                new_task = Task(res.name)
                new_task.add_task(res)
                new_task.add_task(task)
                self.domain.add_task(new_task)
            else:
                res.add_task(task)
        return task

    def _parse_precondition(self, params: list):
        if params == 'nil':
            return super(JSHOPParser, self)._parse_precondition([])
        # Check for predicates which are not yet discovered
        for p in params:
            if type(p) == list:
                if type(p) == list and len(p) == 1 and type(p[0]) == list:
                    p = p[0]

                while len(p) == 2 and type(p[1]) == list:
                    p = p[1]

                if len(p) > 1:
                    self._log_predicate(p[0], p[1:])
                else:
                    self._log_predicate(p[0], [])

        if len(params) > 0:
            try:
                params.insert(0, 'and')
            except:
                raise TypeError
        return super(JSHOPParser, self)._parse_precondition(params)

    def _parse_state_axiom(self, params):
        pred_name = params[0][0]
        pred_params = params[0][1:]
        conditions = params[1:]

        derived_pred = DerivedPredicate(pred_name, self._parse_parameters(pred_params))

        for c in conditions:
            derived_pred.add_condition(self._parse_precondition(c))
        self.domain.add_derived_predicate(derived_pred)

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
                if len(p) == 3 and all([type(x) == str for x in p]) and p[0][0] == '?' and p[2][0] == '?' and p[1] == '.':
                    assert param_names == []
                    """['?goal', '.', '?goals']
                    At solve time we need to check ?goals is a list and pop the leading value and store it in ?goal"""
                    param_list.append(ListParameter(p[2], p[0]))
                else:
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
                if p != 'nil':
                    param_names.append(p)
            else:
                raise TypeError("Unexpected token {}".format(p))
            i += 1
        __add_t_param_list()
        return param_list

    def _parse_predicates(self, *args):
        pass

    def _parse_constraint(self, *args):
        pass

    def _post_domain_parsing_grounding(self, *args):
        pass

    def _set_problem_name(self, *args):
        pass

    def _check_domain_name(self, *args):
        pass

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
                task_label, task_modifier, task_parameters, decorator = None, None, None, None
                if params[i] == "and":
                    pass
                else:
                    if type(params[i]) == list and type(params[i][0]) == str and params[i][0].startswith('!!'):
                        # ['!!assert', ['goal', '?goal']]
                        section = params[i]
                        task_modifier = self.domain.get_modifier(section[0])
                        parameters = section[1:]

                        if type(parameters) == list and len(parameters) == 1 and type(parameters[0]) == list:
                            parameters = parameters[0]

                        if len(parameters) == 2 and parameters[0] == 'goal':
                            decorator = parameters[0]
                            parameters = parameters[1]

                        try:
                            assert all([type(x) == str for x in parameters])
                        except:
                            raise TypeError

                        if parameters[0] == "goal":
                            decorator = parameters[0]
                            parameters = parameters[1:]
                        task_parameters = self._parse_parameters(parameters)

                    # Check if there is a list within a list
                    elif len(params[i]) > 1 and type(params[i][1]) == list:
                        task_label = params[i][0]
                        task_modifier = params[i][1][0]
                        parameters = params[i][1][1:]

                        task_parameters = self._parse_parameters(parameters)
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
                    subtasks.add_subtask(task_label, task_modifier, task_parameters, decorator)

                    if type(task_modifier) == str:
                        # Mark this method for grounding after parsing has finished
                        self._requires_grounding.append(subtasks.tasks[len(subtasks) - 1])
                i += 1
        return subtasks

    def _parse_objects(self, *args):
        pass

    def _parse_initial_state(self, group):
        while len(group) > 0:
            section = group.pop(0)
            if len(section) > 1:
                obs = [self._log_object(x) for x in section[1:]]
            else:
                obs = []
            self.problem.add_to_initial_state(ProblemPredicate(self.domain.get_predicate(section[0]), obs))

    def _parse_execution_subtasks(self, group):
        sub_tasks = None
        while len(group) > 0:
            section = group.pop(0)
            subT = self._parse_subtasks(section)

            for param in subT.tasks[0].parameters:
                self._log_object(param.name)

            if sub_tasks is None:
                sub_tasks = subT
            else:
                sub_tasks.append(subT.tasks[0])
        self.problem.add_subtasks(sub_tasks)
        self._requires_grounding.append(sub_tasks)

    def _parse_goal_state(self, *args):
        pass

    def _parse_htn_tag(self, *args):
        pass

    def _parse_constant(self, *args):
        pass
