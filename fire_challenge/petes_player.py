"""
Pete's Fire Challenge Player

Algorithm:
1. Find all "interesting" squares:
   - Squares adjacent to initial fire positions
   - "Doorway" squares (blocked on 2-3 sides, open on 1-2 sides)
2. Try every combination of wall placements among interesting squares
3. Pick the best solution
"""

from itertools import combinations
from fire_challenge import (
    get_map,
    get_available_maps,
    place_walls, 
    test_result, 
    highlight_cells,
    visualize_result
)


def find_fire_positions(grid):
    """Find all initial fire positions in the grid."""
    # Note: grids are stored [y,x] but coordinates are given as (x,y) by math convention.
    fire_positions = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 2:  # Fire cell
                fire_positions.append((x, y))
    return fire_positions


def find_adjacent_to_fire(grid, fire_positions):
    """Find all open cells adjacent to fire positions."""
    # Note: grids are stored [y,x] but coordinates are given as (x,y) by math convention.
    height, width = grid.shape
    adjacent = set()
    
    for fx, fy in fire_positions:
        # Check 4 adjacent cells
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = fx + dx, fy + dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny, nx] == 0:  # Open cell
                    adjacent.add((nx, ny))
    
    return list(adjacent)


def is_doorway(grid, x, y):
    """
    Check if a cell is a doorway (blocked on 2-3 sides, open on 1-2 sides).
    A cell must be open itself to be a doorway.
    """
    if grid[y, x] != 0:  # Must be open
        return False
    
    height, width = grid.shape
    blocked = 0
    open_count = 0
    
    # Check all 4 directions
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        nx, ny = x + dx, y + dy
        
        # Out of bounds counts as blocked
        if nx < 0 or nx >= width or ny < 0 or ny >= height:
            blocked += 1
        elif grid[ny, nx] != 0:  # Water or fire (blocked)
            blocked += 1
        else:  # Open
            open_count += 1
    
    # Doorway: 2-3 sides blocked, 1-2 sides open
    return blocked >= 2 and open_count >= 1


def find_doorways(grid):
    """Find all doorway cells in the grid."""
    height, width = grid.shape
    doorways = []
    
    for y in range(height):
        for x in range(width):
            if is_doorway(grid, x, y):
                doorways.append((x, y))
    
    return doorways


def solve_fire_challenge(map_num=0):
    """
    Solve the fire challenge using Pete's algorithm.
    """
    # Get the map
    grid, max_walls, map_name = get_map(map=map_num)
    
    print(f"\nMap {map_num}: {map_name} - Pete's Algorithm")
    print(f"Grid size: {grid.shape}")
    print(f"Maximum walls: {max_walls}")
    print("\nGrid layout:")
    print(grid)
    
    # Find fire positions
    fire_positions = find_fire_positions(grid)
    print(f"\nFire positions: {fire_positions}")
    
    # Find interesting squares
    adjacent_to_fire = find_adjacent_to_fire(grid, fire_positions)
    doorways = find_doorways(grid)
    
    # Combine and deduplicate
    interesting_squares = list(set(adjacent_to_fire + doorways))
    
    print(f"\nAdjacent to fire: {len(adjacent_to_fire)} squares")
    print(f"Doorways found: {len(doorways)} squares")
    print(f"Total interesting squares: {len(interesting_squares)}")
    print(f"Interesting positions: {interesting_squares}")
    
    # Highlight interesting squares
    highlight_cells(interesting_squares, level=1)
    
    # Try all combinations
    best_score = 0
    best_walls = []
    total_combinations = 0
    
    print(f"\nTrying all combinations of {max_walls} walls from {len(interesting_squares)} positions...")
    
    for num_walls in range(1, min(max_walls, len(interesting_squares)) + 1):
        for wall_combo in combinations(interesting_squares, num_walls):
            total_combinations += 1
            
            # Reset and try this combination
            grid, _, _ = get_map(map=map_num)
            place_walls(list(wall_combo))
            score = test_result()
            
            if score > best_score:
                best_score = score
                best_walls = list(wall_combo)
                print(f"  New best! Score: {score}, Walls: {wall_combo}")
    
    print(f"\nTested {total_combinations} combinations")
    print(f"Best score: {best_score} cells saved")
    print(f"Best wall positions: {best_walls}")
    
    # Apply the best solution
    grid, _, _ = get_map(map=map_num)
    highlight_cells(interesting_squares, level=1)
    highlight_cells(best_walls, level=2)
    place_walls(best_walls)
    
    final_score = test_result()
    print(f"Final verification: {final_score} cells saved\n")
    
    # Visualize
    print("Launching visualization...")
    visualize_result()


if __name__ == "__main__":
    print("Pete's Fire Challenge Solver")
    print("=" * 50)
    
    print("\nAvailable maps:")
    available_maps = get_available_maps()
    for num, name in available_maps:
        print(f"  {num}: {name}")
    
    map_choice = input("\nEnter map number (or press Enter for map 0): ").strip()
    
    if map_choice.isdigit():
        map_num = int(map_choice)
        if 0 <= map_num < len(available_maps):
            solve_fire_challenge(map_num=map_num)
        else:
            print("Invalid map number. Using map 0.")
            solve_fire_challenge(map_num=0)
    else:
        print("Using map 0...")
        solve_fire_challenge(map_num=0)
