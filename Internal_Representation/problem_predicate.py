from Internal_Representation.predicate import Predicate
from Internal_Representation.Object import Object


class ProblemPredicate:
    def __init__(self, predicate: Predicate, objects: list[Object]):
        assert type(predicate) == Predicate
        assert type(objects) == list
        for o in objects:
            assert type(o) == Object

        self.predicate = predicate
        self.objects = objects
