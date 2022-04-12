# TODO
1. Create an improved requirement parameter selector that looks ahead to the requirements of subtasks and their subtasks etc. Aiming to get better results for JSHOP
2. Add and test a depth first approach - this will get stuck in recursion
3. Track number of times a heuristic is called
4. Partial ordering
   1. Consider orderings for initial task network
      1. The pruning methods found in current heuristics will not work with this - Change to consider which tasks are remaining not how many are remaining
5. Remove the requirements variable from modifier class. Move Requirement class to heuristic folder
6. When expanding JSHOP tasks we need to use an if-else approach (if the first methods preconditions are satisifed we don't bother with the second)
7. Implement writing plan to file

# Things to Test
1. Models created and solving times with and without the precondition optimisations (checking some preconditions before selecting parameters)

# Running Configurations
1. -m cProfile
2. Tests/Examples/IPC_Tests/Rover/rover-domain.hddl Tests/Examples/IPC_Tests/Rover/pfile01.hddl
3. Tests/Examples/IPC_Tests/um-translog01/domain.hddl Tests/Examples/IPC_Tests/um-translog01/problem.hddl
4. Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl