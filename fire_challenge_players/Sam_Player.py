"""
Sam's Fire Challenge Player - Smart Optimization Algorithm
Sam Mirazi 1-21-2026 (v3 - Performance Optimized)

Strategy:
1. Calculate "protection value" of each cell using flood-fill
2. Use greedy algorithm to quickly find a good solution
3. Use local search to improve the greedy solution
4. Only fall back to exhaustive search for small problems

This approach is O(n*k) instead of O(n^k) - orders of magnitude faster!
"""

from itertools import combinations
from collections import deque
from multiprocessing import Pool, cpu_count
from functools import partial
import numpy as np
from fire_challenge import (
    FireChallenge,
    get_map,
    place_walls,
    test_result,
    highlight_cells,
    visualize_result
)


# ============================================================================
# Core Utility Functions
# ============================================================================

def find_fire_positions(grid):
    """Find all initial fire positions in the grid."""
    fire_positions = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 2:
                fire_positions.append((x, y))
    return fire_positions


def find_all_open_cells(grid):
    """Find all open cells in the grid."""
    open_cells = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 0:
                open_cells.append((x, y))
    return open_cells


# Cache for fire simulation results
_fire_simulation_cache = {}
_cache_hits = 0
_cache_misses = 0

def clear_simulation_cache():
    """Clear the simulation cache. Call this when starting a new map."""
    global _fire_simulation_cache, _cache_hits, _cache_misses
    _fire_simulation_cache.clear()
    _cache_hits = 0
    _cache_misses = 0

def get_cache_stats():
    """Get cache performance statistics."""
    total = _cache_hits + _cache_misses
    hit_rate = (_cache_hits / total * 100) if total > 0 else 0
    return {
        'hits': _cache_hits,
        'misses': _cache_misses,
        'total': total,
        'hit_rate': hit_rate,
        'cache_size': len(_fire_simulation_cache)
    }

def simulate_fire_fast(grid, wall_positions=None):
    """
    Fast fire simulation with caching. Returns number of cells saved.
    Uses numpy for speed + LRU cache for duplicate simulations.
    
    Caching gives 2-10x speedup by avoiding redundant BFS simulations.
    """
    global _cache_hits, _cache_misses
    
    # Create cache key: grid shape/data + sorted wall positions
    # Using grid.tobytes() is faster than hashing individual cells
    grid_key = grid.tobytes()
    walls_key = tuple(sorted(wall_positions)) if wall_positions else ()
    cache_key = (grid_key, walls_key)
    
    # Check cache first
    if cache_key in _fire_simulation_cache:
        _cache_hits += 1
        return _fire_simulation_cache[cache_key]
    
    _cache_misses += 1
    
    # Cache miss - run simulation
    test_grid = grid.copy()

    # Place walls
    if wall_positions:
        for x, y in wall_positions:
            if 0 <= y < test_grid.shape[0] and 0 <= x < test_grid.shape[1]:
                if test_grid[y, x] == 0:
                    test_grid[y, x] = 3

    height, width = test_grid.shape

    # BFS fire spread
    fire_queue = deque()
    for y in range(height):
        for x in range(width):
            if test_grid[y, x] == 2:
                fire_queue.append((x, y))

    while fire_queue:
        x, y = fire_queue.popleft()
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if test_grid[ny, nx] == 0:
                    test_grid[ny, nx] = 2
                    fire_queue.append((nx, ny))

    result = int(np.sum(test_grid == 0))
    
    # Store in cache
    _fire_simulation_cache[cache_key] = result
    
    return result


# ============================================================================
# Smart Value Calculation
# ============================================================================

def calculate_cell_protection_value(grid, cell, fire_positions):
    """
    Calculate how many cells would be protected if we place a wall at 'cell'.
    This is the KEY insight - we measure actual protection value, not heuristics.
    """
    x, y = cell
    if grid[y, x] != 0:
        return 0

    # Baseline: cells saved without this wall
    baseline = simulate_fire_fast(grid, None)

    # With wall: cells saved with this wall
    with_wall = simulate_fire_fast(grid, [cell])

    return with_wall - baseline


def calculate_all_protection_values(grid):
    """
    Calculate protection value for all open cells.
    Returns dict of {(x,y): value}
    """
    fire_positions = find_fire_positions(grid)
    open_cells = find_all_open_cells(grid)

    values = {}
    for cell in open_cells:
        values[cell] = calculate_cell_protection_value(grid, cell, fire_positions)

    return values


def calculate_marginal_value(grid, cell, existing_walls):
    """
    Calculate the MARGINAL value of adding 'cell' to existing walls.
    This accounts for diminishing returns when walls overlap in protection.
    """
    x, y = cell
    if grid[y, x] != 0:
        return 0
    if cell in existing_walls:
        return 0

    # Current score with existing walls
    current_score = simulate_fire_fast(grid, list(existing_walls))

    # Score with new wall added
    new_walls = list(existing_walls) + [cell]
    new_score = simulate_fire_fast(grid, new_walls)

    return new_score - current_score


# ============================================================================
# Greedy Algorithm (Fast!)
# ============================================================================

def greedy_solve(grid, max_walls, candidates=None):
    """
    Greedy algorithm: iteratively pick the wall with highest marginal value.

    Time complexity: O(max_walls * num_candidates) - MUCH faster than brute force!
    """
    if candidates is None:
        candidates = find_all_open_cells(grid)

    selected_walls = []
    remaining_candidates = set(candidates)

    for wall_num in range(max_walls):
        best_cell = None
        best_value = -1

        # Find the cell with highest marginal value
        for cell in remaining_candidates:
            value = calculate_marginal_value(grid, cell, selected_walls)
            if value > best_value:
                best_value = value
                best_cell = cell

        # If no improvement possible, stop early
        if best_value <= 0:
            break

        selected_walls.append(best_cell)
        remaining_candidates.remove(best_cell)

    final_score = simulate_fire_fast(grid, selected_walls)
    return final_score, selected_walls


# ============================================================================
# Local Search Optimization
# ============================================================================

def local_search_improve(grid, initial_walls, max_walls, candidates=None, max_iterations=100):
    """
    Improve a solution using local search (swap one wall for another).
    This can escape local optima that greedy might get stuck in.
    """
    if candidates is None:
        candidates = find_all_open_cells(grid)

    candidates_set = set(candidates)
    current_walls = list(initial_walls)
    current_score = simulate_fire_fast(grid, current_walls)

    improved = True
    iterations = 0

    while improved and iterations < max_iterations:
        improved = False
        iterations += 1

        # Try removing each wall and adding a different one
        for i, wall_to_remove in enumerate(current_walls):
            # Try each candidate as replacement
            for new_wall in candidates_set:
                if new_wall in current_walls:
                    continue

                # Create new wall set
                new_walls = current_walls[:i] + current_walls[i+1:] + [new_wall]
                new_score = simulate_fire_fast(grid, new_walls)

                if new_score > current_score:
                    current_walls = new_walls
                    current_score = new_score
                    improved = True
                    break

            if improved:
                break

        # Also try adding a wall if we haven't used all
        if not improved and len(current_walls) < max_walls:
            for new_wall in candidates_set:
                if new_wall in current_walls:
                    continue

                new_walls = current_walls + [new_wall]
                new_score = simulate_fire_fast(grid, new_walls)

                if new_score > current_score:
                    current_walls = new_walls
                    current_score = new_score
                    improved = True
                    break

    return current_score, current_walls


# ============================================================================
# Smart Candidate Selection
# ============================================================================

def find_high_value_candidates(grid, top_n=50):
    """
    Find the most promising wall candidates based on protection value.
    This dramatically reduces the search space for any further optimization.
    """
    values = calculate_all_protection_values(grid)

    # Sort by value, highest first
    sorted_cells = sorted(values.keys(), key=lambda c: values[c], reverse=True)

    # Take top N, but ensure we include all cells with value > 0
    high_value = [c for c in sorted_cells if values[c] > 0]

    if len(high_value) > top_n:
        return high_value[:top_n]
    return high_value if high_value else sorted_cells[:top_n]


def find_barrier_extension_candidates(grid):
    """
    Find cells that extend existing barriers (water cells or edges).
    These are often the most valuable positions.
    """
    height, width = grid.shape
    candidates = []

    for y in range(height):
        for x in range(width):
            if grid[y, x] != 0:
                continue

            # Check if adjacent to water or edge
            adjacent_barrier = False
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    adjacent_barrier = True  # Edge
                elif grid[ny, nx] == 1:
                    adjacent_barrier = True  # Water

            if adjacent_barrier:
                candidates.append((x, y))

    return candidates


def find_fire_containment_candidates(grid):
    """
    Find cells that could help contain fire spread.
    Includes: cells adjacent to fire, cells forming rings around fire.
    """
    height, width = grid.shape
    fire_positions = find_fire_positions(grid)
    candidates = set()

    # Add all cells adjacent to fire (distance 1)
    for fx, fy in fire_positions:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = fx + dx, fy + dy
            if 0 <= nx < width and 0 <= ny < height and grid[ny, nx] == 0:
                candidates.add((nx, ny))

    # Add cells at distance 2 from fire (second ring)
    for fx, fy in fire_positions:
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if abs(dx) + abs(dy) <= 2:  # Manhattan distance <= 2
                    nx, ny = fx + dx, fy + dy
                    if 0 <= nx < width and 0 <= ny < height and grid[ny, nx] == 0:
                        candidates.add((nx, ny))

    return list(candidates)


# ============================================================================
# Chokepoint and Gap Detection (for maps with funnels/bottlenecks)
# ============================================================================

def find_chokepoints(grid, max_walls):
    """
    Find chokepoints - narrow passages where few walls can block large areas.

    A chokepoint is a column (or row) where the number of open cells is small,
    meaning walls placed there can block fire from spreading to the other side.
    """
    height, width = grid.shape
    chokepoint_candidates = []

    # Analyze each column for vertical chokepoints
    for x in range(width):
        open_cells_in_col = []
        for y in range(height):
            if grid[y, x] == 0:
                open_cells_in_col.append((x, y))

        # If this column has few open cells (potential chokepoint)
        if 0 < len(open_cells_in_col) <= max_walls:
            chokepoint_candidates.append(open_cells_in_col)

    # Analyze each row for horizontal chokepoints
    for y in range(height):
        open_cells_in_row = []
        for x in range(width):
            if grid[y, x] == 0:
                open_cells_in_row.append((x, y))

        # If this row has few open cells (potential chokepoint)
        if 0 < len(open_cells_in_row) <= max_walls:
            chokepoint_candidates.append(open_cells_in_row)

    return chokepoint_candidates


def find_gaps_in_barriers(grid, max_walls):
    """
    Find gaps in water barriers that could be closed with walls.

    Scans horizontally and vertically for patterns like:
    [water] [open] [open] [water] - a gap of 2 that could be closed
    """
    height, width = grid.shape
    gap_candidates = []

    # Find horizontal gaps (scan each row)
    for y in range(height):
        in_gap = False
        gap_start = -1
        gap_cells = []

        for x in range(width):
            cell = grid[y, x]

            if cell == 1:  # Water - potential barrier
                if in_gap and gap_cells:
                    # End of gap - check if it's small enough to close
                    if len(gap_cells) <= max_walls:
                        gap_candidates.append(gap_cells.copy())
                in_gap = False
                gap_cells = []
                gap_start = x
            elif cell == 0:  # Open cell
                if gap_start >= 0:  # We've seen water before
                    in_gap = True
                    gap_cells.append((x, y))
            else:  # Fire or wall
                in_gap = False
                gap_cells = []

        # Check if gap ends at edge (edge acts as barrier)
        if in_gap and gap_cells and len(gap_cells) <= max_walls:
            gap_candidates.append(gap_cells.copy())

    # Find vertical gaps (scan each column)
    for x in range(width):
        in_gap = False
        gap_start = -1
        gap_cells = []

        for y in range(height):
            cell = grid[y, x]

            if cell == 1:  # Water
                if in_gap and gap_cells:
                    if len(gap_cells) <= max_walls:
                        gap_candidates.append(gap_cells.copy())
                in_gap = False
                gap_cells = []
                gap_start = y
            elif cell == 0:  # Open
                if gap_start >= 0:
                    in_gap = True
                    gap_cells.append((x, y))
            else:  # Fire or wall
                in_gap = False
                gap_cells = []

        if in_gap and gap_cells and len(gap_cells) <= max_walls:
            gap_candidates.append(gap_cells.copy())

    return gap_candidates


def find_vertical_barriers(grid, max_walls):
    """
    Find vertical line barriers that could cut off fire spread.

    For maps like "Big Funnel" where fire comes from one side,
    a vertical wall line in the middle can protect the other side.
    """
    height, width = grid.shape
    fire_positions = find_fire_positions(grid)

    if not fire_positions:
        return []

    # Determine which side fire is on
    fire_cols = [fx for fx, fy in fire_positions]
    avg_fire_col = sum(fire_cols) / len(fire_cols)

    barriers = []

    # Try vertical barriers at different columns
    # Focus on columns away from fire (in the middle or opposite side)
    start_col = 1 if avg_fire_col < width / 2 else width - 2
    end_col = width - 1 if avg_fire_col < width / 2 else 0
    step = 1 if start_col < end_col else -1

    for x in range(start_col, end_col, step):
        barrier = []
        for y in range(height):
            if grid[y, x] == 0:
                barrier.append((x, y))

        # Only consider if it's a feasible barrier
        if 0 < len(barrier) <= max_walls:
            barriers.append(barrier)

    return barriers


def find_horizontal_barriers(grid, max_walls):
    """
    Find horizontal line barriers that could cut off fire spread.
    """
    height, width = grid.shape
    fire_positions = find_fire_positions(grid)

    if not fire_positions:
        return []

    # Determine which side fire is on
    fire_rows = [fy for fx, fy in fire_positions]
    avg_fire_row = sum(fire_rows) / len(fire_rows)

    barriers = []

    # Try horizontal barriers at different rows
    start_row = 1 if avg_fire_row < height / 2 else height - 2
    end_row = height - 1 if avg_fire_row < height / 2 else 0
    step = 1 if start_row < end_row else -1

    for y in range(start_row, end_row, step):
        barrier = []
        for x in range(width):
            if grid[y, x] == 0:
                barrier.append((x, y))

        if 0 < len(barrier) <= max_walls:
            barriers.append(barrier)

    return barriers


def find_partial_barriers_with_water(grid, max_walls):
    """
    Find barriers that use water cells to reduce wall count.

    Looks for rows/columns where water already blocks part of the line,
    so fewer walls are needed to complete the barrier.
    """
    height, width = grid.shape
    partial_barriers = []

    # Check each column - find ones with water that could be completed
    for x in range(width):
        open_cells = []
        has_water = False

        for y in range(height):
            if grid[y, x] == 0:
                open_cells.append((x, y))
            elif grid[y, x] == 1:
                has_water = True

        # If column has water AND few open cells, it's a good partial barrier
        if has_water and 0 < len(open_cells) <= max_walls:
            partial_barriers.append(open_cells)

    # Check each row
    for y in range(height):
        open_cells = []
        has_water = False

        for x in range(width):
            if grid[y, x] == 0:
                open_cells.append((x, y))
            elif grid[y, x] == 1:
                has_water = True

        if has_water and 0 < len(open_cells) <= max_walls:
            partial_barriers.append(open_cells)

    return partial_barriers


def count_cells_on_side(grid, barrier_cells, fire_positions):
    """
    Count how many open cells are on the far side of a barrier from fire.
    This helps evaluate barrier effectiveness.
    """
    if not barrier_cells or not fire_positions:
        return 0

    height, width = grid.shape

    # Create a test grid with the barrier in place
    test_grid = grid.copy()
    for x, y in barrier_cells:
        if test_grid[y, x] == 0:
            test_grid[y, x] = 3  # Wall

    # BFS from fire to find reachable cells
    reachable = set()
    queue = deque(fire_positions)
    for pos in fire_positions:
        reachable.add(pos)

    while queue:
        x, y = queue.popleft()
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in reachable and test_grid[ny, nx] == 0:
                    reachable.add((nx, ny))
                    queue.append((nx, ny))

    # Count unreachable open cells (protected by barrier)
    protected = 0
    for y in range(height):
        for x in range(width):
            if grid[y, x] == 0 and (x, y) not in reachable:
                protected += 1

    return protected


# ============================================================================
# Barrier Completion Algorithm
# ============================================================================

def find_diagonal_barriers(grid, max_walls):
    """
    Find diagonal barrier patterns that could seal off corners.
    This is KEY for maps like "Sam's Bane" where water cells start a diagonal.
    """
    height, width = grid.shape
    barriers = []

    # Find all water cells
    water_cells = []
    for y in range(height):
        for x in range(width):
            if grid[y, x] == 1:
                water_cells.append((x, y))

    # For each water cell, try to extend diagonal barriers to edges
    for wx, wy in water_cells:
        # Try extending toward each corner
        # Upper-right diagonal (going up-right from water)
        for direction in [(1, -1), (1, 1), (-1, -1), (-1, 1)]:
            dx, dy = direction
            diagonal = []
            x, y = wx, wy

            # Walk in the direction until we hit an edge
            while True:
                x += dx
                y += dy
                if x < 0 or x >= width or y < 0 or y >= height:
                    break
                if grid[y, x] == 0:  # Open cell - potential wall
                    diagonal.append((x, y))
                elif grid[y, x] == 1:  # Another water cell - helps!
                    continue
                else:
                    break  # Fire or something else

            if diagonal and len(diagonal) <= max_walls:
                barriers.append(diagonal)

            # Also try the opposite direction from the water
            diagonal_opposite = []
            x, y = wx, wy
            while True:
                x -= dx
                y -= dy
                if x < 0 or x >= width or y < 0 or y >= height:
                    break
                if grid[y, x] == 0:
                    diagonal_opposite.append((x, y))
                elif grid[y, x] == 1:
                    continue
                else:
                    break

            if diagonal_opposite and len(diagonal_opposite) <= max_walls:
                barriers.append(diagonal_opposite)

    # Also generate diagonal barriers from corners (edge-to-edge)
    for start_row in range(height):
        for direction in [(1, 1), (1, -1)]:  # Down-right, Down-left
            diagonal = []
            x, y = 0 if direction[0] > 0 else width - 1, start_row

            while 0 <= x < width and 0 <= y < height:
                if grid[y, x] == 0:
                    diagonal.append((x, y))
                x += direction[0]
                y += direction[1]

            if diagonal and len(diagonal) <= max_walls:
                barriers.append(diagonal)

    for start_col in range(width):
        for direction in [(1, 1), (-1, 1)]:  # Right-down, Left-down
            diagonal = []
            x, y = start_col, 0

            while 0 <= x < width and 0 <= y < height:
                if grid[y, x] == 0:
                    diagonal.append((x, y))
                x += direction[0]
                y += direction[1]

            if diagonal and len(diagonal) <= max_walls:
                barriers.append(diagonal)

    return barriers


def find_barrier_completions(grid, max_walls):
    """
    Find ways to complete partial barriers formed by water cells and edges.
    Returns list of wall combinations that form complete barriers.

    Now includes: diagonal barriers, chokepoints, gaps, vertical/horizontal barriers.
    """
    height, width = grid.shape
    completions = []
    seen_barriers = set()  # Avoid duplicates
    baseline = simulate_fire_fast(grid, None)  # Cache baseline

    def add_barrier(barrier):
        """Add barrier if not seen before and it saves cells."""
        if not barrier or len(barrier) > max_walls:
            return
        key = tuple(sorted(barrier))
        if key in seen_barriers:
            return
        seen_barriers.add(key)
        score = simulate_fire_fast(grid, barrier)
        if score > baseline:  # Only add if better than baseline
            completions.append((score, barrier))

    # Get diagonal barriers (good for corner maps)
    diagonals = find_diagonal_barriers(grid, max_walls)
    for diagonal in diagonals:
        add_barrier(diagonal)

    # Get chokepoints (narrow passages)
    chokepoints = find_chokepoints(grid, max_walls)
    for chokepoint in chokepoints:
        add_barrier(chokepoint)

    # Get gaps in water barriers
    gaps = find_gaps_in_barriers(grid, max_walls)
    for gap in gaps:
        add_barrier(gap)

    # Get vertical barriers (for funnel maps with fire on one side)
    vertical_barriers = find_vertical_barriers(grid, max_walls)
    for barrier in vertical_barriers:
        add_barrier(barrier)

    # Get horizontal barriers
    horizontal_barriers = find_horizontal_barriers(grid, max_walls)
    for barrier in horizontal_barriers:
        add_barrier(barrier)

    # Get partial barriers that use existing water
    partial_barriers = find_partial_barriers_with_water(grid, max_walls)
    for barrier in partial_barriers:
        add_barrier(barrier)

    # Sort by score (best first)
    completions.sort(key=lambda x: x[0], reverse=True)

    return completions


def combine_barrier_completions(grid, max_walls, completions, top_n=10):
    """
    Try combining top barrier completions to find better solutions.
    Often two smaller barriers together save more than either alone.
    """
    if not completions:
        return 0, []

    best_score = 0
    best_walls = []

    # Sort by score and take top N
    top_completions = sorted(completions, key=lambda x: x[0], reverse=True)[:top_n]

    # Try each completion alone
    for score, walls in top_completions:
        if score > best_score:
            best_score = score
            best_walls = walls

    # Try combining pairs of completions
    for i, (score1, walls1) in enumerate(top_completions):
        for j, (score2, walls2) in enumerate(top_completions[i+1:], i+1):
            # Combine walls, removing duplicates
            combined = list(set(walls1 + walls2))
            if len(combined) <= max_walls:
                combined_score = simulate_fire_fast(grid, combined)
                if combined_score > best_score:
                    best_score = combined_score
                    best_walls = combined

    return best_score, best_walls


def find_fire_containment_walls(grid, max_walls):
    """
    Find walls that completely surround/contain all fire cells.
    This is often the optimal solution when fire is clustered.

    Returns list of (score, walls) tuples for different containment options.
    """
    height, width = grid.shape
    fire_positions = set()

    for y in range(height):
        for x in range(width):
            if grid[y, x] == 2:
                fire_positions.add((x, y))

    if not fire_positions:
        return []

    # Find all cells adjacent to fire that are open (potential containment walls)
    containment_walls = set()
    for fx, fy in fire_positions:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = fx + dx, fy + dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny, nx] == 0:  # Open cell adjacent to fire
                    containment_walls.add((nx, ny))

    containment_list = list(containment_walls)
    results = []

    # If we can contain all fire with available walls, try it
    if len(containment_list) <= max_walls:
        score = simulate_fire_fast(grid, containment_list)
        results.append((score, containment_list))

    # Also try subsets if containment needs fewer walls than max
    # (greedy removal of least valuable walls)
    if len(containment_list) > 1:
        current_walls = containment_list.copy()
        current_score = simulate_fire_fast(grid, current_walls)

        # Try removing walls one at a time to see if we can do better with fewer
        for _ in range(min(3, len(current_walls) - 1)):
            best_removal = None
            best_score_after = current_score

            for wall in current_walls:
                test_walls = [w for w in current_walls if w != wall]
                test_score = simulate_fire_fast(grid, test_walls)
                # Keep removal if score doesn't drop much (wall wasn't critical)
                if test_score >= current_score - 1:
                    if best_removal is None or test_score > best_score_after:
                        best_removal = wall
                        best_score_after = test_score

            if best_removal and best_score_after >= current_score - 2:
                current_walls = [w for w in current_walls if w != best_removal]
                current_score = best_score_after
                if len(current_walls) <= max_walls:
                    results.append((current_score, current_walls.copy()))

    return results


def extend_solution_greedily(grid, initial_walls, max_walls, candidates):
    """
    Extend a partial solution by greedily adding more walls.
    This helps find better solutions when we have a good starting point.
    """
    current_walls = list(initial_walls)
    current_score = simulate_fire_fast(grid, current_walls)
    candidates_set = set(candidates) - set(current_walls)

    while len(current_walls) < max_walls and candidates_set:
        best_addition = None
        best_improvement = 0

        for cell in candidates_set:
            test_walls = current_walls + [cell]
            test_score = simulate_fire_fast(grid, test_walls)
            improvement = test_score - current_score

            if improvement > best_improvement:
                best_improvement = improvement
                best_addition = cell

        if best_addition is None or best_improvement <= 0:
            break

        current_walls.append(best_addition)
        candidates_set.remove(best_addition)
        current_score += best_improvement

    return current_score, current_walls


