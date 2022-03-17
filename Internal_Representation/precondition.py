import sys
from Internal_Representation.conditions import Condition, PredicateCondition, OperatorCondition, VariableCondition, ForallCondition


class Precondition:
    def __init__(self, conditions: str):
        self.head = None
        self.conditions = conditions
        self.requirements = None

    def add_operator_condition(self, operator: str, parent: Condition) -> Condition:
        assert type(operator) == str
        assert isinstance(parent, Condition) or parent is None

        con = OperatorCondition(operator)
        self.__final_condition_addition_checks(con, parent)
        return con

    def add_predicate_condition(self, pred, parameter_names: list[str], parent: Condition):
        assert isinstance(parent, Condition) or parent is None
        con = PredicateCondition(pred, parameter_names)
        self.__final_condition_addition_checks(con, parent)
        return con

    def add_variable_condition(self, parameter_name: str, parent: Condition):
        assert isinstance(parent, Condition) or parent is None
        con = VariableCondition(parameter_name)
        self.__final_condition_addition_checks(con, parent)
        return con

    def add_forall_condition(self, selector, satisfier: Condition, parent):
        """
        :param selector: ['?b', '-', 'block'] OR ['?z', ['package', '?z'], ['at', '?z', '?x']]
        :param satisfier: ['done', '?b']
        :return:
        """
        if len(selector) == 3 and all([type(x) == str for x in selector]):
            assert len(selector) == 3
            selected_variable = selector[0]
            selected_cons = ("type", selector[2])
        else:
            assert len(selector) == 2
            selected_variable = selector[0]
            selected_cons = selector[1]

        con = ForallCondition(selected_variable, selected_cons, satisfier)
        self.__final_condition_addition_checks(con, parent)
        return con

    def __final_condition_addition_checks(self, con, parent):
        if self.head is None:
            self.head = con
        if parent is not None:
            parent.add_child(con)

    def evaluate(self, param_dict, search_model, problem) -> bool:
        if self.head is None:
            return True

        result = self.head.evaluate(param_dict, search_model, problem)
        return result

    def load_requirements(self):
        self.requirements = sys.modules['Internal_Representation.requirements'].Requirements([], self)
        self.requirements.prepare_requirements()

    @staticmethod
    def merge_dictionaries(a, b):
        c = a.copy()
        c.update(b)
        return c
