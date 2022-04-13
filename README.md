# TODO
1. Create an improved requirement parameter selector that looks ahead to the requirements of subtasks and their subtasks etc. Aiming to get better results for JSHOP
2. Add and test a depth first approach - this will get stuck in recursion
3. Remove the requirements variable from modifier class. Move Requirement class to heuristic folder
4. When expanding JSHOP tasks we need to use an if-else approach (if the first methods preconditions are satisifed we don't bother with the second)
5. Set heuristic from command line
6. Set parameter types and return types for methods

# Things to Test

# Running Configurations
1. -m cProfile
2. Tests/Examples/IPC_Tests/Rover/rover-domain.hddl Tests/Examples/IPC_Tests/Rover/pfile01.hddl
3. Tests/Examples/IPC_Tests/um-translog01/domain.hddl Tests/Examples/IPC_Tests/um-translog01/problem.hddl
4. Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl
5. python ./output_plan_reader.py ../../output/runner_test_basic_p1