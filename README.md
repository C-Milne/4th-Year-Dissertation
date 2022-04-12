# TODO
1. Create an improved requirement parameter selector that looks ahead to the requirements of subtasks and their subtasks etc. Aiming to get better results for JSHOP
2. Add and test a depth first approach - this will get stuck in recursion
3. Track number of times a heuristic is called
4. Remove the requirements variable from modifier class. Move Requirement class to heuristic folder
5. When expanding JSHOP tasks we need to use an if-else approach (if the first methods preconditions are satisifed we don't bother with the second)
6. Implement writing plan to file

# Things to Test
1. Models created and solving times with and without the precondition optimisations (checking some preconditions before selecting parameters)

# Running Configurations
1. -m cProfile
2. Tests/Examples/IPC_Tests/Rover/rover-domain.hddl Tests/Examples/IPC_Tests/Rover/pfile01.hddl
3. Tests/Examples/IPC_Tests/um-translog01/domain.hddl Tests/Examples/IPC_Tests/um-translog01/problem.hddl
4. Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl