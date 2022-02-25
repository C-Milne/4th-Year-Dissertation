from Internal_Representation.parameter import Parameter
from Internal_Representation.modifier import Modifier


class Task(Modifier):
    def __init__(self, name, parameters=[]):
        super().__init__(name, parameters)
        self.methods = []

    def add_method(self, method):
        self.methods.append(method)

    def compare_params_soft(self, params):
        """Check the parameter names given with the ones on record
        This method does not check parameter type, only name. For method that checks type as well, see compare_params()
        :returns    - True : if all parameters match
                    - False : otherwise"""
        if type(params) == tuple and len(params) == 1:
            params = params[0]

        if len(params) == len(self.parameters):
            i = 0
            l = len(params)
            while i < l:
                i += 1
        else:
            return False

        for p in params:
            found = False
            for p2 in self.parameters:
                if p == p2:
                    found = True
            if not found:
                return False
        return True

    def compare_params(self):
        """TODO : Implement this"""
        """Check the parameter names given with the ones on record
                This method checks name and type. For method that only checks name, see compare_params_soft()
                :returns    - True : if all parameters match
                            - False : otherwise"""
        pass

    def get_parameter_names(self):
        if len(self.parameters) != len(self.parameter_names):
            self.__collect_parameter_names()
        return self.parameter_names

    def __collect_parameter_names(self):
        self.parameter_names = []
        for p in self.parameters:
            self.parameter_names.append(p.name)

    def get_number_parameters(self):
        return len(self.parameters)

    def evaluate_preconditions(self, *args):
        return True