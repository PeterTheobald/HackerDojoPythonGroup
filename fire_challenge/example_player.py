"""
Example player script using the new FireChallenge class-based API.

This script demonstrates how to use the FireChallenge class to:
1. Create a game instance
2. Analyze the grid
3. Place walls strategically
4. Test results
5. Compare multiple strategies
6. Visualize the fire spread

Strategy: Surround the initial fire as much as possible
"""
from fire_challenge import FireChallenge


def solve_fire_challenge_simple(map_num=0, visualize=True):
    """
    Simple strategy using the new class-based API.
    Demonstrates basic usage and properties.
    """
    # Create a new game instance
    game = FireChallenge(map=map_num)
    
    print(f"Map: {game.name}")
    print(f"Grid size: {game.grid.shape}")
    print(f"Maximum walls allowed: {game.max_walls}")
    print(f"Total open cells: {game.total_open_cells}")
    print("\nGrid layout:")
    print(game.grid)
    print("\nLegend: 0=Open, 1=Water, 2=Fire, 3=Wall")
    
    # Find fire starting positions
    fire_positions = []
    for y in range(game.grid.shape[0]):
        for x in range(game.grid.shape[1]):
            if game.grid[y, x] == 2:
                fire_positions.append((x, y))
    
    print(f"\nFire starting positions: {fire_positions}")
    
    # Highlight fire positions as cells of interest
    game.highlight_cells(fire_positions, level=1)
    
    # Strategy: Place walls around fire positions
    wall_candidates = []
    
    for fx, fy in fire_positions:
        # Check 4 directions: right, down, left, up
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            wx, wy = fx + dx, fy + dy
            
            # Check if position is valid and is an open cell
            if 0 <= wx < game.grid.shape[1] and 0 <= wy < game.grid.shape[0]:
                if game.grid[wy, wx] == 0 and (wx, wy) not in wall_candidates:
                    wall_candidates.append((wx, wy))
    
    # Limit to max_walls
    wall_cells = wall_candidates[:game.max_walls]
    
    # Highlight candidate wall positions
    game.highlight_cells(wall_cells, level=2)
    
    print(f"\nFound {len(wall_candidates)} potential wall positions around fire")
    print(f"Placing {len(wall_cells)} walls at: {wall_cells}")
    print(f"Walls remaining: {game.walls_remaining}")
    
    # Place the walls
    game.place_walls(wall_cells)
    
    print(f"Walls remaining after placement: {game.walls_remaining}")
    
    # Test the result
    num_saved = game.test_result()
    print(f"\nCells saved from fire: {num_saved}/{game.total_open_cells}")
    
    # Visualize the result
    if visualize:
        print("\nLaunching visualization...")
        game.visualize()
    
    return num_saved


def compare_strategies(map_num=0):
    """
    Demonstrate how to easily test multiple strategies with the class-based API.
    Each game instance is independent!
    """
    print(f"\n{'='*60}")
    print("COMPARING MULTIPLE STRATEGIES")
    print(f"{'='*60}\n")
    
    # Define different wall placement strategies
    strategies = {
        "Top-left corner": [(0, 0), (1, 0), (0, 1)],
        "Center walls": [(4, 4), (4, 5), (5, 4)],
        "Around fire": None,  # Will be computed
    }
    
    results = {}
    
    for name, walls in strategies.items():
        # Create a fresh game instance for each strategy
        game = FireChallenge(map=map_num)
        
        if walls is None:
            # Compute "around fire" strategy
            fire_positions = []
            for y in range(game.grid.shape[0]):
                for x in range(game.grid.shape[1]):
                    if game.grid[y, x] == 2:
                        fire_positions.append((x, y))
            
            wall_candidates = []
            for fx, fy in fire_positions:
                for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    wx, wy = fx + dx, fy + dy
                    if 0 <= wx < game.grid.shape[1] and 0 <= wy < game.grid.shape[0]:
                        if game.grid[wy, wx] == 0 and (wx, wy) not in wall_candidates:
                            wall_candidates.append((wx, wy))
            
            walls = wall_candidates[:game.max_walls]
        
        try:
            game.place_walls(walls)
            score = game.test_result()
            results[name] = {'score': score, 'walls': walls}
            print(f"✅ {name:20s}: {score:3d} cells saved with walls {walls}")
        except Exception as e:
            results[name] = {'score': 0, 'walls': walls}
            print(f"❌ {name:20s}: Failed - {e}")
    
    # Find and display best strategy
    best_strategy = max(results.items(), key=lambda x: x[1]['score'])
    print(f"\n🏆 Best strategy: {best_strategy[0]} with {best_strategy[1]['score']} cells saved")
    
    return best_strategy


