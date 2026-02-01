#!/usr/bin/env python3
"""
Example: Browsing and selecting from available maps
"""

from fire_challenge import FireChallenge

print("=" * 70)
print("FIRE CHALLENGE - AVAILABLE MAPS")
print("=" * 70)

# Get all available maps
maps = FireChallenge.get_available_maps()

print(f"\nThere are {len(maps)} built-in challenge maps:\n")

# Display maps with details
for num, name in maps:
    # Load map to get details
    game = FireChallenge(map=num)
    print(f"Map {num:2d}: {name:45s} ({game.grid.shape[1]}x{game.grid.shape[0]}, {game.max_walls} walls)")

print("\n" + "=" * 70)

# Interactive selection (if running interactively)
try:
    choice = input("\nEnter map number to preview (or press Enter to skip): ").strip()
    
    if choice.isdigit():
        map_num = int(choice)
        
        if 0 <= map_num < len(maps):
            print("\n" + "=" * 70)
            game = FireChallenge(map=map_num)
            print(f"MAP {map_num}: {game.name}")
            print("=" * 70)
            print(f"\nGrid size: {game.grid.shape[1]} wide x {game.grid.shape[0]} tall")
            print(f"Maximum walls: {game.max_walls}")
            print(f"Open cells to save: {game.total_open_cells}")
            
            print("\nMap preview:")
            print("-" * 70)
            game.print_map('str')
            print("-" * 70)
            print("\nLegend: (space)=open, #=water, *=fire, W=wall")
        else:
            print(f"Invalid map number. Choose 0-{len(maps)-1}")
    elif choice:
        print("Please enter a number")
        
except (KeyboardInterrupt, EOFError):
    print("\n\nExiting...")

print("\n" + "=" * 70)
print("TIP: Use FireChallenge.get_available_maps() to list all maps")
print("     Then: game = FireChallenge(map=<number>)")
print("=" * 70)
