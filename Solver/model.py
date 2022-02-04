from Parsers.HDDL.HDDL_Parser import HDDLParser
"""The idea here is that this class will contain all information regarding the current state of the environment"""


class Model:
    def __init__(self, intake):
        self.current_state = {}
        if type(intake) == HDDLParser:
            self.__populate_current_state_parser(intake)
        elif type(intake) == dict:
            self.__populate_current_state_dict(intake)
        self.actions_taken = []

    def __populate_current_state_parser(self, parser):
        self.current_state = parser.initial_state

    def __populate_current_state_dict(self, dict):
        self.current_state = dict

    def add_action(self, action):
        self.actions_taken.append(action)
