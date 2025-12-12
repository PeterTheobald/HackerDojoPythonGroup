#!/usr/bin/env python3
"""
Map Algorithms Module

Contributors: Add your pathfinding algorithms here.
Each function will be automatically registered by the benchmark system.

Algorithm Requirements:
- Signature: def solve_name(grid: List[List[int]], tracer) -> Optional[List[Tuple[int, int]]]
- grid: 2D list where 0=open, 1=wall
- tracer: Use tracer.visit(row, col, state) to record exploration
- Return: List of (row, col) tuples from (0,0) to (n-1,m-1), or None if no path
- Name your function starting with "solve_"
- Add a docstring describing your algorithm
"""

from typing import List, Tuple, Optional
from collections import deque
import heapq


# Algorithm metadata - add your algorithm info here
ALGORITHMS = [
    {"name": "BFS", "function": "solve_bfs", "description": "Breadth-First Search - guarantees shortest path"},
    {"name": "DFS", "function": "solve_dfs", "description": "Depth-First Search - may not find shortest path"},
    {"name": "A*", "function": "solve_astar", "description": "A* with Manhattan distance - optimal and efficient"},
    {"name": "Bidirectional BFS", "function": "solve_bidirectional_bfs", "description": "BFS from both ends - faster for long paths"},
    {"name": "Bidirectional A*", "function": "solve_bidirectional_astar", "description": "A* from both ends - optimal and very efficient"},
]


def solve_bfs(grid: List[List[int]], tracer) -> Optional[List[Tuple[int, int]]]:
    """Find shortest path using BFS."""
    if not grid or not grid[0]:
        return None
    
    n = len(grid)
    m = len(grid[0])
    
    if grid[0][0] == 1 or grid[n-1][m-1] == 1:
        return None
    
    queue = deque([(0, 0)])
    visited = {(0, 0)}
    parent = {(0, 0): None}
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        row, col = queue.popleft()
        tracer.visit(row, col, "exploring")
        
        if row == n - 1 and col == m - 1:
            # Reconstruct path
            path = []
            curr = (row, col)
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path = path[::-1]
            
            # Mark path in tracer
            for r, c in path:
                tracer.visit(r, c, "path")
            
            return path
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < n and 0 <= new_col < m and 
                grid[new_row][new_col] == 0 and 
                (new_row, new_col) not in visited):
                visited.add((new_row, new_col))
                parent[(new_row, new_col)] = (row, col)
                queue.append((new_row, new_col))
    
    return None


def solve_dfs(grid: List[List[int]], tracer) -> Optional[List[Tuple[int, int]]]:
    """Find a path using DFS (may not be shortest)."""
    if not grid or not grid[0]:
        return None
    
    n = len(grid)
    m = len(grid[0])
    
    if grid[0][0] == 1 or grid[n-1][m-1] == 1:
        return None
    
    visited = set()
    path = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def dfs(row, col):
        tracer.visit(row, col, "exploring")
        
        if row == n - 1 and col == m - 1:
            path.append((row, col))
            tracer.visit(row, col, "path")
            return True
        
        visited.add((row, col))
        path.append((row, col))
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < n and 0 <= new_col < m and 
                grid[new_row][new_col] == 0 and 
                (new_row, new_col) not in visited):
                if dfs(new_row, new_col):
                    tracer.visit(row, col, "path")
                    return True
        
        tracer.visit(row, col, "backtrack")
        path.pop()
        return False
    
    if dfs(0, 0):
        return path
    return None


