# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "ortools",
# ]
# ///
from ortools.sat.python import cp_model

def solve_hexagonal_grid():
    model = cp_model.CpModel()

    # grid structure:
    #      0   1   2
    #    3   4   5   6
    #  7   8   9  10  11
    #   12  13  14  15
    #     16  17  18

    # Create variables for each cell (1-19, unique numbers)
    tiles = {cell: model.NewIntVar(1, 19, f"tile_{cell}") for cell in range(19)}

    # Add constraint: all tiles must be unique
    model.AddAllDifferent(tiles.values())

    # Add row constraints (sum = 38)
    model.Add(sum(tiles[cell] for cell in [0, 1, 2]) == 38)
    model.Add(sum(tiles[cell] for cell in [3, 4, 5, 6]) == 38)
    model.Add(sum(tiles[cell] for cell in [7, 8, 9, 10, 11]) == 38)
    model.Add(sum(tiles[cell] for cell in [12, 13, 14, 15]) == 38)
    model.Add(sum(tiles[cell] for cell in [16, 17, 18]) == 38)

    # Add diagonal-right constraints (sum = 38)
    model.Add(sum(tiles[cell] for cell in [7, 12, 16]) == 38)
    model.Add(sum(tiles[cell] for cell in [3, 8, 13, 17]) == 38)
    model.Add(sum(tiles[cell] for cell in [0, 4, 9, 14, 18]) == 38)
    model.Add(sum(tiles[cell] for cell in [1, 5, 10, 15]) == 38)
    model.Add(sum(tiles[cell] for cell in [2, 6, 11]) == 38)

    # Add diagonal-left constraints (sum = 38)
    model.Add(sum(tiles[cell] for cell in [0, 3, 7]) == 38)
    model.Add(sum(tiles[cell] for cell in [1, 4, 8, 12]) == 38)
    model.Add(sum(tiles[cell] for cell in [2, 5, 9, 13, 16]) == 38)
    model.Add(sum(tiles[cell] for cell in [6, 10, 14, 17]) == 38)
    model.Add(sum(tiles[cell] for cell in [11, 15, 18]) == 38)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        # Extract the solution
        solution = [solver.Value(tiles[cell]) for cell in range(19)]

        # Format the solution in hexagonal shape
        hexagonal_solution = [
            "      {}   {}   {}".format(solution[0], solution[1], solution[2]),
            "    {}   {}   {}   {}".format(solution[3], solution[4], solution[5], solution[6]),
            "  {}   {}   {}   {}   {}".format(solution[7], solution[8], solution[9], solution[10], solution[11]),
            "   {}   {}   {}   {}".format(solution[12], solution[13], solution[14], solution[15]),
            "     {}   {}   {}".format(solution[16], solution[17], solution[18]),
        ]

        # Print the formatted solution
        for row in hexagonal_solution:
            print(row)
    else:
        print("No solution found.")

# Run the solver
solve_hexagonal_grid()


# Outputs:
#      18   17   3
#    11   1   7   19
#  9   6   5   2   16
#   14   8   4   12
#     15   13   10
