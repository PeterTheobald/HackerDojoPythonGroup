#!/usr/bin/env python3
"""
Simple Example Player for Fire Challenge

This demonstrates the basic steps to play the fire challenge:
1. Create a game instance
2. Find fire positions
3. Place walls next to the fire
4. Test how many cells were saved
5. Visualize the result
"""

from fire_challenge import FireChallenge


def solve_fire_challenge_simple(map_num=0, visualize=True):
    """
    Simple strategy: Place walls next to fire starting positions.
    
    Args:
        map_num: Which map to play (0-13)
        visualize: Whether to show the fire spread animation
        
    Returns:
        Number of cells saved from fire
    """
    # Create a game instance
    game = FireChallenge(map=map_num)
    
    print(f"Playing: {game.name}")
    print(f"Map size: {game.grid.shape}")
    print(f"Maximum walls allowed: {game.max_walls}")
    print(f"Total open cells to protect: {game.total_open_cells}\n")
    
    # Find all fire starting positions
    fire_positions = []
    for y in range(game.grid.shape[0]):
        for x in range(game.grid.shape[1]):
            if game.grid[y, x] == 2:  # 2 = fire
                fire_positions.append((x, y))
    
    print(f"Fire starting at: {fire_positions}\n")
    
    # Find open cells next to fire positions
    wall_candidates = []
    for fire_x, fire_y in fire_positions:
        # Check all 4 adjacent cells (up, down, left, right)
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = fire_x + dx, fire_y + dy
            
            # Check if position is valid and is an open cell
            if (0 <= nx < game.grid.shape[1] and 
                0 <= ny < game.grid.shape[0] and
                game.grid[ny, nx] == 0):  # 0 = open cell
                
                if (nx, ny) not in wall_candidates:
                    wall_candidates.append((nx, ny))
    
    # Use only as many walls as allowed
    walls_to_place = wall_candidates[:game.max_walls]
    
    print(f"Placing {len(walls_to_place)} walls at: {walls_to_place}")
    game.place_walls(walls_to_place)
    
    # Test the result
    score = game.test_result()
    print(f"\nResult: Saved {score}/{game.total_open_cells} cells from fire!")
    
    # Show the visualization
    if visualize:
        game.visualize()
    
    return score


if __name__ == "__main__":
    # Play map 0 by default
    print("=" * 60)
    print("FIRE CHALLENGE - SIMPLE EXAMPLE")
    print("=" * 60)
    print()
    
    print("\nAvailable maps:")
    available_maps = FireChallenge.get_available_maps()
    for num, name in available_maps:
        print(f"  {num}: {name}")
    
    map_choice = input("\nEnter map number (or press Enter for map 0): ").strip()
    
    if map_choice.isdigit():
        map_num = int(map_choice)
    else:
        map_num = 0
        
    score = solve_fire_challenge_simple(map_num=map_num, visualize=True)
    
    print("\n" + "=" * 60)
    print(f"Final Score: {score} cells saved")
    print("=" * 60)
