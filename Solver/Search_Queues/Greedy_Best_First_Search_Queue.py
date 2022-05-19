from Solver.Search_Queues.search_queue import SearchQueue


class GBFSSearchQueue(SearchQueue):
    def __init__(self):
        super().__init__()

    def _add_model(self, model):
        ranking = self.heuristic.ranking(model)

        if type(ranking) != int and (ranking is None or ranking == False):
            return  # Do not add to search queue
        model.set_ranking(ranking)

        added = False
        i = 0
        while i < len(self._Q):
            if ranking < self._Q[i].get_ranking():
                self._Q.insert(i, model)
                added = True
                break
            i += 1
        if not added:
            self._Q.append(model)
