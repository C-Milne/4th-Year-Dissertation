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

    def __init__(self):
        self.root = None
        self.nodes = {}

    def add_node(self, name, parent) -> Node:
        assert name not in self.nodes
        node = self.Node(name)
        if parent is None and self.root is None:
            self.root = node
        else:
            assert type(parent) == Tree.Node
            parent.children.append(node)
            node.parents.append(parent)
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
        self.tree.add_node("BASE", None)

    def ranking(self, model) -> float:
        pass

    def presolving_processing(self) -> None:
        for t in self.problem.subtasks.tasks:
            self.__presolving_expand(t.task, self.tree.root)

    def __presolving_expand(self, mod, parent):
        assert type(parent) == Tree.Node
        name = mod.name

        # Check if mod is already in tree
        found = self.tree[name]
        if found is None:
            # Create new node
            node = self.tree.add_node(name, parent)

            if type(mod) == Task:
                subTs = mod.methods
            elif type(mod) == Method:
                subTs = mod.subtasks.tasks
            elif type(mod) == Action:
                return
            else:
                raise NotImplementedError
            for t in subTs:
                if type(t) == Subtask:
                    t = t.task
                self.__presolving_expand(t, node)
        else:
            # Node already exists
            node = found
            node.add_parent(parent)
            parent.add_child(node)

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
