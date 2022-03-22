import sys
from Solver.Parameter_Selection.ParameterSelector import ParameterSelector
"""Import already imported modules from sys.modules"""
Modifier = sys.modules["Internal_Representation.modifier"].Modifier
Method = sys.modules["Internal_Representation.method"].Method
Action = sys.modules["Internal_Representation.action"].Action
Task = sys.modules["Internal_Representation.task"].Task
Model = sys.modules["Solver.model"].Model
Object = sys.modules["Internal_Representation.Object"].Object
ListParameter = sys.modules["Internal_Representation.list_parameter"].ListParameter
Type = sys.modules["Internal_Representation.Type"].Type

class AllParameters(ParameterSelector):
    def __init__(self):
        super().__init__()

    def get_potential_parameters(self, modifier: Modifier, parameters: dict, search_model: Model) -> list:
        raise NotImplementedError
