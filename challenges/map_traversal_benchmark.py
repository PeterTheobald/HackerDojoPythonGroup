#!/usr/bin/env python3
"""
Map Traversal Algorithm Benchmark System

This system allows easy contribution and comparison of pathfinding algorithms.
Contributors can add algorithms to map_algorithms.py using the @register_algorithm decorator.
"""

import argparse
import importlib
import inspect
import sys
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import benchmark

# Global registry for algorithms
_algorithm_registry: List[Dict[str, Any]] = []


def register_algorithm(name: str, description: str = ""):
    """Decorator to register a pathfinding algorithm.

    Usage in map_algorithms.py:
        @register_algorithm(name="My Algorithm", description="Does cool things")
        def solve_my_algo(grid, tracer):
            # implementation
            return path
    """

    def decorator(func: Callable):
        _algorithm_registry.append(
            {"name": name, "description": description, "function": func}
        )
        return func

    return decorator


class Tracer:
    """Captures the exploration state of pathfinding algorithms."""

    def __init__(self, grid_size: Tuple[int, int], visualizer=None, grid=None, start_pos=None, end_pos=None):
        self.n_rows, self.n_cols = grid_size
        self.visited_order = []  # List of (row, col, state)
        self.visited_set = set()
        self.backtracks = 0
        self.cells_explored = 0
        self.visualizer = visualizer
        self.grid = grid
        self.start_pos = start_pos if start_pos else (0, 0)
        self.end_pos = end_pos if end_pos else (grid_size[0] - 1, grid_size[1] - 1)

    def visit(self, row: int, col: int, state: str = "exploring"):
        """Record a cell visit.

        Args:
            row, col: Cell coordinates
            state: "exploring", "backtrack", or "path"
        """
        self.visited_order.append((row, col, state))
        if state == "exploring":
            if (row, col) not in self.visited_set:
                self.visited_set.add((row, col))
                self.cells_explored += 1
        elif state == "backtrack":
            self.backtracks += 1

        # Real-time visualization
        if self.visualizer and self.grid:
            self.visualizer.update_cell(self.grid, row, col, state, self.visited_set)

    def get_stats(self) -> Dict[str, int]:
        """Return exploration statistics."""
        return {
            "cells_explored": self.cells_explored,
            "backtracks": self.backtracks,
            "total_steps": len(self.visited_order),
        }

    def get_heatmap(self) -> List[List[int]]:
        """Return a heatmap showing visit frequency."""
        heatmap = [[0 for _ in range(self.n_cols)] for _ in range(self.n_rows)]
        for row, col, _ in self.visited_order:
            heatmap[row][col] += 1
        return heatmap


