# Installing the system
This system can be downloaded from GitHub [here](https://github.com/C-Milne/4th-Year-Dissertation)

# Dependencies
This system requires Python to be installed. Python downloads can be found [here](https://www.python.org/).

All other packages used by the system are included with Python as standard.

This system has been tested with Python versions 3.9 & 3.10

# Running the system
From the command line a problem can be given to the planner to solve using the command:

```commandline
python ./Runner.py <Domain File Path> <Problem File Path>
```

For more information on running the system please refer to the User Manual [here](https://github.com/C-Milne/4th-Year-Dissertation/blob/main/README.md).

# Space and memory requirements
Memory requirements depend entirely on the size of the problem being solved. Larger problems require more options to be searched which in turn uses more memory.

# Key File Paths
- Heuristics : /Solver/Heuristics
- Parameter Selectors : /Solver/Parameter_Selection
- Search Queues : /Solver/Search_Queues
- Solving Algorithms : /Solver/Solving_Algorithms
- Parsers : /Parsers
- Representation Objects : /Internal_Representation
- Example Problems : /Tests/Examples
- Evaluation methods : /Tests/Evaluation/Heuristic_Evaluation
- Unit Tests : /Tests/UnitTests

# Directions for Future Improvements
When developing new interchangeable components specific classes need to be inherited by any developed component.

## Heuristic
Developed Heuristics need to inherit the Heuristic class found in the Solver/Heuristics/Heuristic.py file.
There are some alternatives to inheriting the Heuristic class directly, the Pruning and NoPruning classes found in files Solver/Heuristics/pruning.py and Solver/Heuristics/no_pruning.py respectively.
Both of these classes inherit from the Heuristic class. The Pruning Class contains functionality for basic model pruning that can be inherited by other heuristics. 
The PartialOrderPruning Class from file Solver/Heuristics/partial_order_pruning.py provides the same functionality but for partial-order problems.

## Parameter Selector
Developed Parameter Selectors need to inherit the ParameterSelector Class found in file Solver/Parameter_Selection/ParameterSelector.py.

## Search Queue
Developed Search Queues need to inherit the SearchQueue class found in Solver/Search_Queues/search_queue.py.

## Solver
Developed Solvers need to inherit the Solver class within the Solver/Solving_Algorithms/solver.py file.

## Running Unittests
All of the unittests can be run from the Tests/UnitTests directory using the following command:

```commandline
python ./All_Tests.py
```

# Bug Solving
When attempting to debug the system it is recommended that a debugger with breakpoints is used. To aid in the debugging 
process the search procedure can be manually controlled using a script. 
Below is a snippet of a test case from the file Tests/UnitTest/JSHOP_Solving_Tests.py:

```python
def test_rover_execution_part_guided(self):
    domain, problem, parser, solver = env_setup(False)
    parser.parse_domain(self.rover_test_path + "rover.jshop")
    parser.parse_problem(self.rover_test_path + "problem.jshop")

    execution_prep(problem, solver)
    solver.parameter_selector.presolving_processing(domain, problem)
    # res = solver.solve()

    solver._search(True)
```

In this example the search produce is completely controlled by the script shown. Notice that instead of using ```solver.solve()```
```solver._search(True)``` is being used. This acts as a step control for search. Each functional call of ```solver._search(True)```
will only decompose 1 Task, Method, or Action. This is an effective way to debug and track search procedure.