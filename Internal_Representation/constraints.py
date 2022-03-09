class Constraints:
    class Condition:
        def __init__(self, operator):
            self.operator = operator    # and, not, or, =, var_name
            self.children = []

        def add_child(self, condition):
            assert type(condition) == Constraints.Condition
            self.children.append(condition)

    def __init__(self):
        self.head = None

    def add_condition(self, operator: str, parent: Condition) -> Condition:
        assert type(operator) == str
        assert type(parent) == Constraints.Condition or parent is None

        con = self.Condition(operator)
        if self.head is None:
            self.head = con
        if parent is not None:
            parent.add_child(con)
        return con

    def evaluate(self, param_dict) -> bool:
        def __evaluate_node(condition_node: Constraints.Condition):
            children_eval = []
            if len(condition_node.children) > 0:
                children_eval = [__evaluate_node(x) for x in condition_node.children]
            if condition_node.operator == "and":
                for i in children_eval:
                    if i != True:
                        return False
                return True
            elif condition_node.operator == "or":
                for i in children_eval:
                    if i == True:
                        return True
                return False
            elif condition_node.operator == "not":
                assert len(children_eval) == 1 and type(children_eval[0]) == bool
                return not children_eval[0]
            elif condition_node.operator == "=":
                v = children_eval[0]
                for i in children_eval[1:]:
                    if v != i:
                        return False
                return True
            elif type(condition_node.operator) == str:
                return param_dict[condition_node.operator]
            else:
                raise TypeError("Unexpected operator {}".format(condition_node.operator))

        result = __evaluate_node(self.head)
        return result
