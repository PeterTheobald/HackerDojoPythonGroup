#!/bin/bash

# Get the Python path
PYTHON_PATH=$(cd ~ && uv run which python)

# Extract the base path
BASE_PATH=$(dirname "$(dirname "$PYTHON_PATH")")

# Construct the TCL_LIBRARY path
TCL_LIBRARY="$BASE_PATH/lib/tcl8.6"

# Set the environment variable
export TCL_LIBRARY

# Print the set variable (for verification)
echo "TCL_LIBRARY has been set to: $TCL_LIBRARY"
