from Internal_Representation.parameter import Parameter


class ListParameter(Parameter):
    def __init__(self, param_list_name: str, internal_param_name: str = None):
        super().__init__()
        assert type(param_list_name) == str
        self.param_list_name = param_list_name
        assert type(internal_param_name) == str or internal_param_name is None
        self.internal_param_name = internal_param_name
