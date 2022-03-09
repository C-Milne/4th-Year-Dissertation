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