class Visualizer:
    """Visualize algorithm exploration patterns with real-time terminal graphics."""

    # ANSI color codes
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BOLD = "\033[1m"

    def __init__(self, animation_speed: float = 0.001, start_pos=None, end_pos=None):
        self.animation_speed = animation_speed
        self.start_row = 0
        self.start_pos = start_pos if start_pos else (0, 0)
        self.end_pos = end_pos

    def clear_screen(self):
        """Clear terminal screen."""
        print("\033[2J\033[H", end="", flush=True)

    def move_cursor(self, row: int, col: int):
        """Move cursor to specific position."""
        print(f"\033[{row};{col}H", end="", flush=True)

    def get_cell_display(
        self, grid: List[List[int]], row: int, col: int, state: str, visited: set
    ) -> str:
        """Get colored character for a cell."""
        n, m = len(grid), len(grid[0])

        if (row, col) == self.start_pos:
            return f"{self.BG_GREEN}{self.BLACK}{self.BOLD}S{self.RESET}"
        elif self.end_pos and (row, col) == self.end_pos:
            return f"{self.BG_RED}{self.WHITE}{self.BOLD}E{self.RESET}"
        elif grid[row][col] == 1:
            # Wall - use bright white background with black block
            return f"{self.WHITE}{self.BG_WHITE}#{self.RESET}"
        elif state == "path":
            return f"{self.BG_YELLOW}{self.BLACK}*{self.RESET}"
        elif state == "backtrack":
            return f"{self.BG_MAGENTA}{self.WHITE}×{self.RESET}"
        elif state == "exploring" or (row, col) in visited:
            return f"{self.BG_BLUE}{self.WHITE}·{self.RESET}"
        else:
            return f"{self.BG_BLACK} {self.RESET}"

    def draw_grid(self, grid: List[List[int]], visited: set = None, path: set = None):
        """Draw the entire grid."""
        if visited is None:
            visited = set()
        if path is None:
            path = set()

        n, m = len(grid), len(grid[0])
        for i in range(n):
            line = []
            for j in range(m):
                if (i, j) in path:
                    state = "path"
                elif (i, j) in visited:
                    state = "exploring"
                else:
                    state = "empty"
                line.append(self.get_cell_display(grid, i, j, state, visited))
            print("".join(line))

    def update_cell(
        self, grid: List[List[int]], row: int, col: int, state: str, visited: set
    ):
        """Update a single cell in real-time."""
        if self.start_row > 0:
            self.move_cursor(self.start_row + row, col + 1)
            print(
                self.get_cell_display(grid, row, col, state, visited),
                end="",
                flush=True,
            )
            time.sleep(self.animation_speed)

    def start_visualization(self, grid: List[List[int]], algorithm_name: str):
        """Initialize visualization for an algorithm."""
        self.clear_screen()
        # Move cursor to top-left to ensure we start fresh
        self.move_cursor(1, 1)
        print(f"{self.BOLD}{self.CYAN}Running: {algorithm_name}{self.RESET}")
        print(
            f"{self.GREEN}S{self.RESET}=Start {self.RED}E{self.RESET}=End "
            + f"{self.BLUE}·{self.RESET}=Explored {self.YELLOW}*{self.RESET}=Path "
            + f"{self.MAGENTA}×{self.RESET}=Backtrack {self.WHITE}█{self.RESET}=Wall"
        )
        print()  # Blank line before grid

        # Record starting position for grid
        # Line 1: Running...
        # Line 2: Legend
        # Line 3: Blank
        # Line 4: First grid row
        self.start_row = 4

        # Draw initial grid fresh
        self.draw_grid(grid)

    def print_stats(
        self, name: str, stats: Dict[str, int], path: Optional[List[Tuple[int, int]]]
    ):
        """Print algorithm statistics."""
        n_rows = stats.get("grid_rows", 20)
        self.move_cursor(self.start_row + n_rows + 2, 1)
        print(f"\n{self.BOLD}{name} Statistics:{self.RESET}")
        print(f"  Cells explored: {self.CYAN}{stats['cells_explored']}{self.RESET}")
        print(f"  Backtracks: {self.MAGENTA}{stats['backtracks']}{self.RESET}")
        print(f"  Total steps: {stats['total_steps']}")
        if path:
            print(f"  Path length: {self.YELLOW}{len(path)}{self.RESET}")
        else:
            print(f"  Path length: {self.RED}N/A (no path found){self.RESET}")

    @staticmethod
    def print_grid(grid: List[List[int]]):
        """Print the raw grid."""
        print("\nGrid Layout (0=open, 1=wall):")
        for row in grid:
            print("".join(str(cell) for cell in row))

    @staticmethod
    def print_path(grid: List[List[int]], path: Optional[List[Tuple[int, int]]]):
        """Print grid with path marked."""
        if not path:
            print("No path found!")
            return

        n, m = len(grid), len(grid[0])
        display = [
            ["." if grid[i][j] == 0 else "#" for j in range(m)] for i in range(n)
        ]

        for row, col in path:
            if display[row][col] == ".":
                display[row][col] = "*"

        display[0][0] = "S"
        display[n - 1][m - 1] = "E"

        print("\nPath (S=start, E=end, *=path, #=wall, .=open):")
        for row in display:
            print("".join(row))

    @staticmethod
    def print_heatmap(grid: List[List[int]], heatmap: List[List[int]]):
        """Print exploration heatmap."""
        n, m = len(grid), len(grid[0])
        max_visits = max(max(row) for row in heatmap)

        if max_visits == 0:
            print("No cells explored!")
            return

        print("\nExploration Heatmap (darker = more visits):")
        # Use intensity characters
        chars = " .:-=+*#%@"
        for i in range(n):
            line = []
            for j in range(m):
                if grid[i][j] == 1:
                    line.append("#")
                elif heatmap[i][j] == 0:
                    line.append(" ")
                else:
                    intensity = min(9, int(heatmap[i][j] / max_visits * 9))
                    line.append(chars[intensity])
            print("".join(line))


