from Internal_Representation.modifier import Modifier
from Internal_Representation.reg_parameter import RegParameter
from Internal_Representation.Object import Object
from Internal_Representation.list_parameter import ListParameter
from Internal_Representation.parameter import Parameter


class Subtasks:
    class Subtask:
        def __init__(self, task, parameters=[]):
            try:
                assert isinstance(task, Modifier) or type(task) == str
            except:
                raise TypeError
            self.task = task
            assert type(parameters) == list or type(parameters) == ListParameter
            if type(parameters) == list:
                for p in parameters:
                    assert isinstance(p, Parameter)
            self.parameters = parameters
            self.given_params = {}

        def get_name(self):
            return self.task.name

        def add_given_parameters(self, params: dict[Object]):
            assert type(params) == dict
            if not (len(params.keys()) == 1 and type(params[list(params.keys())[0]]) == ListParameter):
                for i in params:
                    assert type(params[i]) == Object or type(params[i]) == ListParameter
            self.given_params = params

        def evaluate_preconditions(self, model, params, problem):
            if self.task.preconditions is None:
                return True
            else:
                return self.task.preconditions.evaluate(params, model, problem)

    def __init__(self):
        self.tasks = []
        self.labelled_tasks = {}

    def add_subtask(self, label: str, modifier, parameters: list, decorator: str = None):
        assert type(label) == str or label is None
        assert isinstance(modifier, Modifier) or type(modifier) == str
        assert type(parameters) == list or type(parameters) == ListParameter
        if type(parameters) == list:
            for p in parameters:
                assert isinstance(p, Parameter)
        subtask_to_add = self.Subtask(modifier, parameters)
        if label is not None:
            self.labelled_tasks[label] = subtask_to_add
        self.tasks.append(subtask_to_add)

    def order_subtasks(self, orderings):
        ordered_subtasks = []
        for i in orderings:
            if i == "and":
                continue
            assert type(i) == list
            operator = i[0]  # < or >
            taskA = self.labelled_tasks[i[1]]
            taskB = self.labelled_tasks[i[2]]
            if operator == ">":
                taskA, taskB = taskB, taskA

            # TaskA comes before taskB
            if not taskA in ordered_subtasks and not taskB in ordered_subtasks:
                ordered_subtasks.append(taskA)
                ordered_subtasks.append(taskB)
            elif not taskA in ordered_subtasks:
                # Get index of taskB
                taskB_index = ordered_subtasks.index(taskB)
                ordered_subtasks.insert(taskB_index, taskA)
            else:
                ordered_subtasks.append(taskB)
        self.tasks = ordered_subtasks

    def get_tasks(self):
        return self.tasks

    def __len__(self):
        return len(self.tasks)
