from Internal_Representation.modifier import Modifier
from Internal_Representation.parameter import Parameter


class Subtasks:
    class Subtask:
        def __init__(self, task, parameters=[]):
            self.task = task
            self.parameters = parameters

        def get_name(self):
            return self.task.name

    def __init__(self):
        self.tasks = []
        self.labelled_tasks = {}

    def add_subtask(self, label, modifier, parameters):
        assert type(label) == str or label is None
        assert isinstance(modifier, Modifier) or type(modifier) == str
        assert type(parameters) == list
        for p in parameters:
            assert type(p) == Parameter
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