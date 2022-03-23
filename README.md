# TODO
1. Create an improved requirement parameter selector that looks ahead to the requirements of subtasks and their subtasks etc. Aiming to get better results for JSHOP
2. Develop a way for solving algorithms to be interchangable like heuristics and parameter selectors.
3. Track number of times a heuristic is called
4. Delete relaxed plan - max heuristic
5. topological sort - for ordering partial ordered problems

# Things to Test
1. Models created and solving times with and without the precondition optimisations (checking some preconditions before selecting parameters)

# Running Configurations
1. -m cProfile
2. Tests/Examples/IPC_Tests/Rover/rover-domain.hddl Tests/Examples/IPC_Tests/Rover/pfile01.hddl
3. Tests/Examples/IPC_Tests/um-translog01/domain.hddl Tests/Examples/IPC_Tests/um-translog01/problem.hddl
4. Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl