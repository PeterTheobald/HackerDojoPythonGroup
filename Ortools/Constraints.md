Constraint based programming
part of Operational Research (OR)
NP Complete problems (Nondeterministic Polynomial)
optimization problem solver libraries

ORtools = Google's Operational Research tools


Different solver engines:
- CP-SAT - Constraint Programming, Boolean SATisfiability
  - Finds a feasable solution from many candidates for problems that can be expressed as a set of boolean rules, eg: scheduling a set of workers shifts
- Network Flows - Find best route in graph of nodes and connections, eg: Shipping goods with railroad cars
- MP-Solver, GLOP (Google Linear Optimization Programming) - Linear optimization. Constraints can be expressed as a series of linear relationships, eg: x+2y<=14 and 3x-y>=0 and x-y<=2
- Integer Optimization - Entities are finite integers like enums. eg: How many cars, tvs, and computers should our factory produce to maximize profit.
- Assignment problems - Assign pairs such as which workers get which tasks
- Packing Problems - The TETRIS problem, pack the maximum number of boxes into each truck

Compare:
- Videogame pathfinding shortest path; Dijkstra's algorithm, A* algorithm
  - https://www.cs.usfca.edu/~galles/visualization/Dijkstra.html
- Sudoku: see our heuristic based solution vs. CP-SAT
  - https://anhminhtran235.github.io/sudoku-solver-visualizer/
