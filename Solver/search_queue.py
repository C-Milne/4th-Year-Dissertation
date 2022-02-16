from Solver.model import Model


class SearchQueue:
    def __init__(self):
        self.__Q = []

    def add(self, model):
        if type(model) != Model:
            raise TypeError("Invalid parameter type!\n"
                            "Expected Model got {}".format(type(model)))
        moves = model.actions_taken
        added = False
        i = 0
        while i < len(self.__Q):
            if moves < self.__Q[i]:
                self.__Q.insert(i, model)
                added = True
                break
            i += 1
        if not added:
            self.__Q.append(model)

    def pop(self):
        return self.__Q.pop(0)

    def __len__(self):
        return len(self.__Q)