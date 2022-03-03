from Internal_Representation.precondition import Precondition
from Internal_Representation.subtasks import Subtasks
from Internal_Representation.modifier import Modifier
from Internal_Representation.task import Task


class Method(Modifier):
    def __init__(self, name, parameters, preconditions, task, subtasks):
        super().__init__(name, parameters, preconditions)
        assert type(task) == dict and len(task.keys()) == 2 and "task" in task.keys() and "params" in task.keys()
        self.task = task
        assert type(subtasks) == Subtasks or subtasks is None
        self.subtasks = subtasks

        self.requirements = {}
        super(Method, self)._prepare_requirements()

    def evaluate_preconditions(self, model, param_dict):
        """:params  - model : proposed model
                    - params : list of parameters
        :returns    - True : if method can be run on the given model with given parameters
                    - False : Otherwise"""
        # Evaluate preconditions
        if self.preconditions is None:
            return True
        assert type(self.preconditions) == Precondition
        return self.preconditions.evaluate(model, param_dict)

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
