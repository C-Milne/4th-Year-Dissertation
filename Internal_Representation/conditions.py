import sys
from Internal_Representation.predicate import Predicate
from Internal_Representation.Object import Object


class Condition:
    def __init__(self):
        pass

    def evaluate(self, param_dict: dict, search_model, problem) -> bool:
        raise NotImplementedError


class PredicateCondition(Condition):
    def __init__(self, pred: Predicate, parameter_names: list[str]):
        super().__init__()
        assert type(pred) == Predicate
        self.pred = pred
        assert type(parameter_names) == list and all([type(x) == str for x in parameter_names])
        self.parameter_name = parameter_names

    def evaluate(self, param_dict: dict, search_model, problem) -> bool:
        p_list = []
        for i in self.parameter_name:
            p_list.append(param_dict[i])
        return search_model.current_state.check_if_predicate_value_exists(self.pred, p_list)


class VariableCondition(Condition):
    def __init__(self, variable_name: str):
        super().__init__()
        assert type(variable_name) == str
        self.variable_name = variable_name

    def evaluate(self, param_dict: dict, search_model, problem) -> Object:
        return param_dict[self.variable_name]


class OperatorCondition(Condition):
    def __init__(self, operator):
        super().__init__()
        assert operator == "and" or operator == "not" or operator == "or" or operator == "="
        self.operator = operator  # and, not, or, =
        self.children = []

    def add_child(self, condition):
        assert isinstance(condition, Condition)
        self.children.append(condition)

    def evaluate(self, param_dict: dict, search_model, problem) -> bool:
        children_eval = []
        if len(self.children) > 0:
            children_eval = [x.evaluate(param_dict, search_model, problem) for x in self.children]
        if self.operator == "and":
            for i in children_eval:
                if i != True:
                    return False
            return True
        elif self.operator == "or":
            for i in children_eval:
                if i == True:
                    return True
            return False
        elif self.operator == "not":
            assert len(children_eval) == 1 and type(children_eval[0]) == bool
            return not children_eval[0]
        elif self.operator == "=":
            v = children_eval[0]
            for i in children_eval[1:]:
                if v != i:
                    return False
            return True


class ForallCondition(Condition):
    def __init__(self, selected_variable: str, selector, satisfier: Condition):
        super().__init__()
        assert isinstance(satisfier, Condition)
        self.selected_variable = selected_variable
        self.selector = selector
        self.satisfier = satisfier

    def evaluate(self, param_dict: dict, search_model, problem) -> bool:
        obs = self._collect_objects(param_dict, search_model, problem)
        for o in obs:
            res = self.satisfier.evaluate(merge_dictionaries(param_dict, {self.selected_variable: o}), search_model, problem)
            if not res:
                return False
        return True

    def _collect_objects(self, param_dict, search_model, problem) -> list[Object]:
        if type(self.selector) == tuple and self.selector[0] == "type":
            return problem.get_objects_of_type(self.selector[1])
        elif isinstance(self.selector, sys.modules['Internal_Representation.precondition'].Precondition):
            obs = problem.get_all_objects()
            return_list = []
            for k in obs:
                # if self.selector.evaluate(None, search_dict, problem)
                pass
            print("here")
            return return_list
        else:
            raise NotImplementedError


def merge_dictionaries(a, b):
    c = a.copy()
    c.update(b)
    return c