def solve_astar(grid: List[List[int]], tracer) -> Optional[List[Tuple[int, int]]]:
    """Find shortest path using A* with Manhattan distance heuristic."""
    if not grid or not grid[0]:
        return None
    
    n = len(grid)
    m = len(grid[0])
    
    if grid[0][0] == 1 or grid[n-1][m-1] == 1:
        return None
    
    def heuristic(row, col):
        return abs(row - (n - 1)) + abs(col - (m - 1))
    
    # Priority queue: (f_score, g_score, row, col)
    open_heap = [(heuristic(0, 0), 0, 0, 0)]
    visited = set()
    parent = {(0, 0): None}
    g_score = {(0, 0): 0}
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while open_heap:
        f, g, row, col = heapq.heappop(open_heap)
        
        if (row, col) in visited:
            continue
        
        visited.add((row, col))
        tracer.visit(row, col, "exploring")
        
        if row == n - 1 and col == m - 1:
            # Reconstruct path
            path = []
            curr = (row, col)
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            path = path[::-1]
            
            # Mark path in tracer
            for r, c in path:
                tracer.visit(r, c, "path")
            
            return path
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            if (0 <= new_row < n and 0 <= new_col < m and 
                grid[new_row][new_col] == 0):
                tentative_g = g + 1
                
                if tentative_g < g_score.get((new_row, new_col), float('inf')):
                    g_score[(new_row, new_col)] = tentative_g
                    f_score = tentative_g + heuristic(new_row, new_col)
                    parent[(new_row, new_col)] = (row, col)
                    heapq.heappush(open_heap, (f_score, tentative_g, new_row, new_col))
    
    return None


def solve_bidirectional_bfs(grid: List[List[int]], tracer) -> Optional[List[Tuple[int, int]]]:
    """BFS from start and end simultaneously, meeting in the middle."""
    if not grid or not grid[0]:
        return None
    
    n = len(grid)
    m = len(grid[0])
    
    if grid[0][0] == 1 or grid[n-1][m-1] == 1:
        return None
    
    # Forward search from start
    queue_fwd = deque([(0, 0)])
    visited_fwd = {(0, 0): None}
    
    # Backward search from end
    queue_bwd = deque([(n-1, m-1)])
    visited_bwd = {(n-1, m-1): None}
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def reconstruct_path(meet_point):
        """Reconstruct path from both directions."""
        # Forward path
        path_fwd = []
        curr = meet_point
        while curr is not None:
            path_fwd.append(curr)
            curr = visited_fwd[curr]
        path_fwd = path_fwd[::-1]
        
        # Backward path
        path_bwd = []
        curr = visited_bwd[meet_point]
        while curr is not None:
            path_bwd.append(curr)
            curr = visited_bwd[curr]
        
        return path_fwd + path_bwd
    
    while queue_fwd or queue_bwd:
        # Forward step
        if queue_fwd:
            row, col = queue_fwd.popleft()
            tracer.visit(row, col, "exploring")
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < n and 0 <= new_col < m and 
                    grid[new_row][new_col] == 0):
                    
                    if (new_row, new_col) not in visited_fwd:
                        visited_fwd[(new_row, new_col)] = (row, col)
                        
                        # Check if we've met the backward search
                        if (new_row, new_col) in visited_bwd:
                            path = reconstruct_path((new_row, new_col))
                            for r, c in path:
                                tracer.visit(r, c, "path")
                            return path
                        
                        queue_fwd.append((new_row, new_col))
        
        # Backward step
        if queue_bwd:
            row, col = queue_bwd.popleft()
            tracer.visit(row, col, "exploring")
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < n and 0 <= new_col < m and 
                    grid[new_row][new_col] == 0):
                    
                    if (new_row, new_col) not in visited_bwd:
                        visited_bwd[(new_row, new_col)] = (row, col)
                        
                        # Check if we've met the forward search
                        if (new_row, new_col) in visited_fwd:
                            path = reconstruct_path((new_row, new_col))
                            for r, c in path:
                                tracer.visit(r, c, "path")
                            return path
                        
                        queue_bwd.append((new_row, new_col))
    
    return None


