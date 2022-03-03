from Solver.model import Model


class SearchQueue:
    def __init__(self):
        self.__Q = []
        self.__completed_models = []

    def add(self, model):
        if type(model) != Model:
            raise TypeError("Invalid parameter type!\n"
                            "Expected Model got {}".format(type(model)))

        # This is where the heuristic value would be calculated
        ranking = len(model.actions_taken)
        model.set_ranking(ranking)

        if len(model.search_modifiers) > 0:
            self.__add_model(model, ranking)
        else:
            self.__completed_models.append(model)

    def __add_model(self, model, ranking):
        added = False
        i = 0
        while i < len(self.__Q):
            if ranking < self.__Q[i].get_ranking():
                self.__Q.insert(i, model)
                added = True
                break
            i += 1
        if not added:
            self.__Q.append(model)

    def pop(self):
        return self.__Q.pop(0)

    def clear(self):
        self.__Q = []

    def get_num_search_models(self):
        return len(self.__Q)

    def get_num_completed_models(self):
        return len(self.__completed_models)

    def get_sole_completed_model(self):
        if len(self.__completed_models) == 1:
            return self.__completed_models[0]
        return None

    def __len__(self):
        return len(self.__Q)
