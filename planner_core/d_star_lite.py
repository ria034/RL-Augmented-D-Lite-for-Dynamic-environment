"""
Core D* Lite implementation.

Deliberately has NO ROS or RL dependencies -- this module should be testable
and runnable with just a grid/graph in memory, so it can be:
  (a) unit tested in isolation,
  (b) called many thousands of times cheaply during RL training,
  (c) wrapped by integration/ once RL is ready to influence its decisions.

TODO:
- Implement the standard D* Lite algorithm (Koenig & Likhachev, 2002):
  incremental search with g/rhs values, priority queue keyed by calculated
  keys, UpdateVertex / ComputeShortestPath / replanning on edge-cost change.
- Expose hooks for the integration layer to influence (not replace) the
  planner's decisions -- e.g. a pluggable edge-cost function, or a callback
  invoked before each replan -- rather than hardcoding RL into this file.
  Keeping this module RL-agnostic is what makes it independently testable.
"""


class DStarLite:
    def __init__(self, grid_map, start, goal):
        """
        grid_map: planner_core.grid_map.GridMap (or compatible interface)
        start, goal: (x, y) grid coordinates
        """
        raise NotImplementedError

    def compute_shortest_path(self):
        """Run (or re-run, incrementally) the D* Lite search."""
        raise NotImplementedError

    def update_edge_cost(self, u, v, new_cost):
        """Called when the environment changes (new/cleared obstacle, etc.)."""
        raise NotImplementedError

    def get_path(self):
        """Return the current best path from start to goal."""
        raise NotImplementedError
