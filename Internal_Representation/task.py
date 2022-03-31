from Internal_Representation.modifier import Modifier


class Task(Modifier):
    def __init__(self, name, parameters=[]):
        super().__init__(name, parameters)
        self.methods = []
        self.tasks = []

    def add_method(self, method):
        self.methods.append(method)

    def add_task(self, t):
        self.tasks.append(t)

    def evaluate_preconditions(self, *args):
        return True
