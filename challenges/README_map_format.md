# Map Format Guide

## Basic Map Format

Maps are defined as multi-line strings where:
- ` ` (space) = open/walkable cell
- `#` = wall/obstacle
- `S` = start position (optional)
- `E` = finish/goal position (optional)

## Default Behavior

If no `S` is specified, the start defaults to the **upper-left** corner (0, 0).
If no `E` is specified, the finish defaults to the **lower-right** corner.

## Example Maps

### Simple map with default start/finish
```python
simple_map = """
    #####
    #   #
    # # #
    #   #
    #####
"""
# Start: (0, 0) - top-left
# Finish: (4, 4) - bottom-right
```

### Map with custom start and finish
```python
custom_map = """
    #####
    #S  #
    # # #
    #  E#
    #####
"""
# Start: (1, 1) - marked with 'S'
# Finish: (3, 3) - marked with 'E'
```

### Map with only custom start
```python
start_only_map = """
S   #####
    #   #
    # # #
    #   #
    #####
"""
# Start: (0, 0) - marked with 'S'
# Finish: (4, 8) - defaults to bottom-right
```

## Notes

- `S` and `E` are treated as open (walkable) cells
- Both start and finish positions must be on open cells (not walls)
- You can use either or both of `S` and `E` markers
- The map is automatically padded to create a rectangular grid
