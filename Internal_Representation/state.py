from Internal_Representation.problem_predicate import ProblemPredicate


class State:
    def __init__(self):
        self._index = {}
        self.elements = []

    def add_element(self, element: ProblemPredicate):
        assert type(element) == ProblemPredicate
        self.elements.append(element)
        self.__add_element_to_index(element)

    def __add_element_to_index(self, element: ProblemPredicate):
        name = element.predicate.name
        if name in self._index.keys():
            self._index[name].append(len(self.elements) - 1)
        else:
            self._index[name] = [len(self.elements) - 1]

    def get_indexes(self, pred_name: str):
        if type(pred_name) != str:
            raise TypeError("Parameter 'pred_name' must be a string. Type received: {}".format(type(pred_name)))
        if pred_name in self._index.keys():
            return self._index[pred_name]
        else:
            return None
