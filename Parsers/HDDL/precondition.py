class Precondition:
    def __init__(self, params):
        self.conditions = params

    def evaluate(self, model, param_dict, cons=None):
        """Evaluates if precondition is satisfied by the current start
        :params     - model : model of current state
                    - param_dict : map of parameters
        :returns    - True if precondition is satisfied
                    - False if precondition is not satisfied
        Warning - This is a recursive method"""
        if cons is None:
            cons = self.conditions

        for i in range(len(cons)):
            if cons[i] == "and":
                # All the following statements need to be True
                predicates = [self.evaluate(model, param_dict, x) for x in cons[i + 1:]]
                for p in predicates:
                    if not p:
                        return False
                return True
            elif cons[i] == "or":
                # Only one of the following statements need to be True
                predicates = [self.evaluate(model, param_dict, x) for x in cons[i + 1:]]
                for p in predicates:
                    if p:
                        return True
                return False
            elif cons[i] == "not":
                # Negate the following statement
                return not self.evaluate(model, param_dict, cons[1])
            else:
                # Evaluate predicate
                for j in model.current_state.keys():
                    if j == cons[0]:
                        if param_dict[cons[1]] in model.current_state[j]:
                            return True
                        return False
                return False
