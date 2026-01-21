"""
Sam's Fire Challenge Player - Advanced Optimization Algorithm
Sam Mirazi 1-21-2026

Strategy:
1. Expand search space to ALL open cells (not just adjacent to fire)
2. Use exhaustive search for small problems
3. Use smart candidate filtering + exhaustive for medium problems  
4. Use multiprocessing for parallel computation on all CPU cores
5. Memory-efficient generator approach
"""

from itertools import combinations
from collections import deque
from multiprocessing import Pool, cpu_count
from functools import partial
import numpy as np
from fire_challenge import (
    get_map, 
    place_walls, 
    test_result, 
    highlight_cells,
    visualize_result
)


def find_fire_positions(grid):
    """Find all initial fire positions in the grid."""
    fire_positions = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 2:  # Fire cell
                fire_positions.append((x, y))
    return fire_positions


def find_all_open_cells(grid):
    """Find all open cells in the grid."""
    open_cells = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 0:  # Open cell
                open_cells.append((x, y))
    return open_cells


def generate_diagonal_candidates(grid, max_walls):
    """Generate specific diagonal line patterns for corner protection."""
    height, width = grid.shape
    diagonals = []
    
    # Generate diagonals from each corner
    # Each diagonal aims to use edges as natural barriers
    
    # Top-right corner diagonals (going down-left)
    for start_x in range(max(0, width - height - 3), width):
        diagonal = []
        for offset in range(max_walls):
            x = start_x + offset
            y = offset
            if 0 <= x < width and 0 <= y < height and grid[y, x] == 0:
                diagonal.append((x, y))
        if len(diagonal) >= max_walls:
            diagonals.append(diagonal[:max_walls])
    
    # Top-left corner diagonals (going down-right)
    for start_x in range(min(height + 3, width)):
        diagonal = []
        for offset in range(max_walls):
            x = start_x + offset
            y = offset
            if 0 <= x < width and 0 <= y < height and grid[y, x] == 0:
                diagonal.append((x, y))
        if len(diagonal) >= max_walls:
            diagonals.append(diagonal[:max_walls])
    
    # Bottom-right corner diagonals (going up-left)
    for start_x in range(max(0, width - height - 3), width):
        diagonal = []
        for offset in range(max_walls):
            x = start_x + offset
            y = height - 1 - offset
            if 0 <= x < width and 0 <= y < height and grid[y, x] == 0:
                diagonal.append((x, y))
        if len(diagonal) >= max_walls:
            diagonals.append(diagonal[:max_walls])
    
    # Bottom-left corner diagonals (going up-right)
    for start_x in range(min(height + 3, width)):
        diagonal = []
        for offset in range(max_walls):
            x = start_x - offset
            y = height - 1 - offset
            if 0 <= x < width and 0 <= y < height and grid[y, x] == 0:
                diagonal.append((x, y))
        if len(diagonal) >= max_walls:
            diagonals.append(diagonal[:max_walls])
    
    return diagonals


def find_strategic_cells(grid):
    """Find cells that are likely to be good wall positions."""
    height, width = grid.shape
    strategic = set()
    
    # Find cells adjacent to fire
    for y in range(height):
        for x in range(width):
            if grid[y, x] == 2:  # Fire
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and grid[ny, nx] == 0:
                        strategic.add((nx, ny))
    
    # Find doorway/chokepoint cells (blocked on 2-3 sides)
    for y in range(height):
        for x in range(width):
            if grid[y, x] != 0:  # Must be open
                continue
            
            blocked = 0
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= width or ny < 0 or ny >= height or grid[ny, nx] != 0:
                    blocked += 1
            
            if blocked >= 2:  # Chokepoint
                strategic.add((x, y))
    
    # Find cells adjacent to water (good blocking positions)
    for y in range(height):
        for x in range(width):
            if grid[y, x] == 1:  # Water
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height and grid[ny, nx] == 0:
                        strategic.add((nx, ny))
    
    return list(strategic)


