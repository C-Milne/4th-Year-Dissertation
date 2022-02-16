class State:
    def __init__(self, problem):
        self._index = {}
        self.objects = {}
        self.elements = []
        self.problem = problem

    def add_element(self, e):
        if len(e) == 1:
            if type(e) == list:
                e = e[0]
            self.elements.append(e)
            self.__add_element_index(e, len(self.elements) - 1)
        else:
            self.elements.append(e)
            self.__add_objects(e[1:])
            self.__add_element_index(e[0], len(self.elements) - 1)

    def __add_element_index(self, val, index):
        if val in self._index.keys():
            self._index[val].append(index)
        else:
            self._index[val] = [index]

    def __add_objects(self, obs):
        for o in obs:
            self.objects[o] = self.problem.get_object(o)

    def get_indexes(self, pred_name):
        if pred_name in self._index.keys():
            return self._index[pred_name]
        else:
            return None
