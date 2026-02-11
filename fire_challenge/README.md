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

```bash
pip install fire-challenge
```

Or using [uv](https://github.com/astral-sh/uv):
```bash
uv pip install fire-challenge
or
uv add fire-challenge
```

## Usage
#### Listing Available Maps

```python
from fire_challenge import FireChallenge

# Get list of all maps
maps = FireChallenge.get_available_maps()
for num, name in maps:
    print(f"Map {num}: {name}")
```

#### Basic Example

```python
from fire_challenge import FireChallenge

# Create a new game instance
game = FireChallenge(map=0)
print(f"Playing: {game.name}")
print(f"Max walls: {game.max_walls}")

# Analyze the grid (0=open, 1=water, 2=fire)
print(game.grid)

# Place walls at strategic positions
game.place_walls([(3, 0), (3, 1), (4, 1)])

# Test how many cells you saved
num_saved = game.test_result()
print(f"Saved {num_saved} cells!")

# Visualize the fire spread animation
game.visualize()
```

#### Comparing Multiple Strategies

The class-based API makes it easy to test different approaches:

```python
from fire_challenge import FireChallenge

# Test different wall placements
strategies = [
    [(0, 1), (0, 2), (0, 3)],
    [(1, 0), (2, 0), (3, 0)],
    [(0, 1), (1, 1), (2, 1)],
]

best_score = 0
best_walls = []

for walls in strategies:
    # Each instance is independent!
    game = FireChallenge(map=0)
    game.place_walls(walls)
    score = game.test_result()
    
    print(f"Walls {walls}: saved {score} cells")
    
    if score > best_score:
        best_score = score
        best_walls = walls

print(f"Best solution: {best_walls} with {best_score} cells saved")

# Visualize the best solution
game = FireChallenge(map=0)
game.place_walls(best_walls)
game.visualize()
```

#### Using reset() for Multiple Attempts

```python
from fire_challenge import FireChallenge

game = FireChallenge(map=0)

# Try first strategy
game.place_walls([(0, 0), (1, 0)])
score1 = game.test_result()
print(f"Strategy 1: {score1} cells saved")

# Reset and try another
game.reset()
game.place_walls([(4, 4), (5, 5)])
score2 = game.test_result()
print(f"Strategy 2: {score2} cells saved")
```

#### Inspecting Game State

```python
from fire_challenge import FireChallenge

game = FireChallenge(map=0)

# Access useful properties
print(f"Map name: {game.name}")
print(f"Grid size: {game.grid.shape}")
print(f"Max walls: {game.max_walls}")
print(f"Walls remaining: {game.walls_remaining}")
print(f"Total open cells: {game.total_open_cells}")

game.place_walls([(1, 1), (2, 2)])
print(f"Walls placed: {game.walls_placed}")
print(f"Walls remaining: {game.walls_remaining}")
```

#### Printing Maps

```python
from fire_challenge import FireChallenge

game = FireChallenge(map=0)

# Print as integer grid
print("Grid as integers:")
game.print_map('int')
# Output: [[0 0 0 ...] [0 0 0 ...] ...]

# Print as visual characters with border
print("\nGrid as characters:")
game.print_map('str')
# Output:
# ┌────────┐
# │        │
# │  ###   │
# │* # #   │
# │  ###   │
# │       *│
# └────────┘

# Place walls and see them in the output
game.place_walls([(1, 1), (2, 1)])
game.print_map('str')  # Shows 'W' for walls

# Get map as string for further processing
map_string = game.get_map_string('str')
```

#### Highlighting Cells

```python
from fire_challenge import FireChallenge

game = FireChallenge(map=1)

# Find fire positions
fire_positions = [(x, y) for y in range(game.grid.shape[0]) 
                  for x in range(game.grid.shape[1]) if game.grid[y, x] == 2]

# Highlight cells of interest (level 1 = yellow frame)
game.highlight_cells(fire_positions, level=1)

# Mark candidate wall positions (level 2 = orange frame)
candidates = [(5, 5), (5, 6), (6, 5)]
game.highlight_cells(candidates, level=2)

# Place walls and visualize
game.place_walls(candidates)
game.visualize()
```

### Creating Custom Maps

```python
from fire_challenge import FireChallenge

# Create from a string representation
map_str = '''
*   #
    #
#####
   *
'''

game = FireChallenge.from_string(map_str, max_walls=3, name="My Custom Map")
game.place_walls([(1, 0), (2, 2)])
game.visualize()

# Or create from a numpy array
import numpy as np

custom_grid = np.array([
    [2, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [1, 1, 1, 2],
])

game = FireChallenge.from_custom_grid(custom_grid, max_walls=2, name="Array Map")
game.place_walls([(1, 0), (2, 2)])
game.visualize()
```

## API Reference

### FireChallenge Class

#### `FireChallenge(map=0)`
Create a new fire challenge game instance.
- **Parameters**: `map` (int) - Map number (0-13, use `FireChallenge.get_available_maps()` to see all)
- **Example**: `game = FireChallenge(map=0)`

**Static Methods:**
- `FireChallenge.get_available_maps()` - Get list of all built-in maps as (number, name) tuples

**Class Methods:**
- `FireChallenge.from_custom_grid(grid, max_walls, name="Custom Map")` - Create from numpy array
- `FireChallenge.from_string(map_string, max_walls, name="Custom Map")` - Create from string representation

**Instance Methods:**
- `.place_walls(cells)` - Place walls at (x, y) positions
- `.test_result()` - Return number of cells saved
- `.visualize()` - Display fire spread animation
- `.reset()` - Remove all placed walls and highlights
- `.highlight_cells(cells, level)` - Highlight cells (level 1=yellow, 2=orange)
- `.highlight_clear()` - Clear all highlights
- `.print_map(format='int')` - Print map to console ('int' for numbers, 'str' for characters)
- `.get_map_string(format='str')` - Return map as string ('int' or 'str' format)

**Properties (read-only):**
- `.grid` - Current grid state (numpy array copy)
- `.name` - Map name
- `.map_number` - Map number or None for custom maps
- `.max_walls` - Maximum walls allowed
- `.walls_remaining` - Walls that can still be placed
- `.walls_placed` - List of wall positions placed
- `.total_open_cells` - Total open cells in original grid

## Challenge Maps

- **Map 0 - Two Fires**: 8x8 grid with two fire sources, 5 walls allowed
- **Map 1 - Corner Fires**: 10x10 grid with corner fires, 10 walls allowed
- **Map 2 - Diagonal Fires**: 6x6 grid with diagonal fires, 3 walls allowed  
- **Map 3 - Fire Row**: 10x10 grid with multiple fires in a row, 8 walls allowed
- **Map 4 - Two Rooms**: 10x10 two rooms with one door - block the door with 1 wall
- **Map 5 - Central Town**: 10x10 central town with 3 entrances - seal it with 3 walls
- **Map 6 - Hallway Rooms**: 7x12 hallway with multiple rooms - 1 wall to save the most
- **Map 7 - Big Funnel**: 10x15 funnel shape with fire at both ends, 4 walls allowed
- **Map 8 - Fake Doors**: 10x15 maze with multiple openings - find the real choke points, 4 walls allowed
- **Map 9 - Wide Open, Safe Corner**: 10x15 wide open area with a safe corner, 7 walls allowed
- **Map 10 - Sams Bane (assisted corner)**: 10x15 assisted corner challenge, 7 walls allowed
- **Map 11 - Diagonal Corner with Blocked Fires**: 15x15 diagonal pattern with blocked fires, 12 walls allowed
- **Map 12 - The Diabolical Five-Fire Maze**: 30x30 complex maze with five fire sources, 8 walls allowed
- **Map 13 - Nightmare open map with complex water assists**: 30x30 extremely challenging open map, 15 walls allowed

## Examples

### Beginner Tutorial

```bash
python beginner_tutorial.py
```

Starts with simple custom maps and teaches the basics of the FireChallenge API.

### Browse Available Maps

```bash
python browse_maps.py
```

Interactive tool to preview all 14 built-in challenge maps.

### Create Your Own Player

See the example player template in the "Leaderboard Competition" section below.

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
from fire_challenge import FireChallenge

def solve_fire_challenge(map_num, visualize=True):
    """Your strategy description here."""
    
    # Create game instance
    game = FireChallenge(map=map_num)
    
    # Your algorithm here
    # ...
    
    # Place walls
    wall_positions = [(x1, y1), (x2, y2)]  # Your wall positions
    game.place_walls(wall_positions)
    
    # Get score
    score = game.test_result()
    
    # Optional visualization
    if visualize:
        game.visualize()
    
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

MIT License: Use it as you like but always include the author copyright and license
Part of the Hacker Dojo Python Group project materials.


## Building and Publishing to PyPI

This package uses [uv](https://github.com/astral-sh/uv) for building and publishing.

### Prerequisites

Install uv if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Build Process

1. **Update the version number** in `pyproject.toml`:
   ```toml
   [project]
   version = "2.1.1"  # Increment appropriately
   ```

2. **Clean old builds and build the package**:
   ```bash
   cd fire_challenge
   rm dist/*.tar.gz dist/*.whl
   uv build
   ```
   
   This creates distribution files in the `dist/` directory:
   - `fire_challenge-X.Y.Z-py3-none-any.whl` (wheel)
   - `fire_challenge-X.Y.Z.tar.gz` (source distribution)

3. **Test the build locally** (optional but recommended):
   ```bash
   uv pip install dist/fire_challenge-X.Y.Z-py3-none-any.whl --force-reinstall
   python -c "from fire_challenge import FireChallenge; print(FireChallenge.get_available_maps())"
   ```

### Publishing to PyPI

1. **Set up PyPI credentials** (one-time setup):
   
   Ensure your `~/.pypirc` file contains your PyPI credentials:
   ```ini
   [pypi]
   username = your_username
   password = your_password
   ```
   
   Note: `uv-publish` will automatically read credentials from `~/.pypirc`

2. **Publish to PyPI**:
   ```bash
   uvx uv-publish
   ```
   
   The command will use your credentials from `~/.pypirc` automatically.

3. **Verify the upload**:
   
   Visit https://pypi.org/project/fire-challenge/ to confirm the new version is live.

4. **Test installation from PyPI**:
   ```bash
   uv pip install fire-challenge --upgrade
   python -c "from fire_challenge import FireChallenge; print('Success!')"
   ```

### Version Numbering Guidelines

Follow [Semantic Versioning](https://semver.org/):
- **Major (X.0.0)**: Breaking API changes
- **Minor (X.Y.0)**: New features, backward compatible
- **Patch (X.Y.Z)**: Bug fixes, backward compatible

### Quick Reference

```bash
# Full workflow
cd fire_challenge
# 1. Update version in pyproject.toml
# 2. Clean old builds and build
rm dist/*.tar.gz dist/*.whl
uv build
# 3. Publish
uvx uv-publish
# 4. Test
uv pip install fire-challenge --upgrade
```

