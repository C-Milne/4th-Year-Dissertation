from Internal_Representation.modifier import Modifier
from Internal_Representation.action import Action
from Internal_Representation.method import Method
from Internal_Representation.task import Task
from Internal_Representation.predicate import Predicate
from Internal_Representation.Type import Type


class Domain:
    def __init__(self, problem):
        self.actions = {}
        self.methods = {}
        self.tasks = {}
        self.types = {}
        self.predicates = {}
        self.problem = problem

    def add_action(self, action):
        assert type(action) == Action
        self.actions[action.name] = action

    def add_method(self, method):
        assert type(method) == Method
        self.methods[method.name] = method
        if not method.task is None:
            self._add_method_to_task(method, method.task['task'])

    def add_task(self, task):
        assert type(task) == Task
        self.tasks[task.name] = task

    def add_predicate(self, predicate):
        assert type(predicate) == Predicate
        self.predicates[predicate.name] = predicate

    def add_type(self, t):
        assert type(t) == Type
        self.types[t.name] = t

    def get_action(self, action_name):
        """Return an actions object
        :params     - action_name : name of object to be returned
        :returns    - action object : if can be found
                    - False : otherwise"""
        try:
            return self.actions[action_name]
        except Exception:
            # Could not find action
            pass
        return False

    def get_task(self, name):
        if name in self.tasks.keys():
            # Compare parameters given with parameters of task
            return self.tasks[name]
        return None

    def get_task_methods(self, task):
        """TODO : implement for type Task"""
        if type(task) == str:
            task = self.get_task(task)
        return task.methods

    def get_type(self, name):
        if name in self.types:
            return self.types[name]
        else:
            return False

    def get_method(self, method_name):
        if not method_name in self.methods.keys():
            return None
        return self.methods[method_name]

    def get_modifier(self, name):
        if name in self.methods.keys():
            return self.methods[name]
        elif name in self.tasks.keys():
            return self.tasks[name]
        elif name in self.actions.keys():
            return self.actions[name]
        else:
            return None

    def get_predicate(self, name):
        if not name in self.predicates.keys():
            return None
        return self.predicates[name]

    def name_assigned(self, str):
        """TODO : Test this with all components"""
        """:param   - str : string being checked
            :returns    - True : if str is already in use
                        - False : otherwise"""
        if str in self.methods.keys() or str in self.tasks.keys() or str in self.actions.keys():
            return True
        return False

    def add_problem(self, problem):
        self.problem = problem

    def _add_method_to_task(self, method, task):
        assert type(method) == Method
        assert type(task) == Task
        task.add_method(method)