def discover_algorithms():
    """Import map_algorithms.py and discover algorithms."""
    algorithms = []
    try:
        # Import the module
        import map_algorithms

        # Get algorithm metadata from module
        if hasattr(map_algorithms, "ALGORITHMS"):
            for algo_info in map_algorithms.ALGORITHMS:
                func_name = algo_info["function"]
                if hasattr(map_algorithms, func_name):
                    algorithms.append(
                        {
                            "name": algo_info["name"],
                            "description": algo_info.get("description", ""),
                            "function": getattr(map_algorithms, func_name),
                        }
                    )
    except ImportError as e:
        print(f"Warning: map_algorithms.py not found. Error: {e}")
    except Exception as e:
        print(f"Error loading algorithms: {e}")
        import traceback

        traceback.print_exc()

    return algorithms


def run_benchmark(
    grid: List[List[int]],
    start_pos: Tuple[int, int] = (0, 0),
    end_pos: Tuple[int, int] = None,
    num_runs: int = 1000,
    visualize: bool = True,
    animation_speed: float = 0.001,
):
    """Run benchmark on all registered algorithms."""
    algorithms = discover_algorithms()

    if not algorithms:
        print("No algorithms registered! Add algorithms to map_algorithms.py")
        return

    print(f"\nFound {len(algorithms)} algorithms to benchmark:")
    for algo in algorithms:
        desc = f" - {algo['description']}" if algo["description"] else ""
        print(f"  • {algo['name']}{desc}")

    n, m = len(grid), len(grid[0])
    
    # Default end_pos to bottom-right if not specified
    if end_pos is None:
        end_pos = (n - 1, m - 1)

    # First, run animated visualizations
    if visualize:
        visualizer = Visualizer(animation_speed=animation_speed, start_pos=start_pos, end_pos=end_pos)

        for i, algo in enumerate(algorithms):
            # Show initial unexplored map
            visualizer.clear_screen()
            print(
                f"\n{visualizer.BOLD}{visualizer.CYAN}Algorithm {i+1}/{len(algorithms)}: {algo['name']}{visualizer.RESET}"
            )
            if algo["description"]:
                print(f"{visualizer.WHITE}{algo['description']}{visualizer.RESET}")
            print(
                f"\n{visualizer.GREEN}S{visualizer.RESET}=Start {visualizer.RED}E{visualizer.RESET}=End "
                + f"{visualizer.BLUE}·{visualizer.RESET}=Explored {visualizer.YELLOW}*{visualizer.RESET}=Path "
                + f"{visualizer.MAGENTA}×{visualizer.RESET}=Backtrack {visualizer.WHITE}█{visualizer.RESET}=Wall\n"
            )

            visualizer.draw_grid(grid, visited=set(), path=set())

            # Wait for user to start - use print instead of input prompt to avoid newline issues
            print(
                f"\n{visualizer.BOLD}{visualizer.GREEN}Press Enter to start animation...{visualizer.RESET}",
                end="",
                flush=True,
            )
            input()  # Get input without printing anything else

            # Immediately clear screen to prevent scrolling offset
            visualizer.start_visualization(grid, algo["name"])

            # Run with visualization
            tracer = Tracer((n, m), visualizer=visualizer, grid=grid, start_pos=start_pos, end_pos=end_pos)
            path = algo["function"](grid, tracer, start_pos, end_pos)

            # Show final path
            if path:
                for row, col in path:
                    visualizer.update_cell(grid, row, col, "path", tracer.visited_set)

            stats = tracer.get_stats()
            stats["grid_rows"] = n
            visualizer.print_stats(algo["name"], stats, path)

            # Wait for user input before next algorithm
            if i < len(algorithms) - 1:
                input(
                    f"\n{visualizer.BOLD}Press Enter to continue to next algorithm...{visualizer.RESET}"
                )
            else:
                input(
                    f"\n{visualizer.BOLD}Press Enter to continue to benchmark...{visualizer.RESET}"
                )

        print(
            f"\n\n{visualizer.BOLD}{visualizer.GREEN}Animation complete!{visualizer.RESET}"
        )
        print(
            f"\n{visualizer.BOLD}Now running performance benchmark...{visualizer.RESET}\n"
        )
        time.sleep(1)

    # Prepare benchmark data (non-animated for speed)
    benchmark_algos = []

    for algo in algorithms:

        def make_wrapper(func):
            def wrapper(data):
                grid, tracer = data
                return func(grid, tracer, tracer.start_pos, tracer.end_pos)

            return wrapper

        def make_setup(grid_data, size, s_pos, e_pos):
            def setup():
                tracer = Tracer(size, start_pos=s_pos, end_pos=e_pos)  # No visualizer for benchmark
                return (grid_data, tracer)

            return setup

        benchmark_algos.append(
            {
                "title": algo["name"],
                "algorithm_fn": make_wrapper(algo["function"]),
                "setup_fn": make_setup(grid, (n, m), start_pos, end_pos),
            }
        )

    # Run benchmark
    print(f"Running benchmark with {num_runs} iterations per algorithm...")
    results = benchmark.run(benchmark_algos, REPEAT=num_runs)

    return results


