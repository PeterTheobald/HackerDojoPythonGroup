# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.2.0] - 2026-02-06
### Added
- Build and publish usign uv documentation added to README
- CHANGELOG.md for tracking version history
- Examples organized in `examples/` folder for better project structure

### Changed
- Reorganized project structure: moved example files to `examples/` directory
- Updated source distribution to include `examples/` folder

## [2.1.0] - 2025-02-06
### Added
- MIT License allowing free usage with attribution
- Command line map selection option for map_traversal_benchmark.py
- `print_map()` method with dual formats (int grid and string with borders)
- `get_map_string()` method for formatted map display

### Changed
- Visual distinction in fire visualization: initial fire (darkred) vs spreading fire (orange)
- Fire spread tracking now uses value 4 for initial fire cells
- Custom map format now uses '*' for fire instead of 'f'
- Example files now dynamically find open cells and respect max_walls

### Fixed
- Legacy compatibility: re-added `get_available_maps()` module function for backward compatibility

## [2.0.1] - 2025-02-05
### Fixed
- Backward compatibility issue where legacy client players calling `get_available_maps()` directly would fail
- Added module-level wrapper function for `get_available_maps()`

## [2.0.0] - 2025-02-05
### Added
- Class-based `FireChallenge` API with instance methods
- Static method `FireChallenge.get_available_maps()`
- Class methods: `from_custom_grid()` and `from_string()`
- Simple `example_player.py` (~90 lines) for beginners
- Comprehensive `feature_demonstrations.py` showcasing all features
- `beginner_tutorial.py` for step-by-step learning
- `browse_maps.py` for interactive map exploration

### Changed
- Major architectural refactoring from global state to class-based design
- Modernized type annotations to Python 3.10+ syntax (list[], dict[], X | None)
- Updated Python requirement to 3.10+
- Improved `place_walls()` validation order (validate before modifying state)
- Enhanced documentation with class-based API examples

### Removed
- Personal player solution files (Sam_Player.py, Sam_Universal.py, petes_player.py)
- Test files from package distribution
- Unused dependencies: networkx, ortools
- Legacy global-state API from documentation (kept as deprecated wrapper functions)

## [1.0.0] - 2025-01-29
### Added
- Initial release of fire-challenge package
- 14 pre-built challenge maps
- Fire spread simulation engine
- Visualization with matplotlib
- Custom map creation support
- Basic example player code
