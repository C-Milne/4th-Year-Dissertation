"""The idea here is that this class will contain all information regarding the current state of the environment"""


class Model:
    def __init__(self, parser):
        self.current_state = {}
        self.__populate_current_state(parser)

    def __populate_current_state(self, parser):
        self.current_state = parser.initial_state