def try_wall_combinations_smart(grid, max_walls, candidates, max_combos=10000):
    """
    Try wall combinations but smarter - start with likely good ones.
    Uses iterative deepening: try 1 wall, then 2, etc.
    Stop early if we find a great solution.
    """
    best_score = 0
    best_walls = []
    total_tested = 0

    total_open = int(np.sum(grid == 0))

    for num_walls in range(1, max_walls + 1):
        if num_walls > len(candidates):
            break

        # Limit combinations per level
        max_per_level = max_combos // max_walls

        count = 0
        for wall_combo in combinations(candidates, num_walls):
            score = simulate_fire_fast(grid, list(wall_combo))
            if score > best_score:
                best_score = score
                best_walls = list(wall_combo)

                # Early exit if we found a very good solution
                if best_score > total_open * 0.5:
                    return best_score, best_walls, total_tested

            total_tested += 1
            count += 1
            if count >= max_per_level:
                break

    return best_score, best_walls, total_tested


# ============================================================================
# Exhaustive Search (for small problems only)
# ============================================================================

def exhaustive_search_small(grid, max_walls, candidates, show_progress=True):
    """
    Exhaustive search for small problems. Only use when feasible.
    Shows progress indicator for long searches.
    """
    from math import comb
    import sys

    best_score = 0
    best_walls = []

    # Calculate total combinations for progress reporting
    total_combos = sum(comb(len(candidates), r) for r in range(min(max_walls + 1, len(candidates) + 1)))

    total_tested = 0
    last_percent = -1
    progress_interval = max(1, total_combos // 100)  # Update every 1%

    for num_walls in range(max_walls + 1):
        if num_walls > len(candidates):
            break

        for wall_combo in combinations(candidates, num_walls):
            score = simulate_fire_fast(grid, list(wall_combo))
            if score > best_score:
                best_score = score
                best_walls = list(wall_combo)
            total_tested += 1

            # Show progress
            if show_progress and total_tested % progress_interval == 0:
                percent = (total_tested * 100) // total_combos
                if percent != last_percent:
                    print(f"\r  Progress: {total_tested:,}/{total_combos:,} ({percent}%) - best: {best_score}", end="", flush=True)
                    last_percent = percent

    if show_progress and total_combos > progress_interval:
        print(f"\r  Progress: {total_tested:,}/{total_combos:,} (100%) - best: {best_score}   ")

    return best_score, best_walls, total_tested


# ============================================================================
# Main Solver
# ============================================================================

def solve_fire_challenge(map_num=0, visualize=True, use_parallel=True):
    """
    Smart solver that uses greedy + local search for speed,
    with optional exhaustive refinement for small problems.
    """
    # Clear cache for new map
    clear_simulation_cache()
    
    # Get the map
    grid, max_walls, map_name = get_map(map=map_num)

    print(f"\n{'='*60}")
    print(f"Map {map_num} - {map_name}")
    print(f"{'='*60}")
    print(f"Grid size: {grid.shape}")
    print(f"Maximum walls: {max_walls}")

    # Count cells
    total_open = int(np.sum(grid == 0))
    baseline_saved = simulate_fire_fast(grid, None)

    print(f"Total open cells: {total_open}")
    print(f"Baseline (no walls): {baseline_saved} cells saved")

    # Get all open cells
    all_open = find_all_open_cells(grid)

    # Calculate search space
    from math import comb
    def count_combinations(n, k):
        return sum(comb(n, r) for r in range(min(k + 1, n + 1)))

    total_combos = count_combinations(len(all_open), max_walls)
    print(f"\nBrute force would test: {total_combos:,} combinations")

    # ========================================================================
    # PHASE 0a: Direct Fire Containment (surround fire with walls)
    # ========================================================================
    print(f"\n--- Phase 0a: Fire Containment Strategy ---")

    best_score = baseline_saved
    best_walls = []

    containment_options = find_fire_containment_walls(grid, max_walls)
    if containment_options:
        for score, walls in containment_options:
            print(f"  Containment with {len(walls)} walls: {score} cells saved")
            if score > best_score:
                best_score = score
                best_walls = walls
        if best_score > baseline_saved:
            print(f"Best containment: {best_score} cells saved with {len(best_walls)} walls")
    else:
        print("  Fire cannot be fully contained with available walls")

    # ========================================================================
    # PHASE 0b: Barrier Completion (for maps with water cells)
    # ========================================================================
    print(f"\n--- Phase 0b: Barrier Completion Analysis ---")

    barrier_completions = find_barrier_completions(grid, max_walls)

    if barrier_completions:
        print(f"Found {len(barrier_completions)} potential barrier completions")
        # Try combining barrier completions for better results
        combo_score, combo_walls = combine_barrier_completions(grid, max_walls, barrier_completions, top_n=15)
        if combo_score > best_score:
            best_score = combo_score
            best_walls = combo_walls
            print(f"Best barrier combination: {best_score} cells saved")
    else:
        print("No water-assisted barriers found")

    # ========================================================================
    # PHASE 1: Greedy solution (very fast)
    # ========================================================================
    print(f"\n--- Phase 1: Greedy Algorithm ---")

    # Get high-value candidates from multiple sources
    high_value = find_high_value_candidates(grid, top_n=60)
    barrier_ext = find_barrier_extension_candidates(grid)
    fire_contain = find_fire_containment_candidates(grid)

    # NEW: Get chokepoint and gap candidates
    chokepoint_cells = set()
    for chokepoint in find_chokepoints(grid, max_walls):
        chokepoint_cells.update(chokepoint)

    gap_cells = set()
    for gap in find_gaps_in_barriers(grid, max_walls):
        gap_cells.update(gap)

    # NEW: Get vertical/horizontal barrier cells (for funnel maps)
    barrier_cells = set()
    for barrier in find_vertical_barriers(grid, max_walls):
        barrier_cells.update(barrier)
    for barrier in find_horizontal_barriers(grid, max_walls):
        barrier_cells.update(barrier)
    for barrier in find_partial_barriers_with_water(grid, max_walls):
        barrier_cells.update(barrier)

    # Combine all candidate sources, prioritizing chokepoints and gaps
    # These are often the most valuable for maps with funnels/bottlenecks
    all_candidates = list(chokepoint_cells | gap_cells | barrier_cells)
    for c in fire_contain:
        if c not in all_candidates:
            all_candidates.append(c)
    for c in high_value + barrier_ext:
        if c not in all_candidates:
            all_candidates.append(c)
    print(f"Identified {len(all_candidates)} promising candidates")
    print(f"  - Chokepoint cells: {len(chokepoint_cells)}")
    print(f"  - Gap cells: {len(gap_cells)}")
    print(f"  - Barrier cells: {len(barrier_cells)}")

    greedy_score, greedy_walls = greedy_solve(grid, max_walls, all_candidates)
    print(f"Greedy solution: {greedy_score} cells saved with {len(greedy_walls)} walls")

    if greedy_score > best_score:
        best_score = greedy_score
        best_walls = greedy_walls

    # ========================================================================
    # PHASE 2: Local search improvement
    # ========================================================================
    print(f"\n--- Phase 2: Local Search Optimization ---")

    improved_score, improved_walls = local_search_improve(
        grid, greedy_walls, max_walls, all_candidates, max_iterations=50
    )

    if improved_score > best_score:
        print(f"Local search improved: {improved_score} cells saved")
        best_score = improved_score
        best_walls = improved_walls
    else:
        print(f"Local search: no improvement found")

    # ========================================================================
    # PHASE 2.5: Extend best solutions greedily
    # ========================================================================
    if best_walls and len(best_walls) < max_walls:
        print(f"\n--- Phase 2.5: Extending Best Solution ---")
        extended_score, extended_walls = extend_solution_greedily(
            grid, best_walls, max_walls, all_candidates
        )
        if extended_score > best_score:
            print(f"Extended solution: {extended_score} cells saved")
            best_score = extended_score
            best_walls = extended_walls
        else:
            print(f"Extension: no improvement")

    # Also try extending top barrier completions
    if barrier_completions:
        for _, barrier_walls in sorted(barrier_completions, key=lambda x: x[0], reverse=True)[:5]:
            if len(barrier_walls) < max_walls:
                ext_score, ext_walls = extend_solution_greedily(
                    grid, barrier_walls, max_walls, all_candidates
                )
                if ext_score > best_score:
                    best_score = ext_score
                    best_walls = ext_walls

    # ========================================================================
    # PHASE 3: Smart combination search
    # ========================================================================
    # Build prioritized candidate list
    # Key insight: fire containment cells should be highest priority since they
    # directly affect fire spread, then barrier completions, then others

    fire_positions = find_fire_positions(grid)
    prioritized = []

    # FIRST: Fire containment cells (directly adjacent to fire sources)
    for c in fire_contain:
        if c not in prioritized:
            prioritized.append(c)

    # SECOND: Cells from successful barrier completions
    barrier_candidates = set()
    if barrier_completions:
        for score, walls in sorted(barrier_completions, key=lambda x: x[0], reverse=True)[:20]:
            barrier_candidates.update(walls)
    for c in barrier_candidates:
        if c not in prioritized:
            prioritized.append(c)

    # THIRD: Cells from current best solution neighborhood
    if best_walls:
        height, width = grid.shape
        for wx, wy in best_walls:
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                nx, ny = wx + dx, wy + dy
                if 0 <= nx < width and 0 <= ny < height and grid[ny, nx] == 0:
                    if (nx, ny) not in prioritized:
                        prioritized.append((nx, ny))

    # FOURTH: Remaining candidates from all_candidates
    for c in all_candidates:
        if c not in prioritized:
            prioritized.append(c)

    candidate_combos = count_combinations(len(prioritized), max_walls)

    # Dynamic candidate limit based on max_walls to keep combinations reasonable
    # Target: under 500k combinations for reasonable runtime
    num_fires = len(fire_positions)
    if max_walls <= 5:
        candidate_limit = 30 + num_fires * 5  # ~175k combos with 30 candidates
    elif max_walls <= 7:
        candidate_limit = 22 + num_fires * 3  # ~500k combos with 25 candidates
    elif max_walls <= 10:
        candidate_limit = 18 + num_fires * 2  # ~600k combos with 20 candidates
    else:
        candidate_limit = 15 + num_fires      # Very high max_walls, be conservative
    candidate_limit = min(candidate_limit, len(prioritized))

    # Skip exhaustive if we already have a very good solution
    if best_score >= total_open * 0.85:
        print(f"\n--- Phase 3: Skipped (excellent solution: {best_score}/{total_open}) ---")
    elif candidate_combos <= 50000:
        print(f"\n--- Phase 3: Exhaustive Search ({candidate_combos:,} combinations) ---")

        exhaustive_score, exhaustive_walls, tested = exhaustive_search_small(
            grid, max_walls, prioritized
        )

        print(f"Exhaustive search: {exhaustive_score} cells saved (tested {tested:,})")

        if exhaustive_score > best_score:
            best_score = exhaustive_score
            best_walls = exhaustive_walls
    elif best_score < total_open * 0.7:
        # If we haven't found a good solution, try harder but with smaller candidate set
        print(f"\n--- Phase 3: Smart Combination Search (best so far: {best_score}) ---")
        print(f"Using {candidate_limit} prioritized candidates (fires: {num_fires})")

        smart_candidates = prioritized[:candidate_limit]
        smart_combos = count_combinations(len(smart_candidates), max_walls)

        if smart_combos <= 500000:
            smart_score, smart_walls, tested = exhaustive_search_small(
                grid, max_walls, smart_candidates
            )
            print(f"Smart search: {smart_score} cells saved (tested {smart_combos:,})")

            if smart_score > best_score:
                best_score = smart_score
                best_walls = smart_walls
        else:
            # If still too many combos, iteratively reduce until manageable
            reduced_limit = candidate_limit
            while reduced_limit > max_walls + 2:
                reduced_combos = count_combinations(reduced_limit, max_walls)
                if reduced_combos <= 500000:
                    break
                reduced_limit -= 2

            reduced = prioritized[:reduced_limit]
            reduced_combos = count_combinations(len(reduced), max_walls)
            print(f"Reduced to {reduced_limit} candidates ({reduced_combos:,} combos)")

            reduced_score, reduced_walls, tested = exhaustive_search_small(
                grid, max_walls, reduced
            )
            print(f"Reduced search: {reduced_score} cells saved (tested {reduced_combos:,})")

            if reduced_score > best_score:
                best_score = reduced_score
                best_walls = reduced_walls
    else:
        print(f"\n--- Phase 3: Skipped (good solution found: {best_score}) ---")

    # ========================================================================
    # Results
    # ========================================================================
    percentage = (best_score / total_open * 100) if total_open > 0 else 0
    
    # Get cache statistics
    cache_stats = get_cache_stats()

    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Cells saved: {best_score}/{total_open} ({percentage:.1f}%)")
    print(f"Walls used: {len(best_walls)}/{max_walls}")
    print(f"Wall positions: {best_walls}")
    print(f"\nCache Performance:")
    print(f"  Simulations: {cache_stats['total']:,} total")
    print(f"  Cache hits: {cache_stats['hits']:,} ({cache_stats['hit_rate']:.1f}%)")
    print(f"  Cache size: {cache_stats['cache_size']:,} entries")
    if cache_stats['hit_rate'] > 0:
        speedup = 1 / (1 - cache_stats['hit_rate']/100)
        print(f"  Estimated speedup: {speedup:.1f}x")

    if visualize:
        # Apply solution and visualize
        grid, _, _ = get_map(map=map_num)

        # Highlight candidates
        if all_candidates:
            highlight_cells(all_candidates[:20], level=1)

        # Highlight and place best walls
        if best_walls:
            highlight_cells(best_walls, level=2)
            place_walls(best_walls)

        print("\nLaunching visualization...")
        visualize_result()

    return best_score, total_open, best_walls


# ============================================================================
# Batch Testing
# ============================================================================

def test_all_maps(visualize=False):
    """Test the solver on all available maps."""
    print("="*60)
    print("TESTING ALL MAPS")
    print("="*60)

    results = []
    available_maps = FireChallenge.get_available_maps()

    for map_num, map_name in available_maps:
        score, total, walls = solve_fire_challenge(map_num, visualize=visualize)
        results.append((map_num, map_name, score, total, walls))

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for map_num, name, score, total, walls in results:
        pct = score/total*100 if total > 0 else 0
        print(f"Map {map_num:2d} - {name:30s}: {score:3d}/{total:3d} ({pct:5.1f}%)")

    return results


if __name__ == "__main__":
    print("Sam's Fire Challenge Solver - Smart Optimization")
    print("=" * 60)
    print("Using: Greedy + Local Search + Limited Exhaustive")
    print(f"Available CPU cores: {cpu_count()}")

    print("\nAvailable maps:")
    available_maps = FireChallenge.get_available_maps()
    for num, name in available_maps:
        print(f"  {num}: {name}")

    print(f"\nEnter map number, 'all' to test all maps, or press Enter for map 0:")
    map_choice = input().strip()

    if map_choice.lower() == 'all':
        test_all_maps(visualize=False)
    elif map_choice.isdigit():
        map_num = int(map_choice)
        if 0 <= map_num < len(available_maps):
            solve_fire_challenge(map_num=map_num)
        else:
            print("Invalid map number. Using map 0.")
            solve_fire_challenge(map_num=0)
    else:
        print("Using map 0...")
        solve_fire_challenge(map_num=0)