def load_map_from_sample():
    """Load the map from map_samplemap.py, converting spaces to 0 and # to 1.
    
    Returns:
        Tuple of (grid, start_pos, end_pos) where:
        - grid: 2D list with 0=open, 1=wall
        - start_pos: (row, col) for start position (from 'S' or default to (0,0))
        - end_pos: (row, col) for end position (from 'F' or default to bottom-right)
    """
    try:
        import map_samplemap

        # Strip only newlines, not all whitespace, to preserve leading spaces
        lines = map_samplemap.sample_map.strip("\n").split("\n")
        # Find the maximum line length to pad all rows
        max_len = max(len(line) for line in lines)

        grid = []
        start_pos = None
        end_pos = None
        
        for row_idx, line in enumerate(lines):
            # Pad line to max length if needed
            padded_line = line.ljust(max_len)
            row = []
            for col_idx, char in enumerate(padded_line):
                if char == 'S':
                    start_pos = (row_idx, col_idx)
                    row.append(0)  # S is an open cell
                elif char == 'E':
                    end_pos = (row_idx, col_idx)
                    row.append(0)  # F is an open cell
                elif char == '#':
                    row.append(1)  # Wall
                else:
                    row.append(0)  # Open space
            grid.append(row)

        # Default to top-left and bottom-right if not specified
        if start_pos is None:
            start_pos = (0, 0)
            # Ensure start position is open
            if grid[0][0] == 1:
                grid[0][0] = 0
        
        if end_pos is None:
            end_pos = (len(grid) - 1, len(grid[0]) - 1)
            # Ensure end position is open
            if grid[-1][-1] == 1:
                grid[-1][-1] = 0

        return grid, start_pos, end_pos
    except ImportError as e:
        print(f"Warning: map_samplemap.py not found ({e}), using default 20x20 grid")
        # Simple default grid
        return [[0 for _ in range(20)] for _ in range(20)], (0, 0), (19, 19)
    except Exception as e:
        print(f"Error loading map: {e}")
        import traceback

        traceback.print_exc()
        return [[0 for _ in range(20)] for _ in range(20)], (0, 0), (19, 19)


def main():
    """Main benchmark runner."""
    parser = argparse.ArgumentParser(description='Benchmark map traversal algorithms with visualization')
    parser.add_argument('--repeat', type=int, default=1000, help='Number of iterations for each benchmark (default: 1000)')
    parser.add_argument('--no-visualize', action='store_true', help='Disable visualization')
    parser.add_argument('--animation-speed', type=float, default=0.005, help='Animation delay in seconds (default: 0.005)')
    args = parser.parse_args()
    
    print("=" * 80)
    print("MAP TRAVERSAL ALGORITHM BENCHMARK")
    print("=" * 80)

    # Load grid from sample map
    grid, start_pos, end_pos = load_map_from_sample()
    print(f"Map size: {len(grid)}x{len(grid[0])}")
    print(f"Start: {start_pos}, End: {end_pos}")
    print()

    # Run benchmark with real-time animation
    # animation_speed controls delay between steps (larger = slower)
    # For large maps, use very small delay or set visualize=False
    run_benchmark(
        grid,
        start_pos=start_pos,
        end_pos=end_pos,
        num_runs=args.repeat, 
        visualize=not args.no_visualize, 
        animation_speed=args.animation_speed
    )


if __name__ == "__main__":
    main()
