class State:
    def __init__(self):
        self._index = {}
        self._elements = []

    def add_element(self, e):
        if len(e) == 1:
            if type(e) == list:
                e = e[0]
            self._elements.append(e)
            self.__add_element_index(e, len(self._elements) - 1)
        else:
            self._elements.append(e)
            self.__add_element_index(e[0], len(self._elements) - 1)

    def __add_element_index(self, val, index):
        if val in self._index.keys():
            self._index[val].append(index)
        else:
            self._index[val] = [index]