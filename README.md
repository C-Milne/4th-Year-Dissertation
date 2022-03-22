# TODO
1. Implement way for parameter selection to be done the same way as a heuristic - This needs to be used in the forall condition evaluation as well as the solving module (remove the assertion for the collect_objects method in forall conditions when this is done)
2. Create a heuristic that estimates cost to goal - by comparing which of the goal conditions are already satisfied by the current model. Also ensure recursion does not impact this too bad
3. Create an improved requirement parameter selector that looks ahead to the requirements of subtasks and their subtasks etc. Aiming to get better results for JSHOP

# Things to Test
