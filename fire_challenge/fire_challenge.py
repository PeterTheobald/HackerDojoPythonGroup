"""
Fire Challenge Module
=====================

A game module where players write Python code to place walls on a grid to block fire spread.

Grid values:
- 0: Open cell (can catch fire)
- 1: Water cell (blocks fire)
- 2: Starting fire cell
- 3: Wall cell (placed by player)

Usage:
    from fire_challenge import get_map, place_walls, test_result, visualize_result
    
    grid, max_walls = get_map(map=0)
    # Analyze grid and place walls
    place_walls([(x1, y1), (x2, y2)])
    num_saved = test_result()
    visualize_result()
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import ListedColormap
from collections import deque
from typing import List, Tuple, Optional

# Constants
CELL_OPEN = 0
CELL_WATER = 1
CELL_FIRE = 2
CELL_WALL = 3

# Global state
_current_grid: Optional[np.ndarray] = None
_total_open_cells: int = 0
_max_walls: int = 0
_placed_walls: List[Tuple[int, int]] = []
_highlight_data: dict = {'interest': [], 'candidate': []}

# Challenge maps
CHALLENGE_MAPS = [
    {
        'name': 'Two Fires',
        'grid': np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0],
            [2, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 2],
        ]),
        'max_walls': 5
    },
    {
        'name': 'Corner Fires',
        'grid': np.array([
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        ]),
        'max_walls': 10
    },
    {
        'name': 'Diagonal Fires',
        'grid': np.array([
            [2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2],
        ]),
        'max_walls': 3
    },
    {
        'name': 'Fire Row',
        'grid': np.array([
            [2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        'max_walls': 8
    },
    {
        'name': 'Two Rooms',
        'grid': np.array([
            [2, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        ]),
        'max_walls': 1
    },
    {
        'name': 'Central Town',
        'grid': np.array([
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 1, 1, 1, 1, 0, 0, 2],
            [2, 0, 0, 1, 0, 0, 1, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 1, 0, 0, 2],
            [2, 0, 0, 1, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 1, 0, 0, 1, 0, 0, 2],
            [2, 0, 0, 1, 0, 1, 1, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        ]),
        'max_walls': 3
    },
    {
        'name': 'Hallway Rooms',
        'grid': np.array([
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [2, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]),
        'max_walls': 1
    },
    {
        'name': 'Big Funnel',
        'grid': np.array([
            [2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        'max_walls': 4
    },
    {
        'name': 'Fake Doors',
        'grid': np.array([
            [2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [2, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0],
            [2, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
            [2, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
            [2, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        'max_walls': 4
    },
]


def get_map(map: int = 0) -> Tuple[np.ndarray, int, str]:
    """
    Get a challenge map for the fire spreading game.
    
    Args:
        map: Map number (0-len(CHALLENGE_MAPS)-1)
        
    Returns:
        Tuple of (grid, max_walls, name) where:
            - grid is a 2D numpy array with 0=open, 1=water, 2=fire
            - max_walls is the maximum number of walls allowed
            - name is the map name
    """
    global _current_grid, _total_open_cells, _max_walls, _placed_walls, _highlight_data
    
    if map < 0 or map >= len(CHALLENGE_MAPS):
        raise ValueError(f"Map {map} not found. Available maps: 0-{len(CHALLENGE_MAPS) - 1}")
    
    _current_grid = CHALLENGE_MAPS[map]['grid'].copy()
    _total_open_cells = int(np.sum(_current_grid == CELL_OPEN))
    _max_walls = CHALLENGE_MAPS[map]['max_walls']
    _placed_walls = []
    _highlight_data = {'interest': [], 'candidate': []}
    
    return _current_grid.copy(), _max_walls, CHALLENGE_MAPS[map]['name']


def get_available_maps() -> List[Tuple[int, str]]:
    """
    Get a list of all available challenge maps.
    
    Returns:
        List of (map_number, map_name) tuples
    """
    return [(i, map_data['name']) for i, map_data in enumerate(CHALLENGE_MAPS)]


def place_walls(cells: List[Tuple[int, int]]) -> None:
    """
    Place walls on the grid at specified coordinates.
    
    Args:
        cells: List of (x, y) tuples where walls should be placed
        
    Raises:
        ValueError: If trying to place too many walls or on invalid cells

    Note: grids are stored [y,x] but coordinates are given as (x,y) by math convention.
    """
    global _current_grid, _placed_walls, _max_walls
    
    if _current_grid is None:
        raise RuntimeError("Must call get_map() first")
    
    # Add new walls to existing walls
    _placed_walls.extend(cells)
    
    if len(_placed_walls) > _max_walls:
        raise ValueError(f"Too many walls! Maximum allowed: {_max_walls}, attempted: {len(_placed_walls)}")
    
    # Validate and place walls
    for x, y in cells:
        if x < 0 or x >= _current_grid.shape[1] or y < 0 or y >= _current_grid.shape[0]:
            raise ValueError(f"Cell ({x}, {y}) is out of bounds")
        
        if _current_grid[y, x] != CELL_OPEN:
            raise ValueError(f"Cannot place wall at ({x}, {y}). Cell must be open")
        
        _current_grid[y, x] = CELL_WALL


def _simulate_fire_spread(grid: np.ndarray) -> Tuple[np.ndarray, List[np.ndarray]]:
    """
    Simulate fire spreading across the grid.
    
    Args:
        grid: 2D numpy array with current grid state
        
    Returns:
        Tuple of (final_grid, history) where history is list of grid states over time
    
    Note: grids are stored [y,x] but coordinates are given as (x,y) by math convention.
    """
    height, width = grid.shape
    current = grid.copy()
    history = [current.copy()]
    
    # Find initial fire cells
    fire_cells = deque()
    for y in range(height):
        for x in range(width):
            if current[y, x] == CELL_FIRE:
                fire_cells.append((x, y))
    
    # Spread fire
    while fire_cells:
        next_fire = []
        processed = set()
        
        while fire_cells:
            x, y = fire_cells.popleft()
            
            if (x, y) in processed:
                continue
            processed.add((x, y))
            
            # Check 4 adjacent cells
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                
                if 0 <= nx < width and 0 <= ny < height:
                    if current[ny, nx] == CELL_OPEN:
                        current[ny, nx] = CELL_FIRE
                        next_fire.append((nx, ny))
        
        if next_fire:
            fire_cells.extend(next_fire)
            history.append(current.copy())
    
    return current, history


def test_result() -> int:
    """
    Test the current wall placement and return number of cells saved.
    
    Returns:
        Number of open cells saved from fire
    """
    global _current_grid
    
    if _current_grid is None:
        raise RuntimeError("Must call get_map() first")
    final_grid, _ = _simulate_fire_spread(_current_grid)
    num_saved = np.sum(final_grid == CELL_OPEN)
    return num_saved


def highlight_cells(cells: List[Tuple[int, int]], level: int) -> None:
    """
    Highlight cells for visualization.
    
    Args:
        cells: List of (x, y) tuples to highlight
        level: 1 for 'interest', 2 for 'candidate'
    """
    global _highlight_data
    
    if level == 1:
        _highlight_data['interest'].extend(cells)
    elif level == 2:
        _highlight_data['candidate'].extend(cells)
    else:
        raise ValueError("Level must be 1 (interest) or 2 (candidate)")


def highlight_clear() -> None:
    """Clear all highlighted cells."""
    global _highlight_data
    _highlight_data = {'interest': [], 'candidate': []}


def visualize_result() -> None:
    """
    Display an animated visualization of the fire spreading across the grid.
    """
    global _current_grid, _placed_walls, _highlight_data, _total_open_cells
    
    if _current_grid is None:
        raise RuntimeError("Must call get_map() first")
    
    # Simulate fire spread and get history
    final_grid, history = _simulate_fire_spread(_current_grid)
    
    # Count saved cells
    num_saved = np.sum(final_grid == CELL_OPEN)
    total_open = _total_open_cells
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.ion()
    
    height, width = history[0].shape
    colors = ['white', 'dodgerblue', 'orangered', 'gray']
    cmap = ListedColormap(colors)
    
    # Create image with colormap: 0=white, 1=blue, 2=red, 3=gray
    img = ax.imshow(history[0], interpolation='nearest', cmap=cmap,
                    vmin=0, vmax=3, aspect='auto', origin='upper')
    
    # Draw highlights
    for x, y in _highlight_data.get('interest', []):
        rect = Rectangle((x - 0.5, y - 0.5), 1, 1, fill=False, 
                         edgecolor='yellow', linewidth=3)
        ax.add_patch(rect)
    
    for x, y in _highlight_data.get('candidate', []):
        rect = Rectangle((x - 0.5, y - 0.5), 1, 1, fill=False, 
                         edgecolor='orange', linewidth=3)
        ax.add_patch(rect)
    
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(height - 0.5, -0.5)
    ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, height, 1), minor=True)
    ax.grid(which='minor', alpha=0.5, color='black', linewidth=0.5)
    ax.tick_params(which='minor', size=0)  # Hide minor tick marks
    ax.set_xticks(range(width))
    ax.set_yticks(range(height))
    
    title = f'Fire Spread Simulation - Frame 1/{len(history)}\n'
    title += f'Cells Saved: {num_saved}/{total_open} | Walls Used: {len(_placed_walls)}/{_max_walls}'
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(0.1)
    
    # Animation loop
    frame = 0
    
    try:
        while plt.fignum_exists(fig.number):
            # Update image and title
            img.set_data(history[frame])
            title = f'Fire Spread Simulation - Frame {frame + 1}/{len(history)}\n'
            title += f'Cells Saved: {num_saved}/{total_open} | Walls Used: {len(_placed_walls)}/{_max_walls}'
            ax.set_title(title, fontsize=14, fontweight='bold')
            
            # Redraw and wait
            fig.canvas.draw_idle()
            fig.canvas.flush_events()
            time.sleep(0.5)
            
            frame = (frame + 1) % len(history)
    except KeyboardInterrupt:
        pass
    
    plt.ioff()
    plt.close(fig)


# Export public API
__all__ = [
    'get_map',
    'get_available_maps',
    'place_walls',
    'test_result',
    'highlight_cells',
    'highlight_clear',
    'visualize_result',
]
