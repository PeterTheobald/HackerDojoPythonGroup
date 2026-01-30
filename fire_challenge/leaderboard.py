#!/usr/bin/env python3
"""
Fire Challenge Leaderboard
===========================

Automatically finds all player programs (*_player.py or *_Player.py),
runs them against all available maps, and displays a leaderboard.

Each player program should have a function:
    solve_fire_challenge(map_num, visualize=False)
    
The function should return either:
    - A single number (score)
    - A tuple whose first element is the score
"""

import glob
import importlib.util
import sys
import os
from pathlib import Path
import traceback

# Add the fire_challenge directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fire_challenge import FireChallenge


def find_player_files() -> list[Path]:
    """Find all player files matching *_player.py or *_Player.py pattern."""
    current_dir = Path(__file__).parent
    
    # Find both *_player.py and *_Player.py files
    player_files = []
    player_files.extend(current_dir.glob('*_player.py'))
    player_files.extend(current_dir.glob('*_Player.py'))
    
    # Remove duplicates (in case of case-insensitive file systems)
    player_files = list(set(player_files))
    
    return sorted(player_files)


def load_player_module(player_file: Path):
    """Load a player module from a file path."""
    module_name = player_file.stem
    spec = importlib.util.spec_from_file_location(module_name, player_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load {player_file}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    
    return module


def run_player_on_map(player_name: str, player_module, map_num: int) -> int | None:
    """
    Run a player's solve_fire_challenge function on a specific map.
    
    Returns:
        The score (number of cells saved), or None if there was an error
    """
    if not hasattr(player_module, 'solve_fire_challenge'):
        print(f"  ⚠️  {player_name}: No solve_fire_challenge function found")
        return None
    
    try:
        # Run the player's solution (with visualize=False)
        result = player_module.solve_fire_challenge(map_num, visualize=False)
        
        # Handle both single value and tuple return types
        if isinstance(result, tuple):
            score = result[0]
        else:
            score = result
        
        return int(score) if score is not None else None
    
    except Exception as e:
        print(f"  ❌ {player_name} on map {map_num}: {type(e).__name__}: {str(e)}")
        if "--verbose" in sys.argv:
            traceback.print_exc()
        return None


def format_table(headers: list[str], rows: list[list[str]], col_widths: list[int] | None = None) -> str:
    """Format data as a pretty ASCII table."""
    if col_widths is None:
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Build separator line
    separator = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    
    # Build header
    header_row = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
    
    # Build data rows
    data_rows = []
    for row in rows:
        data_row = "| " + " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)) + " |"
        data_rows.append(data_row)
    
    # Combine all parts
    table = [separator, header_row, separator]
    table.extend(data_rows)
    table.append(separator)
    
    return "\n".join(table)


def run_leaderboard():
    """Main function to run the leaderboard."""
    print("=" * 80)
    print("FIRE CHALLENGE LEADERBOARD")
    print("=" * 80)
    print()
    
    # Find all player files
    player_files = find_player_files()
    
    if not player_files:
        print("❌ No player files found matching *_player.py or *_Player.py")
        return
    
    print(f"Found {len(player_files)} player(s):")
    for pf in player_files:
        print(f"  • {pf.name}")
    print()
    
    # Get available maps
    available_maps = FireChallenge.get_available_maps()
    print(f"Running against {len(available_maps)} maps:")
    for map_num, map_name in available_maps:
        print(f"  {map_num}: {map_name}")
    print()
    print("-" * 80)
    print()
    
    # Run each player on each map
    results: dict[str, dict[int, int | None]] = {}
    
    for player_file in player_files:
        player_name = player_file.stem
        print(f"Running {player_name}...")
        
        try:
            # Load the player module
            player_module = load_player_module(player_file)
            
            # Run on each map
            results[player_name] = {}
            for map_num, map_name in available_maps:
                print(f"  Map {map_num}: {map_name}...", end=" ", flush=True)
                score = run_player_on_map(player_name, player_module, map_num)
                results[player_name][map_num] = score
                
                if score is not None:
                    print(f"✅ Score: {score}")
                else:
                    print("❌ Failed")
            
            print()
        
        except Exception as e:
            print(f"  ❌ Error loading {player_name}: {type(e).__name__}: {str(e)}")
            if "--verbose" in sys.argv:
                traceback.print_exc()
            results[player_name] = {map_num: None for map_num, _ in available_maps}
            print()
    
    # Calculate totals
    totals = {}
    for player_name, scores in results.items():
        valid_scores = [s for s in scores.values() if s is not None]
        totals[player_name] = sum(valid_scores) if valid_scores else 0
    
    # Build results table
    print("-" * 80)
    print()
    print("RESULTS:")
    print()
    
    # Prepare headers: Player name, each map, and Total
    headers = ["Player"]
    for map_num, map_name in available_maps:
        headers.append(f"Map {map_num}")
    headers.append("TOTAL")
    
    # Prepare rows
    rows = []
    for player_name in sorted(results.keys()):
        row = [player_name]
        for map_num, _ in available_maps:
            score = results[player_name][map_num]
            row.append(str(score) if score is not None else "FAIL")
        row.append(str(totals[player_name]))
        rows.append(row)
    
    # Sort rows by total score (descending)
    rows.sort(key=lambda r: int(r[-1]) if r[-1].isdigit() else -1, reverse=True)
    
    # Print table
    print(format_table(headers, rows))
    print()
    
    # Determine winner
    if totals:
        winner = max(totals.items(), key=lambda x: x[1])
        print(f"WINNER: {winner[0]} with {winner[1]} total cells saved!")
    else:
        print("No valid results to determine a winner.")


if __name__ == "__main__":
    run_leaderboard()
