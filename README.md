# TODO
1. Add and test a depth first approach - this will get stuck in recursion
2. Remove the requirements variable from modifier class. Move Requirement class to heuristic folder
3. When expanding JSHOP tasks we need to use an if-else approach (if the first methods preconditions are satisifed we don't bother with the second)

# Things to Test

# Running Configurations
1. -m cProfile
2. Tests/Examples/IPC_Tests/Rover/rover-domain.hddl Tests/Examples/IPC_Tests/Rover/pfile01.hddl
3. Tests/Examples/IPC_Tests/um-translog01/domain.hddl Tests/Examples/IPC_Tests/um-translog01/problem.hddl
4. Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl
5. python ./output_plan_reader.py ../../output/runner_test_basic_p1
6. Tests/Examples/Basic/basic.hddl Tests/Examples/Basic/pb1.hddl -heu Solver/Heuristics/distance_to_goal.py