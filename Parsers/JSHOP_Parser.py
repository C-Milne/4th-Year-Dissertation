from Parsers.parser import Parser
from Internal_Representation.task import Task
from Internal_Representation.method import Method
from Internal_Representation.action import Action
from Internal_Representation.effects import Effects
from Internal_Representation.predicate import Predicate


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
                        else:
                            raise AttributeError("Unknown tag - {}".format(lead))

    def parse_problem(self, problem_path):
        self.problem_path = problem_path
        tokens = self._scan_tokens(problem_path)
        if type(tokens) is list:
            while tokens:
                group = tokens.pop(0)
                if group == "defproblem":
                    tokens.pop(0)
                    self.problem_name = tokens.pop(0)
                else:
                    section = group.pop(0)
                    print("here")

    def _parse_type(self, *args):
        pass

    def _log_predicate(self, pred_name: str, parameters: list[str]) -> Predicate:
        assert type(pred_name) == str
        assert type(parameters) == list
        for p in parameters:
            assert type(p) == str
        # Check if predicate already exists
        if self.domain.get_predicate(pred_name) is None:
            # Add predicate
            pred = Predicate(pred_name, self._parse_parameters(parameters))
            self.domain.add_predicate(pred)
            return pred
        return self.domain.get_predicate(pred_name)

    def _parse_effects(self, params: list[list[str]], negated: bool, effects: Effects):
        """
        :param params: [['have', '?a'], [...], ...]
        :param negated: boolean
        :param effects: Effect object for the new effects to be added to
        :return:
        """
        for p in params:
            pred_name = p[0]
            if len(p) > 1:
                parameters = p[1:]
            else:
                parameters = []
            pred = self._log_predicate(pred_name, parameters)
            effects.add_effect(pred, parameters, negated)

    def _parse_action(self, params):
        """[['!pickup', '?a'], [], [], [['have', '?a']]]
        [['!drop', '?a'], [['have', '?a']], [['have', '?a']], []]
        (name and params) (preconditions) (deletions) (additions)
        """
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
        self.domain.add_task(task)
        return task

    def _parse_precondition(self, params: list):
        if len(params) > 0:
            params.insert(0, 'and')
        return super(JSHOPParser, self)._parse_precondition(params)

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

    def _parse_objects(self, *args):
        pass

    def _parse_initial_state(self, *args):
        pass

    def _parse_goal_state(self, *args):
        pass

    def _parse_htn_tag(self, *args):
        pass

    def _parse_constant(self, *args):
        pass
