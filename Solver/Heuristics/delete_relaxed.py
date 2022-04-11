import copy
import sys
import re
from Solver.Heuristics.Heuristic import Heuristic
from Solver.Parameter_Selection.All_Parameters import AllParameters
Task = sys.modules['Internal_Representation.task'].Task
Method = sys.modules['Internal_Representation.method'].Method
Action = sys.modules['Internal_Representation.action'].Action
Subtasks = sys.modules['Internal_Representation.subtasks'].Subtasks
Subtask = sys.modules['Internal_Representation.subtasks'].Subtasks.Subtask
Model = sys.modules['Solver.model'].Model
Domain = sys.modules['Internal_Representation.domain'].Domain
Problem = sys.modules['Internal_Representation.problem'].Problem
State = sys.modules['Internal_Representation.state'].State
Predicate = sys.modules['Internal_Representation.predicate'].Predicate
RegParameter = sys.modules['Internal_Representation.reg_parameter'].RegParameter
OperatorCondition = sys.modules['Internal_Representation.conditions'].OperatorCondition
PredicateCondition = sys.modules['Internal_Representation.conditions'].PredicateCondition
Precondition = sys.modules['Internal_Representation.precondition'].Precondition
Condition = sys.modules['Internal_Representation.conditions'].Condition
Object = sys.modules['Internal_Representation.Object'].Object
ProblemPredicate = sys.modules['Internal_Representation.problem_predicate'].ProblemPredicate


class AltOperatorCondition(OperatorCondition):
    def __init__(self, operator: str, pred: Predicate):
        super().__init__(operator)
        self.pred = pred

    def evaluate(self, param_dict: dict, search_model, problem) -> bool:
        children_eval = []
        if len(self.children) > 0 and (self.operator == "and" or self.operator == "or"):
            children_eval = [x.evaluate(param_dict, search_model, problem) for x in self.children]
        if self.operator == "and":
            for i in children_eval:
                if i != True:
                    return False
            return True
        elif self.operator == "or":
            for i in children_eval:
                if i == True:
                    return True
            return False
        elif self.operator == "not":
            assert len(self.children) == 1
            """Changes go here"""
            # In the alt state not conditions are stored in the state under new predicates
            # Such as (not-have, kiwi)
            p_list = []
            for i in self.children[0].parameter_name:
                p_list.append(param_dict[i])

            res = search_model.current_state.check_if_predicate_value_exists(self.pred, p_list)
            if res:
                return res
            else:
                # Try normal not evaluation
                res = self.children[0].evaluate(param_dict, search_model, problem)
                if res is True:
                    return False
                else:
                    # Add this new predicate to state
                    search_model.current_state.add_element(ProblemPredicate(self.pred, p_list))
                    return True
        elif self.operator == "=":
            v = children_eval[0]
            for i in children_eval[1:]:
                if v != i:
                    return False
            return True


class AltPredicateCondition(PredicateCondition):
    def __init__(self, pred: Predicate, parameter_names: list):
        super().__init__(pred, parameter_names)

    def evaluate(self, param_dict: dict, search_model, problem) -> bool:
        if self.pred.name != "U":
            p_list = []
            for i in self.parameter_name:
                p_list.append(param_dict[i])

            return search_model.current_state.check_if_predicate_value_exists(self.pred, p_list)
        else:
            if len(self.parameter_name) == 1 and type(self.parameter_name[0]) == str and self.parameter_name[0][0] != "?":
                # Change this to an object
                self.parameter_name = [problem.get_object(self.parameter_name[0])]
            return search_model.current_state.check_if_predicate_value_exists(self.pred, self.parameter_name)


class AltPrecondition(Precondition):
    def __init__(self, conditions: str):
        super().__init__(conditions)

    def add_operator_condition(self, operator: str, parent: Condition, pred: Predicate = None) -> AltOperatorCondition:
        assert type(operator) == str
        assert isinstance(parent, Condition) or parent is None
        assert isinstance(pred, Predicate) or pred is None

        con = AltOperatorCondition(operator, pred)
        self._final_condition_addition_checks(con, parent)
        return con

    def add_predicate_condition(self, pred: Predicate, parameter_names: list, parent: Condition) -> PredicateCondition:
        assert isinstance(parent, Condition) or parent is None
        con = AltPredicateCondition(pred, parameter_names)
        self._final_condition_addition_checks(con, parent)
        return con


