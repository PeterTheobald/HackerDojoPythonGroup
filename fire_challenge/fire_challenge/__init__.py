"""
Fire Challenge Module - Simple imports for player convenience
"""

from .fire_challenge import (
    # New class-based API (recommended)
    FireChallenge,
    # Legacy function API (deprecated)
    get_map,
    get_custom_map,
    get_custom_map_from_string,
    place_walls,
    test_result,
    highlight_cells,
    highlight_clear,
    visualize_result,
)

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
