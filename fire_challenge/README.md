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
grid, max_walls = get_map(map=0)

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
grid, max_walls = get_map(map=1)

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

## API Reference

### `get_map(map=0) -> (grid, max_walls)`
Load a challenge map.
- **Parameters**: `map` (int) - Map number (0-6)
- **Returns**: Tuple of (2D numpy array, max walls allowed)

### `place_walls(cells)`
Place walls on the grid.
- **Parameters**: `cells` (List[Tuple[int, int]]) - List of (x, y) coordinates

### `test_result() -> int`
Test current wall placement.
- **Returns**: Number of cells saved from fire

### `highlight_cells(cells, level)`
Highlight cells in visualization.
- **Parameters**: 
  - `cells` (List[Tuple[int, int]]) - List of (x, y) coordinates
  - `level` (int) - 1 for interest (yellow), 2 for candidate (orange)

### `highlight_clear()`
Clear all highlighted cells.

### `visualize_result()`
Display animated visualization of fire spreading.

## Challenge Maps

- **Map 0**: 8x8 grid with two fire sources, 5 walls allowed
- **Map 1**: 10x10 grid with corner fires, 10 walls allowed
- **Map 2**: 6x6 grid with diagonal fires, 3 walls allowed  
- **Map 3**: 10x10 grid with multiple fires in a row, 8 walls allowed
- **Map 4**: 10x10 two rooms with one door - block the door with 1 wall
- **Map 5**: 10x10 central town with 3 entrances - seal it with 3 walls
- **Map 6**: 12x7 hallway with multiple rooms - 1 wall to save the most

## Running the Example

```bash
uv run example_player.py
```

uv will automatically install numpy and matplotlib if needed, then run the example. The example demonstrates both simple and advanced strategies for wall placement.
*Note: the example players are not smart!*

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
