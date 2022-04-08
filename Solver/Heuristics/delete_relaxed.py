import copy
import sys
from Solver.Heuristics.Heuristic import Heuristic
from Solver.Parameter_Selection.All_Parameters import AllParameters
Task = sys.modules['Internal_Representation.task'].Task
Method = sys.modules['Internal_Representation.method'].Method
Action = sys.modules['Internal_Representation.action'].Action
Subtask = sys.modules['Internal_Representation.subtasks'].Subtasks.Subtask
Model = sys.modules['Solver.model'].Model
Domain = sys.modules['Internal_Representation.domain'].Domain
Problem = sys.modules['Internal_Representation.problem'].Problem
State = sys.modules['Internal_Representation.state'].State
Predicate = sys.modules['Internal_Representation.predicate'].Predicate
RegParameter = sys.modules['Internal_Representation.reg_parameter'].RegParameter
OperatorCondition = sys.modules['Internal_Representation.conditions'].OperatorCondition
Precondition = sys.modules['Internal_Representation.precondition'].Precondition
Condition = sys.modules['Internal_Representation.conditions'].Condition


class AltOperatorCondition(OperatorCondition):
    def __init__(self, operator: str):
        super().__init__(operator)

    def evaluate(self, param_dict: dict, search_model, problem) -> bool:
        children_eval = []
        if len(self.children) > 0:
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
            assert len(children_eval) == 1 and len(self.children) == 1
            """Changes go here"""
            raise NotImplementedError
        elif self.operator == "=":
            v = children_eval[0]
            for i in children_eval[1:]:
                if v != i:
                    return False
            return True


class AltPrecondition(Precondition):
    def __init__(self, conditions: str):
        super().__init__(conditions)

    def add_operator_condition(self, operator: str, parent: Condition) -> AltOperatorCondition:
        assert type(operator) == str
        assert isinstance(parent, Condition) or parent is None

        con = AltOperatorCondition(operator)
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

    def ranking(self, model: Model) -> float:
        print("here")

    def _calculate_distance(self, model: Model):
        # Create duplicate state
        print("Here")

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
            self.alt_domain.add_predicate(self.domain.predicates[p])
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
                alt_subtasks = copy.deepcopy(m.get_subtasks())

                head = alt_precons.head
                if not(type(head) == AltOperatorCondition and head.operator == "and"):
                    raise NotImplementedError

                for s in alt_subtasks.tasks:
                    alt_subt_name = copy.deepcopy(s.task.name)
                    for p in s.parameters:
                        alt_subt_name += "-" + params[p.name].name
                    alt_precons.add_predicate_condition(self.alt_domain.get_predicate("U"), [alt_subt_name], head)

                alt_m = Method(alt_name, m.get_parameters(), alt_precons, m.get_task_dict(), alt_subtasks, m.get_constraints())
                self.alt_domain.add_method(alt_m)

    def _process_alt_preconditions(self, params, mod = None):
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
                            cons = constraints.add_operator_condition(p, parent)
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