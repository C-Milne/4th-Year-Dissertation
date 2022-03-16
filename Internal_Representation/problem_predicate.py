from Internal_Representation.predicate import Predicate
from Internal_Representation.Object import Object


class ProblemPredicate:
    def __init__(self, predicate: Predicate, objects: list[Object]):
        """:Params  - predicate : Predicate
                    - objects   : List of objects that belong to this predicate in ONE instance
                                [object[waypoint1], object[waypoint0]]"""
        assert isinstance(predicate, Predicate)
        assert type(objects) == list
        for o in objects:
            assert type(o) == Object

        self.predicate = predicate
        self.objects = objects

    def __eq__(self, other):
        if self.predicate == other.predicate and self.objects == other.objects:
            return True
        return False

    def __str__(self):
        print_string = self.predicate.name
        if len(self.objects) > 0:
            print_string += " -"
        for o in self.objects:
            print_string += " " + o.name
        return print_string
