"""
Example player script for the Fire Challenge game.

This script demonstrates how to use the fire_challenge module to:
1. Load a challenge map
2. Analyze the grid
3. Place walls strategically
4. Test results
5. Visualize the fire spread

Strategy: Surround the initial fire as much as possible
"""
from fire_challenge import (
    get_map,
    get_available_maps,
    place_walls, 
    test_result, 
    highlight_cells,
    visualize_result
)


def surround_fire_strategy(map_num=0):
    """
    Simple strategy: Surround the fire starting positions with walls.
    """
    # Get the challenge map
    grid, max_walls, map_name = get_map(map=map_num)
    
    print(f"Map {map_num}: {map_name}")
    print(f"Grid size: {grid.shape}")
    print(f"Maximum walls allowed: {max_walls}")
    print("\nGrid layout:")
    print(grid)
    print("\nLegend: 0=Open, 1=Water, 2=Fire, 3=Wall")
    
    # Find fire starting positions
    # Note: grids are stored [y,x] but coordinates are given as (x,y) by math convention.
    fire_positions = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 2:
                fire_positions.append((x, y))
    
    print(f"\nFire starting positions: {fire_positions}")
    
    # Highlight fire positions as cells of interest
    highlight_cells(fire_positions, level=1)
    
    # Strategy: Place walls around fire positions
    # Check all 4 adjacent cells (up, down, left, right) around each fire
    wall_candidates = []
    
    for fx, fy in fire_positions:
        # Check 4 directions: right, down, left, up
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            wx, wy = fx + dx, fy + dy
            
            # Check if position is valid and is an open cell
            if 0 <= wx < grid.shape[1] and 0 <= wy < grid.shape[0]:
                if grid[wy, wx] == 0 and (wx, wy) not in wall_candidates:
                    wall_candidates.append((wx, wy))
    
    # Limit to max_walls
    wall_cells = wall_candidates[:max_walls]
    
    # Highlight candidate wall positions
    highlight_cells(wall_cells, level=2)
    
    print(f"\nFound {len(wall_candidates)} potential wall positions around fire")
    print(f"Placing {len(wall_cells)} walls at: {wall_cells}")
    
    # Place the walls
    place_walls(wall_cells)
    
    # Test the result
    num_saved = test_result()
    print(f"\nCells saved from fire: {num_saved}")
    
    # Visualize the result
    print("\nLaunching visualization...")
    visualize_result()


if __name__ == "__main__":
    print("Fire Challenge - Example Player")
    print("=" * 50)
    print("\nStrategy: Surround initial fire positions with walls")
    
    print("\nAvailable maps:")
    available_maps = get_available_maps()
    for num, name in available_maps:
        print(f"  {num}: {name}")
    
    map_choice = input("\nEnter map number (or press Enter for map 0): ").strip()
    
    if map_choice.isdigit():
        map_num = int(map_choice)
        if 0 <= map_num < len(available_maps):
            surround_fire_strategy(map_num=map_num)
        else:
            print("Invalid map number. Using map 0.")
            surround_fire_strategy(map_num=0)
    else:
        # Default to map 0
        print("Using map 0...")
        surround_fire_strategy(map_num=0)

