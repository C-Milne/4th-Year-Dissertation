from Internal_Representation.task import Task


class Subtasks:
    """TODO: Use this class in methods"""
    class Subtask:
        def __init__(self, task, parameters=[]):
            self.task = task
            self.parameters = parameters

        def get_name(self):
            return self.task.name

    def __init__(self, list_of_tasks, domain):
        assert type(list_of_tasks) == list
        self.tasks = []
        self.labelled_tasks = {}
        for i in list_of_tasks:
            if i == "and":
                continue
            if type(i) == list and len(i) > 1 and type(i[1]) == list:
                label = i[0]

                modifier = domain.get_modifier(i[1][0])

                if len(i[1]) == 1:
                    subtask = self.Subtask(modifier)
                else:
                    subtask = self.Subtask(modifier, i[1][1:])
                self.labelled_tasks[label] = subtask
            else:
                self.tasks.append(i)

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
