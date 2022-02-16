from Internal_Representation.problem import Problem
"""The idea here is that this class will contain all information regarding the current state of the environment"""


class Model:
    def __init__(self, intake, solver, modifiers):
        self.current_state = {}
        if type(intake) == Problem:
            self.__populate_current_state_parser(intake)
        elif type(intake) == dict:
            self.__populate_current_state_dict(intake)
        else:
            raise TypeError("Unexpected parameter type {} for intake".format(type(intake)))
        self.solver = solver
        self.available_modifiers = modifiers
        self.actions_taken = []
        self.num_actions_taken = 0
        self.available_unused_modifiers = 0
        self.count_available_unused_modifiers()

    def __populate_current_state_parser(self, parser):
        self.current_state = parser.initial_state

    def __populate_current_state_dict(self, dict):
        self.current_state = dict

    def add_action(self, action):
        self.actions_taken.append(action)

    def count_available_unused_modifiers(self):
        # Count which methods are available to the model in the current state
        for i in self.available_modifiers:
            # Get method parameters and preconditions
            params = i.get_parameters()
            precon = i.get_precondition()
            requirements = {}
            for p in params:
                requirements[p.name] = {"type": p.param_type, "predicates": []}

            for p in precon.conditions:
                if p == "and" or p == "or":
                    continue
                for v in p[1:]:
                    requirements[v]["predicates"].append(p[0])

            # Can the model satisfy these parameters in current state?


            print(params)