def solve_bidirectional_astar(grid: List[List[int]], tracer) -> Optional[List[Tuple[int, int]]]:
    """A* from start and end simultaneously, meeting in the middle."""
    if not grid or not grid[0]:
        return None
    
    n = len(grid)
    m = len(grid[0])
    
    if grid[0][0] == 1 or grid[n-1][m-1] == 1:
        return None
    
    def heuristic_from_start(row, col):
        """Manhattan distance to end."""
        return abs(row - (n - 1)) + abs(col - (m - 1))
    
    def heuristic_from_end(row, col):
        """Manhattan distance to start."""
        return abs(row - 0) + abs(col - 0)
    
    # Forward search from start (using heuristic toward end)
    heap_fwd = [(heuristic_from_start(0, 0), 0, 0, 0)]  # (f, g, row, col)
    g_score_fwd = {(0, 0): 0}
    parent_fwd = {(0, 0): None}
    visited_fwd = set()
    
    # Backward search from end (using heuristic toward start)
    heap_bwd = [(heuristic_from_end(n-1, m-1), 0, n-1, m-1)]
    g_score_bwd = {(n-1, m-1): 0}
    parent_bwd = {(n-1, m-1): None}
    visited_bwd = set()
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    best_path_length = float('inf')
    meeting_point = None
    
    def reconstruct_path(meet_point):
        """Reconstruct path from both directions."""
        # Forward path
        path_fwd = []
        curr = meet_point
        while curr is not None:
            path_fwd.append(curr)
            curr = parent_fwd[curr]
        path_fwd = path_fwd[::-1]
        
        # Backward path
        path_bwd = []
        curr = parent_bwd[meet_point]
        while curr is not None:
            path_bwd.append(curr)
            curr = parent_bwd[curr]
        
        return path_fwd + path_bwd
    
    while heap_fwd and heap_bwd:
        # Forward step
        if heap_fwd:
            f, g, row, col = heapq.heappop(heap_fwd)
            
            if (row, col) in visited_fwd:
                continue
                
            # Check termination before processing this node
            if meeting_point is not None and g >= best_path_length:
                break
            
            visited_fwd.add((row, col))
            tracer.visit(row, col, "exploring")
            
            # Check if we've met the backward search
            if (row, col) in visited_bwd:
                path_length = g_score_fwd[(row, col)] + g_score_bwd[(row, col)]
                if path_length < best_path_length:
                    best_path_length = path_length
                    meeting_point = (row, col)
                # Once we meet, check if we should stop
                if heap_bwd and g + heap_bwd[0][1] >= best_path_length:
                    break
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < n and 0 <= new_col < m and 
                    grid[new_row][new_col] == 0):
                    tentative_g = g + 1
                    
                    if tentative_g < g_score_fwd.get((new_row, new_col), float('inf')):
                        g_score_fwd[(new_row, new_col)] = tentative_g
                        parent_fwd[(new_row, new_col)] = (row, col)
                        f_score = tentative_g + heuristic_from_start(new_row, new_col)
                        heapq.heappush(heap_fwd, (f_score, tentative_g, new_row, new_col))
        
        # Backward step
        if heap_bwd:
            f, g, row, col = heapq.heappop(heap_bwd)
            
            if (row, col) in visited_bwd:
                continue
                
            # Check termination before processing this node
            if meeting_point is not None and g >= best_path_length:
                break
            
            visited_bwd.add((row, col))
            tracer.visit(row, col, "exploring")
            
            # Check if we've met the forward search
            if (row, col) in visited_fwd:
                path_length = g_score_fwd[(row, col)] + g_score_bwd[(row, col)]
                if path_length < best_path_length:
                    best_path_length = path_length
                    meeting_point = (row, col)
                # Once we meet, check if we should stop
                if heap_fwd and g + heap_fwd[0][1] >= best_path_length:
                    break
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < n and 0 <= new_col < m and 
                    grid[new_row][new_col] == 0):
                    tentative_g = g + 1
                    
                    if tentative_g < g_score_bwd.get((new_row, new_col), float('inf')):
                        g_score_bwd[(new_row, new_col)] = tentative_g
                        parent_bwd[(new_row, new_col)] = (row, col)
                        f_score = tentative_g + heuristic_from_end(new_row, new_col)
                        heapq.heappush(heap_bwd, (f_score, tentative_g, new_row, new_col))
    
    if meeting_point:
        path = reconstruct_path(meeting_point)
        for r, c in path:
            tracer.visit(r, c, "path")
        return path
    
    return None
