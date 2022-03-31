from Solver.Heuristics.Heuristic import Heuristic
from Internal_Representation.problem_predicate import ProblemPredicate


class PredicateDistanceToGoal(Heuristic):
    def __init__(self, domain, problem, solver, search_models):
        super().__init__(domain, problem, solver, search_models)
        self.low_target = True
        self.seen_states = {}
        self.goal_cons = []

    def ranking(self, model) -> float:
        # Consider cost thus far
        cost_so_far = len(model.operations_taken) / 3

        # Consider distance to goal
        distance_to_goal = 0
        for i in self.goal_cons:
            if i not in model.current_state.elements:
                distance_to_goal += 5
        return cost_so_far + distance_to_goal

    def presolving_processing(self) -> None:
        for i in self.problem.goal_conditions.conditions:
            if type(i) == list:
                if len(i) == 1:
                    self.goal_cons.append(ProblemPredicate(self.domain.get_predicate(i[0], [])))
                else:
                    obs = [self.problem.get_object(x) for x in i[1:]]
                    self.goal_cons.append(ProblemPredicate(self.domain.get_predicate(i[0]), obs))

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