class DeleteRelaxed(Heuristic):

    def __init__(self, domain, problem, solver, search_models):
        super().__init__(domain, problem, solver, search_models)
        self.low_target = True
        self.seen_states = {}

        self.alt_domain = None
        self.alt_problem = None
        self.parameter_selector = AllParameters(self.solver)
        self.model_rankings = {}

    def ranking(self, model: Model) -> float:
        # Create duplicate state
        alt_state = State.reproduce(model.current_state)

        if len(model.operations_taken) == 0 or type(model.operations_taken[-1].action) == Action:
            prev_action = True
        else:
            prev_action = False

        if model.model_number not in self.model_rankings and model.parent_model_number is not None and \
                model.parent_model_number in self.model_rankings:
            self.model_rankings[model.model_number] = copy.deepcopy(self.model_rankings[model.parent_model_number])

        if model.model_number not in self.model_rankings or prev_action:
            # Create list with all possible actions and methods
            modifiers = []
            for a in self.alt_domain.get_all_actions():
                modifiers.append(a)
            for m in self.alt_domain.get_all_methods():
                modifiers.append(m)

            # Choose target('s)
            targets = self._get_target_tasks(model)
            if type(targets) == int:
                return targets
            res = self._calculate_distance(self.solver.reproduce_model(model), modifiers, alt_state, targets)
            self.model_rankings[model.model_number] = res
            return res
        else:
            return self.model_rankings[model.model_number]

    def _get_target_tasks(self, model):
        targets = []
        next_mod = model.search_modifiers[0].task
        if type(next_mod) != Task and model.ranking is not None:
            return model.ranking
        elif type(next_mod) != Task:
            i = -1
            op = model.operations_taken[i]
            op_task = op.action
            while type(op_task) != Task:
                i -= 1
                op = model.operations_taken[i]
                op_task = op.action
            assert type(op_task) == Task
            targets.append("U-" + op_task.name +
                           self._concat_param_object_names([op.parameters_used[x] for x in op.parameters_used]))
        else:
            # We have all tasks
            pass

        for m in model.search_modifiers:
            if type(m.task) == Task:
                targets.append("U-" + m.task.name + self._concat_param_object_names([m.given_params[x] for x in m.given_params]))
        for m in model.waiting_subtasks:
            if type(m) == Task:
                targets.append("U-" + m.task.name + self._concat_param_object_names([m.given_params[x] for x in m.given_params]))
        return targets

    def _concat_param_object_names(self, list_obs: list):
        names = ""
        for o in list_obs:
            names += "-" + o.name
        return names

    def _get_objects_from_alt_modifier_name(self, name: str, names_only: bool = False) -> list:
        obs = []
        occurrences = [m.start() for m in re.finditer('-', name)]
        while occurrences:
            start = occurrences.pop(0) + 1
            if occurrences:
                end = occurrences[0]
            else:
                end = len(name)
            if not names_only:
                obs.append(self.problem.get_object(name[start:end]))
            else:
                obs.append(name[start:end])
        return obs

    def _calculate_distance(self, model: Model, modifiers: list, alt_state: State, targets: list) -> int:
        model.current_state = alt_state
        iteration = 0
        while True:
            iteration += 1
            applicable_modifiers = []
            # Find all modifiers which can be applied
            for m in modifiers:
                given_params = {}
                obs = self._get_objects_from_alt_modifier_name(m.name)
                params = m.get_parameters()
                for i in range(len(params)):
                    given_params[params[i].name] = obs[i]
                if m.evaluate_preconditions(model, given_params, self.alt_problem):
                    applicable_modifiers.append((m, copy.copy(given_params)))

            # Add effects of these modifiers to alt_state
            for m in applicable_modifiers:
                given_params = m[1]
                m = m[0]
                if type(m) == Action:
                    for e in m.effects.effects:
                        if e.negated:
                            pred = self.alt_domain.get_predicate("not_" + e.predicate.name)
                            model.current_state.add_element(
                                ProblemPredicate(pred, [given_params[x] for x in e.parameters]))
                        else:
                            model.current_state.add_element(ProblemPredicate(e.predicate, [given_params[x] for x in e.parameters]))

                        # Add action name to state (U-actionName)
                        model.current_state.add_element(ProblemPredicate(
                            self.alt_domain.get_predicate("U"), [self.alt_problem.get_object(m.name)]))
                elif type(m) == Method:
                    # Check if name of task this method expands is already in state
                    ob_names = self._get_objects_from_alt_modifier_name(m.name, True)
                    task_name = m.task['task'].name

                    l = len(m.task['params'])
                    i = 0
                    for ob in ob_names:
                        if i >= l:
                            break
                        task_name += "-" + ob
                        i += 1

                    occurrences = model.current_state.get_indexes("U")
                    found = False
                    for o in occurrences:
                        prob_pred = model.current_state.get_element_index(o)
                        if prob_pred.objects[0].name == task_name:
                            found = True
                            break

                    # If not add name of task this method expands to state
                    if not found:
                        task_name_ob = self.alt_problem.get_object(task_name)
                        model.current_state.add_element(ProblemPredicate(
                            self.alt_domain.get_predicate("U"), [task_name_ob]))
                else:
                    raise TypeError
                # Remove modifiers from list
                del modifiers[modifiers.index(m)]

            # Check exit conditions
            if self._check_targets(model, targets):
                return iteration
            elif len(applicable_modifiers) == 0:
                return False

    def _check_targets(self, model: Model, targets: list) -> bool:
        occurrences = model.current_state.get_indexes("U")
        occurrences = [model.current_state.get_element_index(x) for x in occurrences]

        for t in targets:
            found = False
            for element in occurrences:
                if element.objects[0].name == t[2:]:
                    found = True
                    break
            if not found:
                return False
        return True

    def presolving_processing(self) -> None:
        self.alt_domain = Domain(None)
        self.alt_problem = Problem(self.alt_domain)
        self.alt_domain.add_problem(self.alt_problem)
        # Create new domain
        self._generate_alt_domain()
        self._generate_alt_problem()

    def _generate_alt_domain(self):
        # Give alt domain types
        self.alt_domain.types = self.domain.types

        # Give alt domain predicates
        for p in self.domain.predicates:
            pred = self.domain.predicates[p]
            self.alt_domain.add_predicate(pred)
            self.alt_domain.add_predicate(Predicate("not_" + p, pred.parameters))
        self.alt_domain.add_predicate(Predicate("U", [RegParameter("?action")]))

        # Give alt domain actions
        for a in self.domain.get_all_actions():
            # Consider action with all possible parameters
            param_options = self.parameter_selector.get_potential_parameters(a, {}, None)
            for params in param_options:
                concat_param_names = ""
                for p in params:
                    concat_param_names += "-" + params[p].name
                alt_name = a.name + concat_param_names
                alt_precons = self._process_alt_preconditions(a.get_precondition().get_conditions())
                alt_effects = copy.deepcopy(a.get_effects())
                alt_a = Action(alt_name, a.get_parameters(), alt_precons, alt_effects)
                self.alt_domain.add_action(alt_a)

        # Give alt domain methods
        for m in self.domain.get_all_methods():
            # Consider action with all possible parameters
            param_options = self.parameter_selector.get_potential_parameters(m, {}, None)
            for params in param_options:
                concat_param_names = ""
                for p in params:
                    concat_param_names += "-" + params[p].name
                alt_name = m.name + concat_param_names
                alt_precons = self._process_alt_preconditions(m.get_precondition().get_conditions())

                alt_subtasks = Subtasks(m.subtasks.ordered)

                for s in m.subtasks.tasks:
                    alt_subtasks.add_subtask(None, s.task, [x for x in s.parameters])

                head = alt_precons.head
                if not(type(head) == AltOperatorCondition and head.operator == "and"):
                    raise NotImplementedError

                for s in alt_subtasks.tasks:
                    alt_subt_name = copy.deepcopy(s.task.name)
                    for p in s.parameters:
                        alt_subt_name += "-" + params[p.name].name
                    alt_precons.add_predicate_condition(self.alt_domain.get_predicate("U"), [alt_subt_name], head)

                alt_m = Method(alt_name, m.get_parameters(), alt_precons, m.get_task_dict(), alt_subtasks, m.get_constraints())
                self.alt_domain.methods[alt_m.name] = alt_m

    def _process_alt_preconditions(self, params, mod=None):
        def __parse_conditions(parameters, parent=None):
            if type(parameters) == list and len(parameters) == 1 and type(parameters[0]) == list:
                parameters = parameters[0]

            if type(parameters) == list:
                i = 0
                l = len(parameters)
                while i < l:
                    p = parameters[i]
                    if type(p) == str:
                        if p == "and" or p == "or" or p == "not":
                            if p == "not":
                                pred_name = "not_" + parameters[i + 1][0]
                                pred = self.alt_domain.get_predicate(pred_name)
                                if pred is None:
                                    raise NameError("Predicate '{}' not found in alt_domain".format(pred_name))
                            else:
                                pred = None
                            cons = constraints.add_operator_condition(p, parent, pred)
                            __parse_conditions(parameters[i + 1:], cons)
                            return
                        elif p == "=":
                            cons = constraints.add_operator_condition(p, parent)
                            for v in parameters[i + 1:]:
                                __parse_conditions(v, cons)
                            return
                        elif len(parameters) > 1 and all([type(x) == str for x in parameters]):
                            # Here a type is given
                            # ['valuableorhazardous', '?collect_fees_instance_2_argument_0']
                            pred = self.domain.get_predicate(p)
                            if pred is None:
                                self.domain.add_predicate(Predicate(p, self._parse_parameters(parameters[1:])))
                                pred = self.domain.get_predicate(p)

                            pred_parameters = parameters[1:]
                            """Check if all of the parameters defined in pred_parameters are given from the task
                            (assuming we are parsing a methods precondition)"""
                            if given_params is None:
                                constraints.add_predicate_condition(pred, pred_parameters, parent)
                            else:
                                # Check if all predicate_params are in given_params
                                if all([x in given_params for x in pred_parameters]):
                                    if parent.operator == "not":
                                        parent.parent.children.remove(parent)
                                        operator_parent = constraints.add_given_params_operator_condition("not")
                                        constraints.add_given_params_predicate_condition(pred, pred_parameters,
                                                                                         operator_parent)
                                        parent = parent.parent
                                    else:
                                        constraints.add_given_params_predicate_condition(pred, pred_parameters, parent)
                                else:
                                    constraints.add_predicate_condition(pred, pred_parameters, parent)
                            i = l
                        elif len(parameters) == 1 and type(p) == str:
                            constraints.add_predicate_condition(self.domain.get_predicate(p), [], parent)
                            i = l
                        elif p == "forall":
                            if len(parameters) == 3:
                                selector = parameters[1]
                                satisfier = self._parse_precondition(parameters[2])
                            else:
                                selector = parameters[1] + [self._parse_precondition(['and'] + parameters[2])]
                                satisfier = self._parse_precondition(['and'] + parameters[3])
                            constraints.add_forall_condition(selector, satisfier.head, parent)
                            i += l
                        else:
                            raise TypeError("Unexpected token {}".format(p))
                    elif type(p) == list:
                        __parse_conditions(p, parent)
                    else:
                        raise TypeError("Unexpected type {}".format(type(p)))
                    i += 1
            elif type(parameters) == str:
                return constraints.add_variable_condition(parameters, parent)
            else:
                raise TypeError("Unexpected type {}".format(type(parameters)))

        constraints = AltPrecondition(params)
        if type(mod) == Method:
            given_params = [x.name for x in mod.task['params']]
        else:
            given_params = None
        given_mod = mod
        __parse_conditions(params)
        return constraints

    def _generate_alt_problem(self):
        self.alt_problem.initial_state = State.reproduce(self.problem.initial_state)

        # Get objects
        obs = self.problem.get_all_objects()
        for o in obs:
            self.alt_problem.add_object(obs[o])

        # Create objects for modifiers
        for a in self.alt_domain.actions:
            self.alt_problem.add_object(Object(a))

        for m in self.alt_domain.methods:
            self.alt_problem.add_object(Object(m))

        tasks = self.domain.get_all_tasks()
        for t in tasks:
            # Get all possible combinations of parameter for t
            param_options = self.parameter_selector.get_potential_parameters(tasks[t], {}, None)
            for params in param_options:
                concat_param_names = ""
                for p in params:
                    concat_param_names += "-" + params[p].name
                alt_name = t + concat_param_names
                self.alt_problem.add_object(Object(alt_name))

    def task_milestone(self, model) -> bool:
        num_tasks_remaining = str(len(model.waiting_subtasks))
        if num_tasks_remaining not in self.seen_states:
            self.seen_states[num_tasks_remaining] = [self.solver.reproduce_state(model.current_state)]
            return True
        else:
            reproduced_state = self.solver.reproduce_state(model.current_state)
            if reproduced_state not in self.seen_states[num_tasks_remaining]:
                self.seen_states[num_tasks_remaining].append(reproduced_state)
                return True
            else:
                return False
