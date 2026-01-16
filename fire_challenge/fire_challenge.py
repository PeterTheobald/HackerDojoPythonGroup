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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from collections import deque
from typing import List, Tuple, Optional

# Global state
_current_grid: Optional[np.ndarray] = None
_original_grid: Optional[np.ndarray] = None
_max_walls: int = 0
_placed_walls: List[Tuple[int, int]] = []
_highlight_data: dict = {'interest': [], 'candidate': []}

# Challenge maps
CHALLENGE_MAPS = {
    0: {
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
    1: {
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
    2: {
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
    3: {
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
}


def get_map(map: int = 0) -> Tuple[np.ndarray, int]:
    """
    Get a challenge map for the fire spreading game.
    
    Args:
        map: Map number (0-3)
        
    Returns:
        Tuple of (grid, max_walls) where:
            - grid is a 2D numpy array with 0=open, 1=water, 2=fire
            - max_walls is the maximum number of walls allowed
    """
    global _current_grid, _original_grid, _max_walls, _placed_walls, _highlight_data
    
    if map not in CHALLENGE_MAPS:
        raise ValueError(f"Map {map} not found. Available maps: {list(CHALLENGE_MAPS.keys())}")
    
    _original_grid = CHALLENGE_MAPS[map]['grid'].copy()
    _current_grid = _original_grid.copy()
    _max_walls = CHALLENGE_MAPS[map]['max_walls']
    _placed_walls = []
    _highlight_data = {'interest': [], 'candidate': []}
    
    return _current_grid.copy(), _max_walls


def place_walls(cells: List[Tuple[int, int]]) -> None:
    """
    Place walls on the grid at specified coordinates.
    
    Args:
        cells: List of (x, y) tuples where walls should be placed
        
    Raises:
        ValueError: If trying to place too many walls or on invalid cells
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
        
        if _original_grid[y, x] != 0:
            raise ValueError(f"Cannot place wall at ({x}, {y}). Cell must be open (value 0)")
        
        _current_grid[y, x] = 3  # 3 represents a wall


def _simulate_fire_spread(grid: np.ndarray) -> Tuple[np.ndarray, List[np.ndarray]]:
    """
    Simulate fire spreading across the grid.
    
    Args:
        grid: 2D numpy array with current grid state
        
    Returns:
        Tuple of (final_grid, history) where history is list of grid states over time
    """
    height, width = grid.shape
    current = grid.copy()
    history = [current.copy()]
    
    # Find initial fire cells
    fire_cells = deque()
    for y in range(height):
        for x in range(width):
            if current[y, x] == 2:
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
                    if current[ny, nx] == 0:  # Open cell
                        current[ny, nx] = 2
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
    global _current_grid, _original_grid
    
    if _current_grid is None:
        raise RuntimeError("Must call get_map() first")
    
    # Simulate fire spread
    final_grid, _ = _simulate_fire_spread(_current_grid)
    
    # Count saved cells (cells that are still open - value 0)
    num_saved = np.sum(final_grid == 0)
    
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
    global _current_grid, _placed_walls, _highlight_data
    
    if _current_grid is None:
        raise RuntimeError("Must call get_map() first")
    
    # Simulate fire spread and get history
    final_grid, history = _simulate_fire_spread(_current_grid)
    
    # Count saved cells
    num_saved = np.sum(final_grid == 0)
    total_open = np.sum(_original_grid == 0)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Color map: white=open, blue=water, red=fire, gray=wall
    colors = {
        0: '#FFFFFF',  # Open - white
        1: '#1E90FF',  # Water - blue
        2: '#FF4500',  # Fire - red
        3: '#808080',  # Wall - gray
    }
    
    def draw_grid(grid_state, frame_num):
        ax.clear()
        height, width = grid_state.shape
        
        # Draw grid cells
        for y in range(height):
            for x in range(width):
                color = colors.get(grid_state[y, x], '#FFFFFF')
                rect = Rectangle((x, y), 1, 1, facecolor=color, edgecolor='black', linewidth=0.5)
                ax.add_patch(rect)
        
        # Draw highlight frames
        for x, y in _highlight_data.get('interest', []):
            rect = Rectangle((x, y), 1, 1, fill=False, edgecolor='yellow', linewidth=3)
            ax.add_patch(rect)
        
        for x, y in _highlight_data.get('candidate', []):
            rect = Rectangle((x, y), 1, 1, fill=False, edgecolor='orange', linewidth=3)
            ax.add_patch(rect)
        
        # Set axis properties
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.set_xticks(range(width))
        ax.set_yticks(range(height))
        ax.grid(True, alpha=0.3)
        
        # Title with progress
        title = f'Fire Spread Simulation - Frame {frame_num + 1}/{len(history)}\n'
        title += f'Cells Saved: {num_saved}/{total_open} | Walls Used: {len(_placed_walls)}/{_max_walls}'
        ax.set_title(title, fontsize=14, fontweight='bold')
    
    # Create animation
    def animate(frame):
        draw_grid(history[frame], frame)
    
    anim = animation.FuncAnimation(fig, animate, frames=len(history), 
                                   interval=500, repeat=True)
    
    plt.tight_layout()
    plt.show()


# Export public API
__all__ = [
    'get_map',
    'place_walls',
    'test_result',
    'highlight_cells',
    'highlight_clear',
    'visualize_result',
]
