import sys
"""Import already imported modules from sys.modules"""
Modifier = sys.modules["Internal_Representation.modifier"].Modifier
Method = sys.modules["Internal_Representation.method"].Method
Action = sys.modules["Internal_Representation.action"].Action
Task = sys.modules["Internal_Representation.task"].Task
Model = sys.modules["Solver.model"].Model
Object = sys.modules["Internal_Representation.Object"].Object
ListParameter = sys.modules["Internal_Representation.list_parameter"].ListParameter
Type = sys.modules["Internal_Representation.Type"].Type


class ParameterSelector:
    def __init__(self, solver):
        self.solver = solver

    def get_potential_parameters(self, modifier: Modifier, parameters: dict, search_model: Model) -> list:
        """
        :param modifier: Task / Method / Action that is being executed
        :param parameters: The parameters that are already selected - {'param1': Object ...}
        :param search_model: Search model being expanded
        :return: list of dictionaries containing options of parameters - [{'param1': Object, 'param2': Object ...}, ...]
        """
        raise NotImplementedError

    def compare_parameters(self, method: Method, parameters: dict):
        """ Compares if all the parameters required for a method are given
        :parameter  - method : Method
        :parameter  - parameters : {'?objective1': Object, '?mode': Object}
        :returns    - [True] : if parameters match what is required by method
        :returns    - [False, missing_params] : otherwise. missing_params = ["name1", "name2" ... ]
        """
        assert isinstance(method, Modifier)
        assert type(parameters) == dict
        for p in parameters:
            assert type(parameters[p]) == Object or type(parameters[p]) == ListParameter

        missing_params = []
        for p in method.parameters:
            # Check if a parameter corresponding to p is in parameters dictionary
            if not p.name in parameters:
                missing_params.append(p.name)
                continue
            if not self.check_satisfies_type(p.type, parameters[p.name]):
                return [False, False]
        if len(missing_params) == 0:
            return [True]
        return [False, missing_params]

    def check_satisfies_type(self, required_type: Type, object_to_check: Object):
        def __check_type(req_t, t):
            if t == req_t:
                return True
            for i in t.parents:
                if __check_type(req_t, i):
                    return True
            return False

        if required_type is None:
            return True
        ob_t = object_to_check.type
        res = __check_type(required_type, ob_t)
        return res
