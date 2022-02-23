class State:
    def __init__(self, problem):
        self._index = {}
        self.objects = {}
        self.elements = []
        self.problem = problem

    def add_element(self, predicate_identifier, predicate_definition=[]):
        if len(predicate_definition) == 0:
            self.__add_element_predicate(predicate_identifier)
        else:
            self.__add_element_predicate_definition(predicate_identifier, predicate_definition)
        self.__add_element_index(predicate_identifier, len(self.elements) - 1)

    def __add_element_predicate(self, predicate_identifier):
        if type(predicate_identifier) == list:
            predicate_identifier = predicate_identifier[0]
        self.elements.append(predicate_identifier)

    def __add_element_predicate_definition(self, predicate_identifier, predicate_definition):
        self.elements.append([predicate_identifier] + predicate_definition)
        self.__add_objects(predicate_definition)

    def remove_element(self, predicate_identifier, predicate_definitions=None):
        if predicate_definitions is None:
            self.__remove_element_predicate(predicate_identifier)
        else:
            self.__remove_element_predicate_definition(predicate_identifier, predicate_definitions)

    def __remove_element_predicate(self, identifier):
        """Params:  - identifier : Predicate name
                    - Index : Index in self.elements to be removed"""
        index = self.get_indexes(identifier)
        assert len(index) == 1
        index = index[0]

        # Do the deletion
        del self.elements[index]

        # Adjust self._index
        self.__adjust_index_remove_element(identifier, index)

    def __remove_element_predicate_definition(self, predicate_identifier, predicate_definitions):
        predicate_indexes = self.get_indexes(predicate_identifier)
        for i in predicate_indexes:
            if self.elements[i][1:] == predicate_definitions:
                del self.elements[i]
                break
        # Adjust self._index
        self.__adjust_index_remove_element(predicate_identifier, i)

    def __adjust_index_remove_element(self, identifier, index_removed):
        # Remove deleted element from self._index
        if len(self._index[identifier]) == 1:
            del self._index[identifier]
        else:
            del self._index[identifier][self._index[identifier].index(index_removed)]

        # Update self._index
        for k in self._index.keys():
            i = 0
            while i < len(self._index[k]):
                if self._index[k][i] > index_removed:
                    self._index[k][i] -= 1
                i += 1

    def __add_element_index(self, val, index):
        if val in self._index.keys():
            self._index[val].append(index)
        else:
            self._index[val] = [index]

    def __add_objects(self, obs):
        for o in obs:
            self.objects[o] = self.problem.get_object(o)

    def get_indexes(self, pred_name):
        if type(pred_name) != str:
            print("issue")
        if pred_name in self._index.keys():
            return self._index[pred_name]
        else:
            return None

    def get_predicates(self):
        return self._index.keys()
