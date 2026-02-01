"""
Fire Challenge Module
=====================

A game module where players write Python code to place walls on a grid to block fire spread.

Grid values:
- 0: Open cell (can catch fire)
- 1: Water cell (blocks fire)
- 2: Starting fire cell
- 3: Wall cell (placed by player)

Usage (New Class-Based API):
    from fire_challenge import FireChallenge
    
    game = FireChallenge(map=0)
    print(game.grid)
    game.place_walls([(x1, y1), (x2, y2)])
    num_saved = game.test_result()
    game.visualize()

Legacy Usage (Deprecated):
    from fire_challenge import get_map, place_walls, test_result, visualize_result
    
    grid, max_walls = get_map(map=0)
    place_walls([(x1, y1), (x2, y2)])
    num_saved = test_result()
    visualize_result()
"""

import time
from collections import deque

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle

from .challenge_maps import CHALLENGE_MAPS

# Constants
CELL_OPEN = 0
CELL_WATER = 1
CELL_FIRE = 2
CELL_WALL = 3


class FireChallenge:
    """
    A fire spreading challenge game where players place walls to block fire propagation.
    
    Example:
        game = FireChallenge(map=0)
        game.place_walls([(1, 2), (3, 4)])
        score = game.test_result()
        game.visualize()
    """
    
    def __init__(self, map: int = 0):
        """
        Initialize a new fire challenge game.
        
        Args:
            map: Map number (0-len(available_maps)-1)
        """
        if map < 0 or map >= len(CHALLENGE_MAPS):
            raise ValueError(f"Map {map} not found. Available maps: 0-{len(CHALLENGE_MAPS) - 1}")
        
        self._map_number = map
        self._map_name = CHALLENGE_MAPS[map]['name']
        self._original_grid = CHALLENGE_MAPS[map]['grid'].copy()
        self._current_grid = self._original_grid.copy()
        self._max_walls = CHALLENGE_MAPS[map]['max_walls']
        self._total_open_cells = int(np.sum(self._original_grid == CELL_OPEN))
        self._placed_walls: list[tuple[int, int]] = []
        self._highlight_data: dict[str, list[tuple[int, int]]] = {'interest': [], 'candidate': []}
    
    @staticmethod
    def get_available_maps() -> list[tuple[int, str]]:
        """
        Get list of all available built-in maps.
        
        Returns:
            List of tuples containing (map_number, map_name)
        """
        return [(i, info['name']) for i, info in enumerate(CHALLENGE_MAPS)]
    
    @classmethod
    def from_custom_grid(cls, grid: np.ndarray, max_walls: int, name: str = "Custom Map") -> 'FireChallenge':
        """
        Create a fire challenge from a custom grid.
        
        Args:
            grid: 2D numpy array with 0=open, 1=water, 2=fire
            max_walls: Maximum number of walls allowed
            name: Display name for the map
            
        Returns:
            New FireChallenge instance
        """
        if not isinstance(grid, np.ndarray):
            raise TypeError("Grid must be a numpy array")
        
        if grid.ndim != 2:
            raise ValueError("Grid must be a 2D array")
        
        instance = cls.__new__(cls)
        instance._map_number = None
        instance._map_name = name
        instance._original_grid = grid.copy()
        instance._current_grid = grid.copy()
        instance._max_walls = max_walls
        instance._total_open_cells = int(np.sum(grid == CELL_OPEN))
        instance._placed_walls = []
        instance._highlight_data = {'interest': [], 'candidate': []}
        
        return instance
    
    @classmethod
    def from_string(cls, map_string: str, max_walls: int, name: str = "Custom Map") -> 'FireChallenge':
        """
        Create a fire challenge from a string representation.
        
        Args:
            map_string: Multi-line string where ' '=open, '#'=water, '*'=fire
            max_walls: Maximum number of walls allowed
            name: Display name for the map
            
        Returns:
            New FireChallenge instance
            
        Example:
            map_str = '''
            *   #
                #
            #####
               *
            '''
            game = FireChallenge.from_string(map_str, max_walls=3, name="My Map")
        """
        lines = map_string.strip().split('\n')
        
        char_map = {' ': CELL_OPEN, '#': CELL_WATER, '*': CELL_FIRE}
        
        grid_data = []
        for line in lines:
            row = []
            for char in line:
                if char not in char_map:
                    raise ValueError(f"Invalid character '{char}' in map string. Use ' ', '#', or '*'")
                row.append(char_map[char])
            grid_data.append(row)
        
        if grid_data:
            max_len = max(len(row) for row in grid_data)
            for row in grid_data:
                while len(row) < max_len:
                    row.append(CELL_OPEN)
        
        grid = np.array(grid_data)
        return cls.from_custom_grid(grid, max_walls, name)
    
    def place_walls(self, cells: list[tuple[int, int]]) -> None:
        """
        Place walls on the grid at specified coordinates.
        
        Args:
            cells: List of (x, y) tuples where walls should be placed
            
        Raises:
            ValueError: If trying to place too many walls or on invalid cells
        
        Note: Coordinates are given as (x, y) by math convention.
        """
        # Check if adding these walls would exceed the limit (before modifying state)
        if len(self._placed_walls) + len(cells) > self._max_walls:
            raise ValueError(f"Too many walls! Maximum allowed: {self._max_walls}, current: {len(self._placed_walls)}, attempting to add: {len(cells)}")
        
        # Validate all wall positions before modifying state
        for x, y in cells:
            if x < 0 or x >= self._current_grid.shape[1] or y < 0 or y >= self._current_grid.shape[0]:
                raise ValueError(f"Cell ({x}, {y}) is out of bounds. Grid size: {self._current_grid.shape[1]}x{self._current_grid.shape[0]}")
            
            if self._current_grid[y, x] != CELL_OPEN:
                raise ValueError(f"Cannot place wall at ({x}, {y}). Cell must be open (currently: {self._current_grid[y, x]})")
        
        # All validations passed - now modify state
        for x, y in cells:
            self._current_grid[y, x] = CELL_WALL
        self._placed_walls.extend(cells)
    
    def test_result(self) -> int:
        """
        Test the current wall placement and return number of cells saved.
        
        Returns:
            Number of open cells saved from fire
        """
        final_grid, _ = self._simulate_fire_spread(self._current_grid)
        num_saved = int(np.sum(final_grid == CELL_OPEN))
        return num_saved
    
    def reset(self) -> None:
        """Reset the game, removing all placed walls and highlights."""
        self._current_grid = self._original_grid.copy()
        self._placed_walls = []
        self._highlight_data = {'interest': [], 'candidate': []}
    
    def highlight_cells(self, cells: list[tuple[int, int]], level: int) -> None:
        """
        Highlight cells for visualization.
        
        Args:
            cells: List of (x, y) tuples to highlight
            level: 1 for 'interest' (yellow), 2 for 'candidate' (orange)
        """
        if level == 1:
            self._highlight_data['interest'].extend(cells)
        elif level == 2:
            self._highlight_data['candidate'].extend(cells)
        else:
            raise ValueError("Level must be 1 (interest) or 2 (candidate)")
    
    def highlight_clear(self) -> None:
        """Clear all highlighted cells."""
        self._highlight_data = {'interest': [], 'candidate': []}
    
    def print_map(self, format: str = 'int') -> None:
        """
        Print the current map to the console.
        
        Args:
            format: Display format - 'int' for numeric grid or 'str' for visual characters
                   - 'int': Shows grid as numbers (0=open, 1=water, 2=fire, 3=wall)
                   - 'str': Shows grid as characters (' '=open, '#'=water, '*'=fire, 'W'=wall)
        
        Example:
            game.print_map('int')   # Shows: [[0 0 1] [2 0 3] ...]
            game.print_map('str')   # Shows:   #
                                    #          *  W
        """
        if format == 'int':
            print(self._current_grid)
        elif format == 'str':
            char_map = {
                CELL_OPEN: ' ',
                CELL_WATER: '#',
                CELL_FIRE: '*',
                CELL_WALL: 'W'
            }
            width = self._current_grid.shape[1]
            print('┌' + '─' * width + '┐')
            for row in self._current_grid:
                line = ''.join(char_map.get(cell, '?') for cell in row)
                print('│' + line + '│')
            print('└' + '─' * width + '┘')
        else:
            raise ValueError(f"Invalid format '{format}'. Use 'int' or 'str'")
    
    def get_map_string(self, format: str = 'str') -> str:
        """
        Get the current map as a string.
        
        Args:
            format: Display format - 'int' for numeric grid or 'str' for visual characters
                   - 'int': Returns grid as string representation of numbers
                   - 'str': Returns grid as character string (' '=open, '#'=water, '*'=fire, 'W'=wall)
        
        Returns:
            String representation of the current map
        
        Example:
            map_str = game.get_map_string('str')
        """
        if format == 'int':
            return str(self._current_grid)
        elif format == 'str':
            char_map = {
                CELL_OPEN: ' ',
                CELL_WATER: '#',
                CELL_FIRE: '*',
                CELL_WALL: 'W'
            }
            width = self._current_grid.shape[1]
            lines = ['┌' + '─' * width + '┐']
            for row in self._current_grid:
                line = ''.join(char_map.get(cell, '?') for cell in row)
                lines.append('│' + line + '│')
            lines.append('└' + '─' * width + '┘')
            return '\n'.join(lines)
        else:
            raise ValueError(f"Invalid format '{format}'. Use 'int' or 'str'")
    
    def visualize(self) -> None:
        """Display an animated visualization of the fire spreading across the grid."""
        final_grid, history = self._simulate_fire_spread(self._current_grid)
        
        num_saved = int(np.sum(final_grid == CELL_OPEN))
        
        fig, ax = plt.subplots(figsize=(10, 10))
        plt.ion()
        
        height, width = history[0].shape
        colors = ['white', 'dodgerblue', 'orangered', 'gray', 'darkred']
        cmap = ListedColormap(colors)
        
        img = ax.imshow(history[0], interpolation='nearest', cmap=cmap,
                        vmin=0, vmax=4, aspect='auto', origin='upper')
        
        # Draw highlights
        for x, y in self._highlight_data.get('interest', []):
            rect = Rectangle((x - 0.5, y - 0.5), 1, 1, fill=False, 
                             edgecolor='yellow', linewidth=3)
            ax.add_patch(rect)
        
        for x, y in self._highlight_data.get('candidate', []):
            rect = Rectangle((x - 0.5, y - 0.5), 1, 1, fill=False, 
                             edgecolor='orange', linewidth=3)
            ax.add_patch(rect)
        
        ax.set_xlim(-0.5, width - 0.5)
        ax.set_ylim(height - 0.5, -0.5)
        ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, height, 1), minor=True)
        ax.grid(which='minor', alpha=0.5, color='black', linewidth=0.5)
        ax.tick_params(which='minor', size=0)
        ax.set_xticks(range(width))
        ax.set_yticks(range(height))
        
        map_info = f"Map {self._map_number}: {self._map_name}" if self._map_number is not None else self._map_name
        title = f'{map_info} - Frame 1/{len(history)}\n'
        title += f'Cells Saved: {num_saved}/{self._total_open_cells} | Walls Used: {len(self._placed_walls)}/{self._max_walls}'
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.show(block=False)
        plt.pause(0.1)
        
        frame = 0
        animation_complete = False
        
        try:
            while plt.fignum_exists(fig.number):
                img.set_data(history[frame])
                
                if animation_complete:
                    title = f'Fire Spread Complete - Final Result\n'
                else:
                    title = f'Fire Spread Simulation - Frame {frame + 1}/{len(history)}\n'
                title += f'Cells Saved: {num_saved}/{self._total_open_cells} | Walls Used: {len(self._placed_walls)}/{self._max_walls}'
                ax.set_title(title, fontsize=14, fontweight='bold')
                
                fig.canvas.draw_idle()
                fig.canvas.flush_events()
                
                if animation_complete:
                    time.sleep(0.1)
                else:
                    time.sleep(0.5)
                    frame += 1
                    if frame >= len(history):
                        frame = len(history) - 1
                        animation_complete = True
        except KeyboardInterrupt:
            pass
        
        plt.ioff()
        plt.close(fig)
    
    @staticmethod
    def _simulate_fire_spread(grid: np.ndarray) -> tuple[np.ndarray, list[np.ndarray]]:
        """
        Simulate fire spreading across the grid.
        
        Args:
            grid: 2D numpy array with current grid state
            
        Returns:
            Tuple of (final_grid, history) where history is list of grid states over time
        """
        height, width = grid.shape
        current = grid.copy()
        
        initial_fire_positions = []
        for y in range(height):
            for x in range(width):
                if current[y, x] == CELL_FIRE:
                    current[y, x] = 4  # Initial fire gets special value
                    initial_fire_positions.append((x, y))
        
        history = [current.copy()]
        fire_cells = deque(initial_fire_positions)
        
        while fire_cells:
            next_fire = []
            processed = set()
            
            while fire_cells:
                x, y = fire_cells.popleft()
                
                if (x, y) in processed:
                    continue
                processed.add((x, y))
                
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
    
    @property
    def grid(self) -> np.ndarray:
        """Current grid state (read-only copy)."""
        return self._current_grid.copy()
    
    @property
    def max_walls(self) -> int:
        """Maximum number of walls allowed."""
        return self._max_walls
    
    @property
    def name(self) -> str:
        """Map name."""
        return self._map_name
    
    @property
    def map_number(self) -> int | None:
        """Map number (None for custom maps)."""
        return self._map_number
    
    @property
    def walls_remaining(self) -> int:
        """Number of walls that can still be placed."""
        return self._max_walls - len(self._placed_walls)
    
    @property
    def walls_placed(self) -> list[tuple[int, int]]:
        """List of wall positions that have been placed (read-only copy)."""
        return self._placed_walls.copy()
    
    @property
    def total_open_cells(self) -> int:
        """Total number of open cells in the original grid."""
        return self._total_open_cells
    
    def __repr__(self) -> str:
        return f"FireChallenge(map={self._map_number}, name='{self._map_name}', walls={len(self._placed_walls)}/{self._max_walls})"


