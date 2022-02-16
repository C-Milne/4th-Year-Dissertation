class Predicate:
    def __init__(self, params):
        self.name = None
        self.parameters = []
        self.__parse(params)

    def __parse(self, params):
        """TODO - functionality for types"""
        i = 0
        while i < len(params):
            if i == 0:
                self.name = str(params[i])

            self.parameters.append(params[i])
            i += 1

    def __eq__(self, other):
        if self.name == other:
            return True
        return False
