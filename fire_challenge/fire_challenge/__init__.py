"""
Fire Challenge Module - Simple imports for player convenience
"""

from .fire_challenge import (
    get_map,
    get_available_maps,
    get_custom_map,
    get_custom_map_from_string,
    place_walls,
    test_result,
    highlight_cells,
    highlight_clear,
    visualize_result,
)

__all__ = [
    'get_map',
    'get_available_maps',
    'get_custom_map',
    'get_custom_map_from_string',
    'place_walls',
    'test_result',
    'highlight_cells',
    'highlight_clear',
    'visualize_result',
]
