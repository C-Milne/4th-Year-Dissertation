# TODO
1. Combine SHOP parser with established codebase
2. Implement breadth first with pruning - If multiple subtasks are given in the beginning of search. Add them one at a time to the search_modifiers so duplicate states can be pruned
3. Implement way for parameter selection to be done the same way as a heuristic - This needs to be used in the forall condition evaluation as well as the solving module (remove the assertion for the collect_objects method in forall conditions when this is done)
4. Create a heuristic that estimates cost to goal - by comparing which of the goal conditions are already satisfied by the current model. Also ensure recursion does not impact this too bad


# Things to Test
