import sys
from Solver.Heuristics.Heuristic import Heuristic
Task = sys.modules['Internal_Representation.task'].Task
Method = sys.modules['Internal_Representation.method'].Method
Action = sys.modules['Internal_Representation.action'].Action
Subtask = sys.modules['Internal_Representation.subtasks'].Subtasks.Subtask
Model = sys.modules['Solver.model'].Model


class Tree:
    class Node:
        def __init__(self, name):
            self.name = name
            self.operator = None
            self.type = None
            self.parents = []
            self.children = []
            self.distance = None

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

        def set_distance(self, v: int):
            assert type(v) == int
            self.distance = v

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

    def ranking(self, model: Model) -> float:
        next_mod = model.search_modifiers[0].task
        if type(next_mod) != Task and model.ranking is not None:
            return model.ranking
        elif type(next_mod) != Task:
            i = -1
            op = model.operations_taken[i].action
            while type(op) != Task:
                i -= 1
                op = model.operations_taken[i].action
            assert type(op) == Task
            return len(model.operations_taken) + self.tree.nodes[op.name].distance + self._calculate_distance_tasks(model)
        else:
            # We have all tasks
            return len(model.operations_taken) + self._calculate_distance_tasks(model)

    def _calculate_distance_tasks(self, model: Model):
        distance = 0
        for m in model.search_modifiers:
            if type(m) == Task:
                distance += self.tree.nodes[m.name].distance
        for m in model.waiting_subtasks:
            if type(m) == Task:
                distance += self.tree.nodes[m.name].distance
        return distance

    def presolving_processing(self) -> None:
        # Add all actions to tree
        for a in self.domain.get_all_actions():
            node = self.tree.add_node(a.name)
            node.set_distance(1)

        # Create bottom up reachability conditions for methods
        method_reach_conditions = {}
        for m in self.domain.get_all_methods():
            method_reach_conditions[m.name] = list(set([x.task.name for x in m.subtasks.tasks]))

        # Add methods which are bottom up reachable to the tree
        task_nodes = []
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
                    if node not in task_nodes:
                        task_nodes.append(node)
                    for mc in m_cons:
                        mc = self.tree[mc]
                        node.add_child(mc)
                        mc.add_parent(node)
                    change = True
                    del_list.append(m)

            for m in del_list:
                del method_reach_conditions[m]

        # Assign each task node a distance to goal
        for tn in task_nodes:
            self._calculate_task_node_distance_goal(tn)

    def _calculate_task_node_distance_goal(self, tn) -> int:
        if tn.distance is not None:
            return tn.distance
        total_distance = 0
        for n in tn.children:
            if n.distance is None and tn not in n.children:
                total_distance += self._calculate_task_node_distance_goal(n)
            elif n.distance is None and tn in n.children and tn != n:
                total_distance += 1
            elif tn == n:
                continue
            else:
                total_distance += n.distance
        total_distance += 1
        tn.set_distance(total_distance)
        return total_distance

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
