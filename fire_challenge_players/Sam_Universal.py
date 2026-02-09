
# type: ignore

"""
Universal Fire Challenge Solver - CP-SAT Optimization
======================================================
Sam Mirazi - True Universal Solution

ONE model for ALL maps:
- Binary variables: x[v]=wall, r[v]=burned
- Constraints encode reachability directly
- Solver finds optimal wall placement

No heuristics. No scenarios. Pure optimization.
"""

from ortools.sat.python import cp_model
import numpy as np
from fire_challenge import (
    get_map,
    place_walls,
    highlight_cells,
    visualize_result,
    get_available_maps
)


def solve_fire_cpsat(grid, max_walls, time_limit=60.0):
    """
    Universal fire challenge solver using CP-SAT.

    Formulation:
    - x[v] = 1 if wall placed at open cell v
    - r[v] = 1 if cell v is burned (reachable from fire)

    Constraints:
    1. Budget: sum(x) <= max_walls
    2. Sources burn: r[s] = 1 for all fire sources
    3. Walls block: r[v] <= 1 - x[v] (wall can't burn)
    4. Reachability: r[v] >= r[u] - x[v] (fire spreads to non-walled neighbors)

    Objective: minimize sum(r[v]) over open cells
    """
    height, width = grid.shape

    # Identify traversable cells (open=0 or fire=2), excluding water(1)
    traversable = []
    open_cells = []
    fire_sources = []
    cell_to_idx = {}

    for y in range(height):
        for x in range(width):
            if grid[y, x] in (0, 2):
                idx = len(traversable)
                cell_to_idx[(x, y)] = idx
                traversable.append((x, y))
                if grid[y, x] == 0:
                    open_cells.append((x, y))
                else:
                    fire_sources.append((x, y))

    if not open_cells or not fire_sources:
        return [], 0

    # Build adjacency (4-neighbor) among traversable cells
    edges = []
    for (x, y) in traversable:
        u = cell_to_idx[(x, y)]
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) in cell_to_idx:
                v = cell_to_idx[(nx, ny)]
                edges.append((u, v))

    # Build CP-SAT model
    model = cp_model.CpModel()

    # r[u] = 1 if cell u is burned/reachable from fire
    r = [model.NewBoolVar(f"r_{u}") for u in range(len(traversable))]

    # x[u] = 1 if wall placed at cell u (only for open cells)
    x = {}
    for cell in open_cells:
        u = cell_to_idx[cell]
        x[u] = model.NewBoolVar(f"x_{u}")

    # Constraint 1: Budget - sum of walls <= max_walls
    model.Add(sum(x.values()) <= max_walls)

    # Constraint 2: Fire sources always burn
    for cell in fire_sources:
        s = cell_to_idx[cell]
        model.Add(r[s] == 1)

    # Constraint 3: Walls cannot burn (r[u] + x[u] <= 1)
    for u, xu in x.items():
        model.Add(r[u] + xu <= 1)

    # Constraint 4: Reachability closure
    # If u burns and v is neighbor: r[v] >= r[u] - x[v]
    # Rewritten as: r[v] + x[v] >= r[u] (if v is open)
    #           or: r[v] >= r[u] (if v is fire source)
    for u, v in edges:
        if v in x:
            model.Add(r[v] + x[v] >= r[u])
        else:
            model.Add(r[v] >= r[u])

    # Objective: minimize burned open cells
    model.Minimize(sum(r[cell_to_idx[cell]] for cell in open_cells))

    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 28

    status = solver.Solve(model)

    # Map status to string
    status_names = {
        cp_model.OPTIMAL: "OPTIMAL",
        cp_model.FEASIBLE: "FEASIBLE",
        cp_model.INFEASIBLE: "INFEASIBLE",
        cp_model.MODEL_INVALID: "MODEL_INVALID",
        cp_model.UNKNOWN: "UNKNOWN"
    }
    status_str = status_names.get(status, "UNKNOWN")
    print(f"CP-SAT status = {status_str}")

    # Extract solution
    walls = []
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        for u, xu in x.items():
            if solver.Value(xu) == 1:
                walls.append(traversable[u])

    # Calculate cells saved
    burned_count = sum(solver.Value(r[cell_to_idx[cell]]) for cell in open_cells)
    saved = len(open_cells) - burned_count

    return walls, saved, status_str


def solve_fire_challenge(map_num=0, visualize=True):
    """
    Solve a fire challenge map using CP-SAT optimization.
    """
    grid, max_walls, map_name = get_map(map=map_num)

    print(f"\n{'='*60}")
    print(f"Map {map_num} - {map_name}")
    print(f"{'='*60}")
    print(f"Grid size: {grid.shape}")
    print(f"Maximum walls: {max_walls}")

    total_open = int(np.sum(grid == 0))
    print(f"Total open cells: {total_open}")

    # Solve with CP-SAT
    print(f"\n--- CP-SAT Optimization ---")
    best_walls, best_score, status = solve_fire_cpsat(grid, max_walls)

    # Results
    percentage = (best_score / total_open * 100) if total_open > 0 else 0

    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Cells saved: {best_score}/{total_open} ({percentage:.1f}%)")
    print(f"Walls used: {len(best_walls)}/{max_walls}")
    print(f"Wall positions: {best_walls}")

    if visualize:
        grid, _, _ = get_map(map=map_num)

        if best_walls:
            highlight_cells(best_walls, level=2)
            place_walls(best_walls)

        print("\nLaunching visualization...")
        visualize_result()

    return best_score, total_open, best_walls, status


def test_all_maps(visualize=False):
    """Test on all maps."""
    print("="*60)
    print("CP-SAT UNIVERSAL SOLVER - ALL MAPS")
    print("="*60)

    results = []
    available_maps = get_available_maps()

    for map_num, map_name in available_maps:
        score, total, walls, status = solve_fire_challenge(map_num, visualize=visualize)
        results.append((map_num, map_name, score, total, walls, status))

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for map_num, name, score, total, walls, status in results:
        pct = score/total*100 if total > 0 else 0
        print(f"Map {map_num:2d} - {name:30s}: {score:3d}/{total:3d} ({pct:5.1f}%) [{status}]")

    return results


if __name__ == "__main__":
    print("CP-SAT Universal Fire Challenge Solver")
    print("=" * 60)

    print("\nAvailable maps:")
    available_maps = get_available_maps()
    for num, name in available_maps:
        print(f"  {num}: {name}")

    print(f"\nEnter map number, 'all' to test all, or Enter for map 0:")
    choice = input().strip()

    if choice.lower() == 'all':
        test_all_maps(visualize=False)
    elif choice.isdigit():
        map_num = int(choice)
        if 0 <= map_num < len(available_maps):
            solve_fire_challenge(map_num=map_num)
        else:
            print("Invalid. Using map 0.")
            solve_fire_challenge(map_num=0)
    else:
        solve_fire_challenge(map_num=0)
