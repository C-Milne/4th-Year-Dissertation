# TODO
1. Create a heuristic that estimates cost to goal - by comparing which of the goal conditions are already satisfied by the current model. Instead of checking all predicates all the time, we can use the action tracker to see what has been changed - then we can just update the ranking. Also ensure recursion does not impact this too bad
2. Create an improved requirement parameter selector that looks ahead to the requirements of subtasks and their subtasks etc. Aiming to get better results for JSHOP
3. Develop a way for solving algorithms to be interchangable like heuristics and parameter selectors.
4. Track number of times a heuristic is called
5. Python profiler?? - python -m cprofile scripts args
6. Delete relaxed plan - max heuristic
7. topological sort - for ordering partial ordered problems

# Things to Test
1. Models created and solving times with and without the precondition optimisations (checking some preconditions before selecting parameters)
