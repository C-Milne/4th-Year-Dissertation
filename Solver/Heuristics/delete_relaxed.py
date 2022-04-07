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
OperatorConditon = sys.modules['Internal_Representation.conditions'].OperatorCondition


class DeleteRelaxed(Heuristic):

    def __init__(self, domain, problem, solver, search_models):
        super().__init__(domain, problem, solver, search_models)
        self.low_target = True
        self.seen_states = {}

        self.alt_domain = None
        self.alt_problem = None
        self.parameter_selector = AllParameters(self.solver)

    def ranking(self, model: Model) -> float:
        pass

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
                alt_precons = copy.deepcopy(a.get_precondition())
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
                alt_precons = copy.deepcopy(m.get_precondition())
                alt_subtasks = copy.deepcopy(m.get_subtasks())

                head = alt_precons.head
                if not(type(head) == OperatorConditon and head.operator == "and"):
                    raise NotImplementedError

                for s in alt_subtasks.tasks:
                    alt_subt_name = copy.deepcopy(s.task.name)
                    for p in s.parameters:
                        alt_subt_name += "-" + params[p.name].name
                    alt_precons.add_predicate_condition(self.alt_domain.get_predicate("U"), [alt_subt_name], head)

                alt_m = Method(alt_name, m.get_parameters(), alt_precons, m.get_task_dict(), alt_subtasks, m.get_constraints())
                self.alt_domain.add_method(alt_m)

    def _generate_alt_problem(self):
        pass

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