def test_wall_configuration(grid, wall_positions):
    """
    Test a wall configuration using the fire_challenge module's test_result.
    
    Returns:
        Number of cells saved
    """
    # Get fresh grid
    map_num = None
    for i in range(10):  # Updated to 0-9 for new maps
        test_grid, _, _ = get_map(map=i)
        if np.array_equal(grid, test_grid):
            map_num = i
            break
    
    if map_num is None:
        # Fallback: simulate manually
        return simulate_fire_manual(grid, wall_positions)
    
    # Use official API
    _, _, _ = get_map(map=map_num)
    if wall_positions:
        place_walls(wall_positions)
    return test_result()


def simulate_fire_manual(grid, wall_positions):
    """Manual fire simulation for fallback."""
    test_grid = grid.copy()
    
    # Place walls
    for x, y in wall_positions:
        if test_grid[y, x] == 0:
            test_grid[y, x] = 3
    
    # BFS fire spread
    fire_queue = deque()
    for y in range(test_grid.shape[0]):
        for x in range(test_grid.shape[1]):
            if test_grid[y, x] == 2:
                fire_queue.append((x, y))
    
    while fire_queue:
        x, y = fire_queue.popleft()
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < test_grid.shape[1] and 
                0 <= ny < test_grid.shape[0] and
                test_grid[ny, nx] == 0):
                test_grid[ny, nx] = 2
                fire_queue.append((nx, ny))
    
    return int(np.sum(test_grid == 0))


def test_single_combination(wall_combo, map_num):
    """
    Test a single wall combination. Worker function for multiprocessing.
    
    Args:
        wall_combo: Tuple of wall positions
        map_num: Map number
        
    Returns:
        (score, wall_combo)
    """
    from fire_challenge import get_map, place_walls, test_result
    
    _, _, _ = get_map(map=map_num)
    if wall_combo:
        place_walls(list(wall_combo))
    score = test_result()
    return score, wall_combo


