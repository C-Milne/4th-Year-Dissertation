from Internal_Representation.action import Action
from Internal_Representation.method import Method
from Internal_Representation.task import Task
from Internal_Representation.predicate import Predicate
from Internal_Representation.Type import Type


class Domain:
    def __init__(self):
        self.actions = {}
        self.methods = {}
        self.tasks = {}
        self.types = {}
        self.predicates = {}

    def add_action(self, action):
        assert type(action) == Action
        self.actions[action.name] = action

    def add_method(self, method):
        assert type(method) == Method
        self.methods[method.name] = method

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

    def get_task(self, name, *args):
        if name in self.tasks.keys():
            # Compare parameters given with parameters of task
            task = self.tasks[name]
            if len(args) > 0:
                if task.compare_params_soft(args):
                    return task
                else:
                    raise SyntaxError("Parameters Given for Task {} ({}), Do Not Match Parameters on Record ({})"
                                      .format(name, args[0], task.get_parameter_names()))
            else:
                # No parameters given
                if len(task.parameters) == 0:
                    return task
                else:
                    raise SyntaxError("Could not find Task {} with no Parameters.".format(name))

    def get_task_methods(self, task):
        """TODO : implement for type Task"""
        if type(task) == str:
            task = self.get_task(task)
        else:
            raise NotImplementedError("This functionality is not implemented yet")
        return task.methods

    def get_type(self, name):
        if name in self.types:
            return self.types[name]
        else:
            return False

    def name_assigned(self, str):
        """:param   - str : string being checked
            :returns    - True : if str is already in use
                        - False : otherwise"""
        if str in self.methods.keys() or str in self.tasks.keys() or str in self.actions.keys():
            return True
        return False
