#!/usr/bin/env python3
"""
Beginner-friendly example: Using print_map to understand the game
"""

from fire_challenge import FireChallenge

print("BEGINNER TUTORIAL: Understanding Fire Challenge with print_map")
print("=" * 70)

# Step 1: Create a custom map
print("\nStep 1: Create a simple custom map")
print("-" * 70)

my_map = '''
    
 *  
    
  * 
'''

game = FireChallenge.from_string(my_map, max_walls=2, name="My First Map")

print(f"Created map: {game.name}")
print(f"Grid size: {game.grid.shape[1]} wide x {game.grid.shape[0]} tall")
print(f"You can place up to {game.max_walls} walls")

print("\nHere's your map (as integers):")
game.print_map('int')
print("\nLegend: 0=open, 1=water, 2=fire, 3=wall")

print("\nHere's your map (as characters):")
game.print_map('str')
print("\nLegend: (space)=open, #=water, *=fire, W=wall")

# Step 2: Explain the goal
print("\n" + "=" * 70)
print("Step 2: The Goal")
print("-" * 70)
print(f"Save as many of the {game.total_open_cells} open cells as possible!")
print("Fire spreads to adjacent open cells (up, down, left, right)")
print("Walls and water block fire from spreading")

# Step 3: Try placing walls
print("\n" + "=" * 70)
print("Step 3: Let's try placing walls")
print("-" * 70)

print("\nStrategy: Block the path between the two fires")
print("Placing wall at position (1, 1)...")
game.place_walls([(1, 1)])

print("\nMap after placing 1 wall:")
game.print_map('str')
print(f"Walls used: {len(game.walls_placed)}/{game.max_walls}")

print("\nPlacing another wall at position (2, 1)...")
game.place_walls([(2, 1)])

print("\nMap after placing 2 walls:")
game.print_map('str')
print(f"Walls used: {len(game.walls_placed)}/{game.max_walls}")

# Step 4: Test the result
print("\n" + "=" * 70)
print("Step 4: Test the result")
print("-" * 70)

score = game.test_result()
print(f"\n🎉 You saved {score} out of {game.total_open_cells} cells!")
percentage = (score / game.total_open_cells) * 100
print(f"   That's {percentage:.1f}% saved!")

# Step 5: Try a different approach
print("\n" + "=" * 70)
print("Step 5: Can we do better? Let's try again")
print("-" * 70)

game.reset()
print("Reset the map (all walls removed)")
print("\nOriginal map:")
game.print_map('str')

print("\nTrying different positions: (0, 1) and (3, 1)")
game.place_walls([(0, 1), (3, 1)])

print("\nNew wall placement:")
game.print_map('str')

score2 = game.test_result()
print(f"\nNew score: {score2} out of {game.total_open_cells} cells saved")

if score2 > score:
    print("✓ Better strategy!")
elif score2 < score:
    print("✗ First strategy was better")
else:
    print("= Same result")

print("\n" + "=" * 70)
print("TIP: Use game.print_map('str') to visualize your strategy anytime!")
print("=" * 70)
