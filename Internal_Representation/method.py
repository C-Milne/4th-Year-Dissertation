from Internal_Representation.subtasks import Subtasks
from Internal_Representation.modifier import Modifier


class Method(Modifier):
    def __init__(self, name, parameters, preconditions: Modifier.Precondition, task: dict, subtasks, constraints):
        """
        :param name:
        :param parameters:
        :param preconditions:
        :param task: {'task': Task, 'params': }
        :param subtasks:
        :param constraints:
        """
        super().__init__(name, parameters, preconditions)
        assert type(task) == dict and len(task.keys()) == 2 and "task" in task.keys() and "params" in task.keys()
        self.task = task
        assert type(subtasks) == Subtasks or subtasks is None
        self.subtasks = subtasks
        assert type(constraints) == Modifier.Precondition or constraints is None
        self.constraints = constraints

    def evaluate_preconditions(self, model, param_dict, problem) -> bool:
        """:params  - model : proposed model
                    - param_dict : dictionary of parameters
                    - problem : problem being solved
        :returns    - True : if method can be run on the given model with given parameters
                    - False : Otherwise"""
        result = super().evaluate_preconditions(model, param_dict, problem)
        if self.constraints is not None and result:
            result = self._evaluate_constraints(param_dict, model, problem)
        return result

    def _evaluate_constraints(self, param_dict: dict, model, problem):
        """:parameter param_dict : map of parameters - {?x: Object[banjo], ?y: Object[kiwi]}."""
        if self.constraints is None:
            return True
        result = self.constraints.evaluate(param_dict, model, problem)
        return result

    def get_constraints(self):
        return self.constraints

    def get_subtasks(self):
        return self.subtasks

    def get_task_dict(self):
        return self.task