# ============================================================================
# Legacy Global Function API (Deprecated - use FireChallenge class instead)
# ============================================================================

# ============================================================================
# Legacy Global Function API (Deprecated - use FireChallenge class instead)
# ============================================================================

# Global state for legacy API
_current_game: FireChallenge | None = None


def get_map(map: int = 0) -> tuple[np.ndarray, int, str]:
    """
    Get a challenge map for the fire spreading game.
    
    **DEPRECATED**: Use FireChallenge class instead:
        game = FireChallenge(map=0)
    
    Args:
        map: Map number (0-len(CHALLENGE_MAPS)-1)
        
    Returns:
        Tuple of (grid, max_walls, name) where:
            - grid is a 2D numpy array with 0=open, 1=water, 2=fire
            - max_walls is the maximum number of walls allowed
            - name is the map name
    """
    global _current_game
    _current_game = FireChallenge(map=map)
    return _current_game.grid, _current_game.max_walls, _current_game.name


def get_custom_map(grid: np.ndarray, max_walls: int, name: str = "Custom Map") -> tuple[np.ndarray, int, str]:
    """
    Load a custom map for the fire spreading game.
    
    **DEPRECATED**: Use FireChallenge.from_custom_grid() instead:
        game = FireChallenge.from_custom_grid(grid, max_walls, name)
    
    Args:
        grid: 2D numpy array with 0=open, 1=water, 2=fire
        max_walls: Maximum number of walls allowed
        name: Display name for the map
        
    Returns:
        Tuple of (grid, max_walls, name)
    """
    global _current_game
    _current_game = FireChallenge.from_custom_grid(grid, max_walls, name)
    return _current_game.grid, _current_game.max_walls, _current_game.name


