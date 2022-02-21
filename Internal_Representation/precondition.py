class Precondition:
    def __init__(self, params, domain):
        self.conditions = []
        self.domain = domain
        self.__parse(params)

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
            elif cons[i] == "forall":
                # All instances of predicates need to hold
                param_name = cons[1][0]
                param_type = cons[1][2]
                # get all objects of type param_type
                obs = self.domain.problem.get_objects_of_type(param_type)

                for o in obs:
                    response = self.evaluate(model, {cons[1][0]: o}, cons[2])
                    if response is False:
                        return False
                return True

            else:
                # Evaluate predicate
                indexes = model.current_state.get_indexes(cons[0])
                if indexes is None:
                    return False
                for j in indexes:
                    if param_dict[cons[1]].name in model.current_state.elements[j]:
                        return True
                return False

    def __parse(self, params):
        """TODO - Check params is valid"""
        self.conditions = params
