class Precondition:
    def __init__(self, cons):
        assert type(cons) == list
        self.conditions = cons

    def evaluate(self, model, param_dict, cons=None):
        """Evaluates if precondition is satisfied by the current state of the model

        :parameter - model : model of current state
        :parameter - param_dict : map of parameters - {?x: Object[banjo], ?y: Object[kiwi]}.
        Values in dictionary need to match up with the ones defined in the precondition
        :returns - True if precondition is satisfied
        :returns - False if precondition is not satisfied
        """
        if self.conditions == []:
            return True

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
            elif cons[i] == "forall":
                # All instances of predicates need to hold
                param_name = cons[1][0]
                param_type = cons[1][2]

                # get all objects of type param_type
                obs = model.problem.get_objects_of_type(param_type)

                for o in obs:
                    response = self.evaluate(model, self.merge_dictionaries(param_dict, {param_name: o}), cons[2])
                    if response is False:
                        return False
                return True

            else:
                # Evaluate predicate
                indexes = model.current_state.get_indexes(cons[0])
                if indexes is None:
                    return False

                for j in indexes:
                    index = 0
                    broken = False
                    for p in cons[1:]:
                        try:
                            if param_dict[p] != model.current_state.elements[j].objects[index]:
                                broken = True
                                break
                        except:
                            raise TypeError
                        index += 1
                    if not broken:
                        return True
                return False

    @staticmethod
    def merge_dictionaries(a, b):
        c = a.copy()
        c.update(b)
        return c