def get_custom_map_from_string(map_string: str, max_walls: int, name: str = "Custom Map") -> tuple[np.ndarray, int, str]:
    """
    Load a custom map from a string representation.
    
    **DEPRECATED**: Use FireChallenge.from_string() instead:
        game = FireChallenge.from_string(map_str, max_walls, name)
    
    Args:
        map_string: Multi-line string where:
            ' ' = open cell (0)
            '#' = water cell (1)
            '*' = fire cell (2)
        max_walls: Maximum number of walls allowed
        name: Display name for the map
        
    Returns:
        Tuple of (grid, max_walls, name)
        
    Example:
        map_str = '''
        *   #
            #
        #####
           *
        '''
        grid, max_walls, name = get_custom_map_from_string(map_str, max_walls=3, name="My Map")
    """
    global _current_game
    _current_game = FireChallenge.from_string(map_string, max_walls, name)
    return _current_game.grid, _current_game.max_walls, _current_game.name


def place_walls(cells: list[tuple[int, int]]) -> None:
    """
    Place walls on the grid at specified coordinates.
    
    **DEPRECATED**: Use FireChallenge class instead:
        game.place_walls(cells)
    
    Args:
        cells: List of (x, y) tuples where walls should be placed
        
    Raises:
        ValueError: If trying to place too many walls or on invalid cells
        RuntimeError: If get_map() hasn't been called first

    Note: grids are stored [y,x] but coordinates are given as (x,y) by math convention.
    """
    global _current_game
    
    if _current_game is None:
        raise RuntimeError("Must call get_map() first")
    
    _current_game.place_walls(cells)


