#! /usr/bin/env python

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import NamedTuple

import numpy as np
import typer
from fire_challenge.challenge_maps import CHALLENGE_MAPS
from fire_challenge.fire_challenge import get_map
from networkx import Graph
from numpy.typing import NDArray


class CellType(Enum):
    OPEN = 0
    WATER = 1
    FIRE = 2
    WALL = 3

    def is_fireproof(self) -> bool:
        return self in (CellType.WATER, CellType.WALL)


def get_map_grid(map_num: int = 0) -> NDArray[np.int64]:
    return CHALLENGE_MAPS[map_num]["grid"]


log = logging.getLogger(__name__)


def _add_undirected_edge(g: Graph, a: tuple[int, int], b: tuple[int, int]) -> None:
    g.add_edge(a, b)
    g.add_edge(b, a)


class Coord(NamedTuple):
    x: int
    y: int


SOURCE = Coord(-2, -2)  # connected to the problem's one or more starting flames
SINK = Coord(-1, -1)  # connected to the zero or more proposed wall locations


def get_map_graph(grid: np.ndarray) -> Graph:
    rows, cols = grid.shape

    g = Graph()
    g.add_node(SOURCE, value=CellType.FIRE)

    for x in range(cols):
        for y in range(rows):
            g.add_node(Coord(x, y), value=CellType(grid[x, y]))

    nbr_offsets = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]
    for coord in g.nodes:
        node = g.nodes[coord]
        if node["value"].is_fireproof():
            continue
        for dx, dy in nbr_offsets:
            nx, ny = coord.x + dx, coord.y + dy
            if nx in range(cols) and ny in range(rows):
                nbr = g.nodes[Coord(nx, ny)]
                if nbr["value"].is_fireproof():
                    continue
                _add_undirected_edge(g, coord, Coord(nx, ny))
                if nbr["value"] is CellType.FIRE:
                    _add_undirected_edge(g, coord, SOURCE)
                    log.info("node %r, nbr %r", node, nbr)

    return g


@dataclass
class Solution:
    """A candidate FireChallenge solution.
    It may be a partial solution, proposing fewer than max_walls."""

    sink = SINK
    num_saved: int = 0


@dataclass
class Problem:
    """An instance of a FireChallenge problem."""

    graph: Graph
    max_walls: int
    map_name: str
    source = SOURCE
    solutions: list[Solution] = field(default_factory=list)


def solve_fire_challenge(map_num: int = 0, visualize: bool = False) -> Problem:

    grid, max_walls, map_name = get_map(map=map_num)

    return Problem(get_map_graph(grid), max_walls, map_name)


if __name__ == "__main__":
    typer.run(solve_fire_challenge)
