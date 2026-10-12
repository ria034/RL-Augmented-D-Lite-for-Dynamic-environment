# planner_core

Pure D* Lite implementation. No ROS, no RL, no external simulation
dependencies -- just the algorithm operating on a grid/graph in memory.

This is intentional: `rl_policy/` needs to call this thousands of times
during training, which only works if it's fast and has no ROS overhead; and
keeping it dependency-free means it can be properly unit tested on its own
before anything else in the project depends on it.

## Files
- `grid_map.py` — grid/cost-map representation
- `d_star_lite.py` — the D* Lite algorithm itself

## Status
Not yet implemented (stubs only).