def demonstrate_reset(map_num=0):
    """
    Demonstrate the reset() functionality to try multiple approaches with one instance.
    """
    print(f"\n{'='*60}")
    print("DEMONSTRATING RESET FUNCTIONALITY")
    print(f"{'='*60}\n")
    
    game = FireChallenge(map=map_num)
    
    # Try first strategy
    print("Strategy 1: Place walls at top-left")
    game.place_walls([(0, 0), (1, 0)])
    score1 = game.test_result()
    print(f"Score: {score1}, Walls placed: {game.walls_placed}\n")
    
    # Reset and try another strategy
    print("Resetting game...")
    game.reset()
    print(f"After reset - Walls placed: {game.walls_placed}")
    print(f"Walls remaining: {game.walls_remaining}\n")
    
    print("Strategy 2: Place walls at center")
    game.place_walls([(4, 4), (5, 5)])
    score2 = game.test_result()
    print(f"Score: {score2}, Walls placed: {game.walls_placed}\n")
    
    return score1, score2


def demonstrate_properties(map_num=0):
    """
    Show all the useful properties available on the FireChallenge object.
    """
    print(f"\n{'='*60}")
    print("FIRE CHALLENGE OBJECT PROPERTIES")
    print(f"{'='*60}\n")
    
    game = FireChallenge(map=map_num)
    
    print(f"Game object: {game}")
    print(f"\nProperties:")
    print(f"  .name              = {game.name}")
    print(f"  .map_number        = {game.map_number}")
    print(f"  .max_walls         = {game.max_walls}")
    print(f"  .walls_remaining   = {game.walls_remaining}")
    print(f"  .walls_placed      = {game.walls_placed}")
    print(f"  .total_open_cells  = {game.total_open_cells}")
    print(f"  .grid.shape        = {game.grid.shape}")
    
    # Place some walls and show updated properties
    print("\nPlacing 2 walls...")
    game.place_walls([(1, 1), (2, 2)])
    
    print(f"\nUpdated properties:")
    print(f"  .walls_remaining   = {game.walls_remaining}")
    print(f"  .walls_placed      = {game.walls_placed}")


if __name__ == "__main__":
    print("Fire Challenge - Class-Based API Examples")
    print("=" * 60)
    
    print("\nAvailable maps:")
    available_maps = get_available_maps()
    for num, name in available_maps:
        print(f"  {num}: {name}")
    
    map_choice = input("\nEnter map number (or press Enter for map 0): ").strip()
    
    if map_choice.isdigit():
        map_num = int(map_choice)
    else:
        map_num = 0
    
    # Run demonstrations
    print("\n" + "="*60)
    print("1. SIMPLE STRATEGY EXAMPLE")
    print("="*60)
    solve_fire_challenge_simple(map_num, visualize=False)
    
    # Compare strategies
    compare_strategies(map_num)
    
    # Demonstrate reset
    demonstrate_reset(map_num)
    
    # Show properties
    demonstrate_properties(map_num)
    
    # Ask if user wants to visualize
    print("\n" + "="*60)
    visualize = input("\nVisualize the best solution? (y/n): ").strip().lower()
    if visualize == 'y':
        game = FireChallenge(map=map_num)
        
        # Use the simple strategy
        fire_positions = []
        for y in range(game.grid.shape[0]):
            for x in range(game.grid.shape[1]):
                if game.grid[y, x] == 2:
                    fire_positions.append((x, y))
        
        wall_candidates = []
        for fx, fy in fire_positions:
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                wx, wy = fx + dx, fy + dy
                if 0 <= wx < game.grid.shape[1] and 0 <= wy < game.grid.shape[0]:
                    if game.grid[wy, wx] == 0 and (wx, wy) not in wall_candidates:
                        wall_candidates.append((wx, wy))
        
        game.highlight_cells(fire_positions, level=1)
        game.highlight_cells(wall_candidates[:game.max_walls], level=2)
        game.place_walls(wall_candidates[:game.max_walls])
        game.visualize()
