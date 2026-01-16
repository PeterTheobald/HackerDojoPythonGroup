"""
Example player script for the Fire Challenge game.

This script demonstrates how to use the fire_challenge module to:
1. Load a challenge map
2. Analyze the grid
3. Place walls strategically
4. Test results
5. Visualize the fire spread
"""

from fire_challenge import (
    get_map, 
    place_walls, 
    test_result, 
    highlight_cells,
    highlight_clear,
    visualize_result
)


def simple_strategy(map_num=0):
    """
    A simple wall placement strategy that creates barriers.
    """
    # Get the challenge map
    grid, max_walls = get_map(map=map_num)
    
    print(f"Map {map_num} loaded!")
    print(f"Grid size: {grid.shape}")
    print(f"Maximum walls allowed: {max_walls}")
    print("\nGrid layout:")
    print(grid)
    print("\nLegend: 0=Open, 1=Water, 2=Fire, 3=Wall")
    
    # Find fire starting positions
    fire_positions = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 2:
                fire_positions.append((x, y))
    
    print(f"\nFire starting positions: {fire_positions}")
    
    # Highlight fire positions as cells of interest
    highlight_cells(fire_positions, level=1)
    
    # Strategy: Place walls to create barriers
    # For map 0, let's try to create a barrier
    if map_num == 0:
        # Create a vertical barrier in the middle
        wall_cells = [
            (3, 0),
            (3, 1),
            (4, 1),
            (4, 5),
            (4, 6),
        ]
    elif map_num == 2:
        # Create barriers avoiding water cells at (2,2) and (3,2)
        wall_cells = [
            (1, 1),
            (2, 3),
            (3, 4),
        ]
    else:
        # Default: place some walls near fire
        wall_cells = []
        for fx, fy in fire_positions[:1]:
            # Place walls around first fire
            for dx, dy in [(1, 0), (0, 1), (1, 1)]:
                wx, wy = fx + dx, fy + dy
                if 0 <= wx < grid.shape[1] and 0 <= wy < grid.shape[0]:
                    if grid[wy, wx] == 0 and len(wall_cells) < max_walls:
                        wall_cells.append((wx, wy))
    
    # Highlight candidate wall positions
    highlight_cells(wall_cells, level=2)
    
    # Place the walls
    print(f"\nPlacing walls at: {wall_cells}")
    place_walls(wall_cells)
    
    # Test the result
    num_saved = test_result()
    print(f"\nCells saved from fire: {num_saved}")
    
    # Visualize the result
    print("\nLaunching visualization...")
    visualize_result()


def advanced_strategy(map_num=0):
    """
    A more advanced strategy that tries to maximize saved cells.
    """
    grid, max_walls = get_map(map=map_num)
    
    print(f"Map {map_num} loaded - Advanced Strategy")
    print(f"Grid size: {grid.shape}")
    print(f"Maximum walls: {max_walls}")
    
    # Find all fire positions
    fire_positions = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 2:
                fire_positions.append((x, y))
    
    # Find all open cells far from fire
    height, width = grid.shape
    safe_cells = []
    
    for y in range(height):
        for x in range(width):
            if grid[y, x] == 0:
                # Calculate minimum Manhattan distance to any fire
                min_dist = min(abs(x - fx) + abs(y - fy) for fx, fy in fire_positions)
                safe_cells.append((x, y, min_dist))
    
    # Sort by distance (furthest first)
    safe_cells.sort(key=lambda c: c[2], reverse=True)
    
    # Highlight the safest areas
    safest = [(x, y) for x, y, d in safe_cells[:5]]
    highlight_cells(safest, level=1)
    
    # Create a barrier between fire and safe cells
    # Strategy: find the midpoint and create a barrier
    if fire_positions and safe_cells:
        avg_fire_x = sum(fx for fx, fy in fire_positions) / len(fire_positions)
        avg_fire_y = sum(fy for fx, fy in fire_positions) / len(fire_positions)
        
        # Place walls in a line perpendicular to fire spread direction
        wall_cells = []
        
        if map_num == 1:
            # For map 1, create diagonal barriers
            for i in range(min(max_walls, 10)):
                wx, wy = i, i
                if 0 <= wx < width and 0 <= wy < height and grid[wy, wx] == 0:
                    wall_cells.append((wx, wy))
        else:
            # Create a barrier line
            mid_x = width // 2
            mid_y = height // 2
            
            for offset in range(max_walls):
                if len(wall_cells) >= max_walls:
                    break
                    
                # Try vertical line
                wx, wy = mid_x, mid_y - max_walls//2 + offset
                if 0 <= wx < width and 0 <= wy < height and grid[wy, wx] == 0:
                    wall_cells.append((wx, wy))
    
    highlight_cells(wall_cells, level=2)
    
    print(f"\nPlacing {len(wall_cells)} walls")
    place_walls(wall_cells)
    
    num_saved = test_result()
    print(f"Cells saved: {num_saved}")
    
    visualize_result()


if __name__ == "__main__":
    print("Fire Challenge - Example Player")
    print("=" * 50)
    print("\nChoose a strategy:")
    print("1. Simple strategy on map 0")
    print("2. Simple strategy on map 2")
    print("3. Advanced strategy on map 1")
    print("4. Advanced strategy on map 3")
    
    choice = input("\nEnter choice (1-4, or press Enter for default): ").strip()
    
    if choice == "1":
        simple_strategy(map_num=0)
    elif choice == "2":
        simple_strategy(map_num=2)
    elif choice == "3":
        advanced_strategy(map_num=1)
    elif choice == "4":
        advanced_strategy(map_num=3)
    else:
        # Default
        print("\nRunning simple strategy on map 0...")
        simple_strategy(map_num=0)
