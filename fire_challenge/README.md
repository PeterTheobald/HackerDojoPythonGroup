# Fire Challenge

A Python module for creating grid-based fire spread challenges where players write code to strategically place walls to block fire propagation.

## Overview

The fire challenge presents players with a grid containing:
- **Open cells (0)**: Can catch fire
- **Water cells (1)**: Block fire spread
- **Fire cells (2)**: Starting fire positions
- **Wall cells (3)**: Placed by player to block fire

Players must analyze the grid and place a limited number of walls to save as many cells as possible from the spreading fire.

## Installation

No installation needed! [uv](https://github.com/astral-sh/uv) automatically manages dependencies when you run the scripts.

## Usage

### Basic Example

```python
from fire_challenge import get_map, place_walls, test_result, visualize_result

# Get a challenge map
grid, max_walls, map_name = get_map(map=0)
print(f"Playing: {map_name}")

# Analyze the grid (0=open, 1=water, 2=fire)
print(grid)

# Place walls at strategic positions
place_walls([(3, 0), (3, 1), (4, 1)])

# Test how many cells you saved
num_saved = test_result()
print(f"Saved {num_saved} cells!")

# Visualize the fire spread animation
visualize_result()
```

### Advanced Features

```python
from fire_challenge import (
    get_map, place_walls, test_result, 
    highlight_cells, highlight_clear, visualize_result
)

# Load a map
grid, max_walls, map_name = get_map(map=1)

# Find fire positions
fire_positions = [(x, y) for y in range(grid.shape[0]) 
                  for x in range(grid.shape[1]) if grid[y, x] == 2]

# Highlight cells of interest (level 1 = yellow frame)
highlight_cells(fire_positions, level=1)

# Mark candidate wall positions (level 2 = orange frame)
candidates = [(5, 5), (5, 6), (6, 5)]
highlight_cells(candidates, level=2)

# Place walls
place_walls(candidates)

# Clear highlights if needed
# highlight_clear()

# Test and visualize
num_saved = test_result()
visualize_result()
```

### Testing Multiple Wall Placements

```python
from fire_challenge import get_map, place_walls, test_result

# Load a map
grid, max_walls, map_name = get_map(map=3)

best_score = 0
best_walls = []

# Try different wall placement strategies
candidates = [
    [(0, 1), (0, 2), (0, 3)],
    [(1, 0), (2, 0), (3, 0)],
    [(0, 1), (1, 1), (2, 1)],
]

for wall_placement in candidates:
    # Reset the map to clear previous walls
    grid, max_walls, map_name = get_map(map=3)
    
    # Try this placement
    place_walls(wall_placement)
    score = test_result()
    
    print(f"Walls {wall_placement}: saved {score} cells")
    
    if score > best_score:
        best_score = score
        best_walls = wall_placement

# Use the best solution
grid, max_walls, map_name = get_map(map=3)
place_walls(best_walls)
print(f"Best solution: {best_walls} with {best_score} cells saved")
```

**Note**: Call `get_map()` again to reset all placed walls and highlights before testing a new wall configuration.

### Creating Custom Maps

```python
from fire_challenge import get_custom_map_from_string, place_walls, visualize_result

# Create a custom map using a string representation
map_str = '''
f   #
    #
#####
   f
'''

grid, max_walls, name = get_custom_map_from_string(
    map_str, 
    max_walls=3, 
    name="My Custom Map"
)

# Or create from a numpy array
import numpy as np
from fire_challenge import get_custom_map

custom_grid = np.array([
    [2, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [1, 1, 1, 2],
])

grid, max_walls, name = get_custom_map(
    custom_grid, 
    max_walls=2, 
    name="Array Map"
)

# Play as normal
place_walls([(1, 0), (2, 2)])
visualize_result()
```

## API Reference

### `get_map(map=0) -> (grid, max_walls, name)`
Load a challenge map.
- **Parameters**: `map` (int) - Map number (0-8)
- **Returns**: Tuple of (2D numpy array, max walls allowed, map name)
- **Note**: Calling `get_map()` resets all placed walls and highlighted cells from any previous map
- **Example**: `grid, max_walls, map_name = get_map(map=0)`

### `get_available_maps() -> List[(int, str)]`
Get a list of all available challenge maps.
- **Returns**: List of (map_number, map_name) tuples
- **Example**: `maps = get_available_maps()`

### `get_custom_map(grid, max_walls, name="Custom Map") -> (grid, max_walls, name)`
Load a custom map from a numpy array.
- **Parameters**: 
  - `grid` (np.ndarray) - 2D numpy array with 0=open, 1=water, 2=fire
  - `max_walls` (int) - Maximum number of walls allowed
  - `name` (str) - Display name for the map
- **Returns**: Tuple of (grid, max_walls, name)
- **Example**: `grid, max_walls, name = get_custom_map(my_array, max_walls=5)`

### `get_custom_map_from_string(map_string, max_walls, name="Custom Map") -> (grid, max_walls, name)`
Load a custom map from a string representation.
- **Parameters**: 
  - `map_string` (str) - Multi-line string where `' '`=open, `'#'`=water, `'f'`=fire
  - `max_walls` (int) - Maximum number of walls allowed
  - `name` (str) - Display name for the map
- **Returns**: Tuple of (grid, max_walls, name)
- **Example**: 
```python
map_str = '''
f   #
    #
#####
   f
'''
grid, max_walls, name = get_custom_map_from_string(map_str, max_walls=3)
```

### `place_walls(cells)`
Place walls on the grid.
- **Parameters**: `cells` (List[Tuple[int, int]]) - List of (x, y) coordinates
- **Example**: `place_walls([(3, 0), (3, 1), (4, 1)])`

### `test_result() -> int`
Test current wall placement.
- **Returns**: Number of cells saved from fire
- **Example**: `num_saved = test_result()`

### `highlight_cells(cells, level)`
Highlight cells in visualization.
- **Parameters**: 
  - `cells` (List[Tuple[int, int]]) - List of (x, y) coordinates
  - `level` (int) - 1 for interest (yellow), 2 for candidate (orange)
- **Example**: `highlight_cells([(2, 3), (4, 5)], level=1)`

### `highlight_clear()`
Clear all highlighted cells.

### `visualize_result()`
Display animated visualization of fire spreading.

## Challenge Maps

- **Map 0 - Two Fires**: 8x8 grid with two fire sources, 5 walls allowed
- **Map 1 - Corner Fires**: 10x10 grid with corner fires, 10 walls allowed
- **Map 2 - Diagonal Fires**: 6x6 grid with diagonal fires, 3 walls allowed  
- **Map 3 - Fire Row**: 10x10 grid with multiple fires in a row, 8 walls allowed
- **Map 4 - Two Rooms**: 10x10 two rooms with one door - block the door with 1 wall
- **Map 5 - Central Town**: 10x10 central town with 3 entrances - seal it with 3 walls
- **Map 6 - Hallway Rooms**: 12x7 hallway with multiple rooms - 1 wall to save the most
- **Map 7 - Big Funnel**: 15x10 funnel shape with fire at both ends, 4 walls allowed
- **Map 8 - Fake Doors**: 15x10 maze with multiple openings - find the real choke points, 4 walls allowed

## Running the Example

```bash
uv run example_player.py
```

uv will automatically install numpy and matplotlib if needed, then run the example. The example demonstrates both simple and advanced strategies for wall placement.
*Note: the example players are not particularly smart!*

## Leaderboard Competition

Compete against other players by creating your own player file!

### Requirements to Participate

To have your player included in the leaderboard:

1. **Name your file**: `*_player.py` or `*_Player.py` (e.g., `alice_player.py`, `Bob_Player.py`)

2. **Define the function**:
   ```python
   def solve_fire_challenge(map_num, visualize=True):
       # Your strategy here
       return score  # or return (score, other_data)
   ```
   - **Parameters**: 
     - `map_num` (int) - The map number to solve
     - `visualize` (bool) - Whether to display visualization (default: True)
   - **Returns**: Either a single number (the score) or a tuple whose first element is the score

3. **Run the leaderboard**:
   ```bash
   python leaderboard.py
   ```

The leaderboard will automatically:
- Find all player files matching the naming pattern
- Run each player against all 11 challenge maps
- Display a results table showing each player's score on each map
- Declare the overall winner based on total cells saved

### Example Player Template

```python
from fire_challenge import get_map, place_walls, test_result, visualize_result

def solve_fire_challenge(map_num, visualize=True):
    """Your strategy description here."""
    
    # Get the map
    grid, max_walls, map_name = get_map(map=map_num)
    
    # Your algorithm here
    # ...
    
    # Place walls
    wall_positions = [(x1, y1), (x2, y2)]  # Your wall positions
    place_walls(wall_positions)
    
    # Get score
    score = test_result()
    
    # Optional visualization
    if visualize:
        visualize_result()
    
    return score
```

## Fire Spread Rules

1. Fire starts at cells marked with value 2
2. Each turn, fire spreads to adjacent open cells (4-directional: up, down, left, right)
3. Fire cannot spread through water cells (1) or wall cells (3)
4. The simulation continues until fire cannot spread further

## Tips for Players

1. Identify fire starting positions
2. Find critical chokepoints where a few walls can block multiple spread paths
3. Protect large areas of open space
4. Use `test_result()` to iterate on your strategy
5. Use `highlight_cells()` to visualize your analysis
6. Water cells are your allies - use them as natural barriers

## License

Part of the Hacker Dojo Python Group project materials.