def exhaustive_search_parallel(grid, map_num, max_walls, candidates, total_open_cells=None):
    """
    Parallel exhaustive search using all CPU cores.
    
    Args:
        grid: The game grid
        map_num: Map number
        max_walls: Maximum walls allowed
        candidates: List of candidate positions
        total_open_cells: Total open cells (for early stopping if we save them all)
    
    Returns:
        (best_score, best_walls)
    """
    # Generate all combinations
    all_combos = [tuple()]  # Start with empty (no walls)
    
    for num_walls in range(1, min(max_walls + 1, len(candidates) + 1)):
        all_combos.extend(combinations(candidates, num_walls))
    
    total_combos = len(all_combos)
    num_cores = cpu_count()
    
    print(f"  Testing {total_combos:,} combinations on {num_cores} CPU cores...")
    
    best_score = 0
    best_walls = []
    
    # Create worker function with fixed map_num
    worker = partial(test_single_combination, map_num=map_num)
    
    # Process in parallel with progress updates
    chunk_size = max(100, total_combos // (num_cores * 10))
    processed = 0
    
    with Pool(processes=num_cores) as pool:
        for i in range(0, total_combos, chunk_size):
            chunk = all_combos[i:i+chunk_size]
            results = pool.map(worker, chunk)
            
            for score, walls in results:
                if score > best_score:
                    best_score = score
                    best_walls = list(walls) if walls else []
                    
                    # Early stopping: if we saved all open cells, we found the perfect solution
                    if total_open_cells and best_score >= total_open_cells:
                        print(f"    ✓ Perfect solution found! Saved all {total_open_cells} cells. Stopping early.")
                        print(f"  Total combinations tested: {processed + len(results)}")
                        return best_score, best_walls
            
            processed += len(chunk)
            if processed % (chunk_size * 5) == 0 or processed >= total_combos:
                print(f"    Progress: {processed:,}/{total_combos:,}, best: {best_score}")
    
    print(f"  Total combinations tested: {total_combos:,}")
    return best_score, best_walls


def exhaustive_search(grid, map_num, max_walls, candidates, total_open_cells=None):
    """
    Sequential exhaustive search (fallback when parallel not available).
    
    Args:
        grid: The game grid
        map_num: Map number
        max_walls: Maximum walls allowed
        candidates: List of candidate positions
        total_open_cells: Total open cells (for early stopping if we save them all)
    
    Returns:
        (best_score, best_walls)
    """
    best_score = 0
    best_walls = []
    total_tested = 0
    
    # Try all combinations from 0 to max_walls
    for num_walls in range(0, min(max_walls + 1, len(candidates) + 1)):
        if num_walls == 0:
            # Test no walls
            _, _, _ = get_map(map=map_num)
            score = test_result()
            if score > best_score:
                best_score = score
                best_walls = []
            total_tested += 1
        else:
            for wall_combo in combinations(candidates, num_walls):
                _, _, _ = get_map(map=map_num)
                place_walls(list(wall_combo))
                score = test_result()
                
                if score > best_score:
                    best_score = score
                    best_walls = list(wall_combo)
                    
                    # Early stopping: if we saved all open cells, we found the perfect solution
                    if total_open_cells and best_score >= total_open_cells:
                        print(f"  ✓ Perfect solution found! Saved all {total_open_cells} cells. Stopping early.")
                        print(f"  Total combinations tested: {total_tested}")
                        return best_score, best_walls
                
                total_tested += 1
                
                # Progress indicator for large searches
                if total_tested % 1000 == 0:
                    print(f"  Tested {total_tested:,} combinations, best: {best_score}")
    
    print(f"  Total combinations tested: {total_tested:,}")
    return best_score, best_walls


def solve_fire_challenge(map_num=0, visualize=True, use_parallel=True):
    """
    Solve the fire challenge using advanced optimization.
    
    Args:
        map_num: Map number (0-9)
        visualize: Whether to show visualization
        use_parallel: Whether to use multiprocessing (faster on multi-core CPUs)
    """
    # Get the map
    grid, max_walls, map_name = get_map(map=map_num)
    
    print(f"\n{'='*60}")
    print(f"Map {map_num} - {map_name}")
    print(f"{'='*60}")
    print(f"Grid size: {grid.shape}")
    print(f"Maximum walls: {max_walls}")
    
    # Count total open cells
    total_open_cells = int(np.sum(grid == 0))
    print(f"Total open cells: {total_open_cells}")
    
    # Get all open cells
    all_open = find_all_open_cells(grid)
    print(f"Total open positions: {len(all_open)}")
    
    # Get strategic cells (likely good positions)
    strategic = find_strategic_cells(grid)
    print(f"Strategic positions identified: {len(strategic)}")
    
    # Check for pre-computed diagonal patterns (for corner protection)
    diagonals = generate_diagonal_candidates(grid, max_walls)
    print(f"Diagonal patterns generated: {len(diagonals)}")
    
    # Calculate search space size efficiently
    def count_combinations(n, k):
        from math import comb
        return sum(comb(n, r) for r in range(min(k + 1, n + 1)))
    
    strategic_combos = count_combinations(len(strategic), max_walls)
    
    print(f"\nEstimated combinations to test: {strategic_combos:,}")
    print(f"Available CPU cores: {cpu_count()}")
    
    # Choose search strategy based on problem size
    # For small grids, search ALL open cells for better results
    all_open_combos = count_combinations(len(all_open), max_walls)
    
    if all_open_combos <= 50000:
        print(f"Strategy: Using ALL {len(all_open)} open cells (comprehensive search)")
        candidates = all_open
        actual_combos = all_open_combos
    elif len(strategic) > 30 and max_walls <= 5:
        print(f"Strategy: Using all {len(all_open)} open cells (strategic too broad)")
        candidates = all_open
        actual_combos = all_open_combos
    else:
        # Use strategic cells but ensure we have enough to find good patterns
        if strategic_combos > 1000000:
            print(f"Strategy: Using top strategic cells (filtered for performance)")
            # For very large strategic sets, prioritize edge cells and diagonals
            edge_cells = [c for c in strategic if c[0] == 0 or c[0] == grid.shape[1]-1 or c[1] == 0 or c[1] == grid.shape[0]-1]
            candidates = edge_cells if len(edge_cells) >= max_walls else strategic[:100]
            actual_combos = count_combinations(len(candidates), max_walls)
        else:
            candidates = strategic
            actual_combos = strategic_combos
    
    print(f"Final combinations to test: {actual_combos:,}")
    
    # First, try pre-computed diagonal patterns (fast check for corner strategies)
    if diagonals:
        print(f"\nTesting {len(diagonals)} pre-computed diagonal patterns...")
        best_diagonal_score = 0
        best_diagonal_walls = []
        
        for diagonal in diagonals:
            grid_test, _, _ = get_map(map=map_num)
            place_walls(diagonal)
            score = test_result()
            if score > best_diagonal_score:
                best_diagonal_score = score
                best_diagonal_walls = diagonal
        
        print(f"  Best diagonal: {best_diagonal_score} cells saved")
        
        # If diagonal is promising, use it as baseline
        if best_diagonal_score > 0:
            best_score = best_diagonal_score
            best_walls = best_diagonal_walls
            print(f"  Using diagonal as baseline solution")
    else:
        best_score = 0
        best_walls = []
    
    # If we already have a great diagonal solution, we can skip exhaustive search for huge spaces
    if best_score > total_open_cells * 0.1 and actual_combos > 1000000:
        print(f"\nSkipping exhaustive search (diagonal found {best_score} cells, search space too large)")
    else:
        # Choose parallel vs sequential
        if use_parallel and cpu_count() > 1:
            if actual_combos <= 500000:  # Increased threshold for better results
                print(f"\nStrategy: PARALLEL exhaustive search ({cpu_count()} cores)")
                search_score, search_walls = exhaustive_search_parallel(grid, map_num, max_walls, candidates, total_open_cells)
                if search_score > best_score:
                    best_score = search_score
                    best_walls = search_walls
            else:
                # For very large search spaces, reduce wall count
                print(f"\nStrategy: PARALLEL with reduced walls (too many combos: {actual_combos:,})")
                reduced_walls = min(max_walls, 5)  # Allow 5 walls minimum
                search_score, search_walls = exhaustive_search_parallel(grid, map_num, reduced_walls, candidates, total_open_cells)
                if search_score > best_score:
                    best_score = search_score
                    best_walls = search_walls
        else:
            if actual_combos <= 10000:
                print("\nStrategy: Sequential exhaustive search")
                search_score, search_walls = exhaustive_search(grid, map_num, max_walls, candidates, total_open_cells)
                if search_score > best_score:
                    best_score = search_score
                    best_walls = search_walls
            else:
                print(f"\nStrategy: Sequential with reduced walls (too many combos: {actual_combos:,})")
                reduced_walls = min(max_walls, 4)
                search_score, search_walls = exhaustive_search(grid, map_num, reduced_walls, candidates, total_open_cells)
                if search_score > best_score:
                    best_score = search_score
                    best_walls = search_walls
    
    # Calculate final results
    percentage = (best_score / total_open_cells * 100) if total_open_cells > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Cells saved: {best_score}/{total_open_cells} ({percentage:.1f}%)")
    print(f"Walls used: {len(best_walls)}/{max_walls}")
    print(f"Wall positions: {best_walls}")
    
    if visualize:
        # Apply solution and visualize
        grid, _, _ = get_map(map=map_num)
        if strategic:
            highlight_cells(strategic[:min(30, len(strategic))], level=1)
        if best_walls:
            highlight_cells(best_walls, level=2)
            place_walls(best_walls)
        
        print("\nLaunching visualization...")
        visualize_result()
    
    return best_score, total_open_cells, best_walls


if __name__ == "__main__":
    from fire_challenge import get_available_maps
    
    print("Sam's Fire Challenge Solver - Optimized with Multiprocessing")
    print("=" * 60)
    print(f"Available CPU cores: {cpu_count()}")
    
    print("\nAvailable maps:")
    available_maps = get_available_maps()
    for num, name in available_maps:
        print(f"  {num}: {name}")
    
    map_choice = input("\nEnter map number (or press Enter for map 0): ").strip()
    
    if map_choice.isdigit():
        map_num = int(map_choice)
        if 0 <= map_num < len(available_maps):
            solve_fire_challenge(map_num=map_num, use_parallel=True)
        else:
            print("Invalid map number. Using map 0.")
            solve_fire_challenge(map_num=0, use_parallel=True)
    else:
        print("Using map 0...")
        solve_fire_challenge(map_num=0, use_parallel=True)
