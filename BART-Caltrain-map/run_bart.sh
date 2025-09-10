#!/bin/bash
source bart_secrets.sh
uv run bokeh serve bart.py --address 0.0.0.0 --port 5006 --allow-websocket-origin=localhost:5006

