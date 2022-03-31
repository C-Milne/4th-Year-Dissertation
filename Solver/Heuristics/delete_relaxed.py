import sys
from Solver.Heuristics.Heuristic import Heuristic
Task = sys.modules['Internal_Representation.task'].Task
Method = sys.modules['Internal_Representation.method'].Method
Action = sys.modules['Internal_Representation.action'].Action
Subtask = sys.modules['Internal_Representation.subtasks'].Subtasks.Subtask


class Tree:
    class Node:
        def __init__(self, name):
            self.name = name
            self.operator = None
            self.type = None
            self.parents = []
            self.children = []

        def add_parent(self, node):
            # Check is not already in parent list
            if all([x.name != node.name for x in self.parents]):
                self.parents.append(node)

        def add_child(self, node):
            # Check is not already in children list
            if all([x.name != node.name for x in self.children]):
                self.children.append(node)

        def set_operator(self, operator: str):
            assert operator == "AND" or operator == "OR"
            self.operator = operator

        def set_type(self, t):
            assert t == Task or t == Method or t == Action
            self.type = t

    def __init__(self):
        self.root = None
        self.nodes = {}

    def add_node(self, name) -> Node:
        if name in self.nodes:
            return self.nodes[name]
        node = self.Node(name)
        self.nodes[name] = node
        return node

    def __getitem__(self, item):
        if item in self.nodes:
            return self.nodes[item]
        return None


class DeleteRelaxed(Heuristic):
    def __init__(self, domain, problem, solver, search_models):
        super().__init__(domain, problem, solver, search_models)
        self.low_target = True
        self.seen_states = {}

        self.tree = Tree()

    def ranking(self, model) -> float:
        pass

    def presolving_processing(self) -> None:
        # Add all actions to tree
        for a in self.domain.get_all_actions():
            self.tree.add_node(a.name)

        # Create bottom up reachability conditions for methods
        method_reach_conditions = {}
        for m in self.domain.get_all_methods():
            method_reach_conditions[m.name] = list(set([x.task.name for x in m.subtasks.tasks]))

        # Add methods which are bottom up reachable to the tree
        change = True
        while change:
            change = False
            if len(method_reach_conditions.keys()) == 0:
                break

            del_list = []
            for m in method_reach_conditions:
                m_cons = method_reach_conditions[m]
                # if all_m_cons hold, add m to tree
                if all(x in self.tree.nodes for x in m_cons):
                    method = self.domain.get_method(m)
                    node = self.tree.add_node(method.task['task'].name)
                    for mc in m_cons:
                        mc = self.tree[mc]
                        node.add_child(mc)
                        mc.add_parent(node)
                    change = True
                    del_list.append(m)

            for m in del_list:
                del method_reach_conditions[m]
        print("Here")

    def task_milestone(self, model) -> bool:
        num_tasks_remaining = str(len(model.waiting_subtasks))
        if num_tasks_remaining not in self.seen_states:
            self.seen_states[num_tasks_remaining] = [self.solver.reproduce_state(model.current_state)]
            return True
        else:
            reproduced_state = self.solver.reproduce_state(model.current_state)
            if reproduced_state not in self.seen_states[num_tasks_remaining]:
                self.seen_states[num_tasks_remaining].append(reproduced_state)
                return True
            else:
                return False
