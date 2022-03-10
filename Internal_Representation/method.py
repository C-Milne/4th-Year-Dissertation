from Internal_Representation.precondition import Precondition
from Internal_Representation.subtasks import Subtasks
from Internal_Representation.modifier import Modifier
from Internal_Representation.constraints import Constraints


class Method(Modifier):
    def __init__(self, name, parameters, preconditions: Precondition, task: dict, subtasks, constraints):
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
        assert type(constraints) == Constraints or constraints is None
        self.constraints = constraints

        self.requirements = {}
        super(Method, self)._prepare_requirements()

    def evaluate_preconditions(self, model, param_dict):
        """:params  - model : proposed model
                    - param_dict : dictionary of parameters
        :returns    - True : if method can be run on the given model with given parameters
                    - False : Otherwise"""
        # Evaluate preconditions
        if self.preconditions is None:
            return True
        assert type(self.preconditions) == Precondition
        result = self.preconditions.evaluate(model, param_dict)
        if self.constraints is not None and result:
            result = self._evaluate_constraints(param_dict)
        return result

    def _evaluate_constraints(self, param_dict: dict):
        """:parameter param_dict : map of parameters - {?x: Object[banjo], ?y: Object[kiwi]}."""
        if self.constraints is None:
            return True
        result = self.constraints.evaluate(param_dict)
        return result

    def get_parameters(self):
        return self.parameters

    def get_number_parameters(self):
        return len(self.parameters)

    def get_precondition(self):
        return self.preconditions

    def get_name(self):
        if self.name is None:
            return 'Unknown'
        return self.name

    def get_constraints(self):
        return self.constraints