def test_result() -> int:
    """
    Test the current wall placement and return number of cells saved.
    
    **DEPRECATED**: Use FireChallenge class instead:
        score = game.test_result()
    
    Returns:
        Number of open cells saved from fire
        
    Raises:
        RuntimeError: If get_map() hasn't been called first
    """
    global _current_game
    
    if _current_game is None:
        raise RuntimeError("Must call get_map() first")
    
    return _current_game.test_result()


def highlight_cells(cells: list[tuple[int, int]], level: int) -> None:
    """
    Highlight cells for visualization.
    
    **DEPRECATED**: Use FireChallenge class instead:
        game.highlight_cells(cells, level)
    
    Args:
        cells: List of (x, y) tuples to highlight
        level: 1 for 'interest', 2 for 'candidate'
        
    Raises:
        RuntimeError: If get_map() hasn't been called first
    """
    global _current_game
    
    if _current_game is None:
        raise RuntimeError("Must call get_map() first")
    
    _current_game.highlight_cells(cells, level)


def highlight_clear() -> None:
    """
    Clear all highlighted cells.
    
    **DEPRECATED**: Use FireChallenge class instead:
        game.highlight_clear()
        
    Raises:
        RuntimeError: If get_map() hasn't been called first
    """
    global _current_game
    
    if _current_game is None:
        raise RuntimeError("Must call get_map() first")
    
    _current_game.highlight_clear()


def visualize_result() -> None:
    """
    Display an animated visualization of the fire spreading across the grid.
    
    **DEPRECATED**: Use FireChallenge class instead:
        game.visualize()
        
    Raises:
        RuntimeError: If get_map() hasn't been called first
    """
    global _current_game
    
    if _current_game is None:
        raise RuntimeError("Must call get_map() first")
    
    _current_game.visualize()


# Export public API
__all__ = [
    # New class-based API (recommended)
    'FireChallenge',
    # Legacy function API (deprecated)
    'get_map',
    'get_custom_map',
    'get_custom_map_from_string',
    'place_walls',
    'test_result',
    'highlight_cells',
    'highlight_clear',
    'visualize_result',
]
