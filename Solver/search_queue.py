from Solver.model import Model


class SearchQueue:
    def __init__(self):
        self.__Q = []

    def add(self, model):
        if type(model) != Model:
            raise TypeError("Invalid parameter type!\n"
                            "Expected Model got {}".format(type(model)))

        # This is where the heuristic value would be calculated
        ranking = model.num_actions_taken
        model.set_ranking(ranking)

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

    def __len__(self):
        return len(self.__Q)