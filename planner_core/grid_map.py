"""
Grid/cost-map representation used by D* Lite.

TODO:
- Decide representation: dense 2D array (simple, fine for small maps) vs.
  sparse/graph representation (scales better for large or mostly-open maps).
- Support loading from: a static array (for unit tests / training envs) and
  a ROS2 OccupancyGrid message (for real deployment) -- keep the conversion
  from OccupancyGrid in ros2_ws/, not here, so this module stays ROS-free.
- Expose whatever neighbor/cost-lookup interface d_star_lite.py needs.
"""


class GridMap:
    def __init__(self, width, height):
        raise NotImplementedError

    def is_occupied(self, cell):
        raise NotImplementedError

    def set_occupied(self, cell, occupied=True):
        """For simulating dynamic obstacles appearing/clearing."""
        raise NotImplementedError

    def neighbors(self, cell):
        raise NotImplementedError

    def cost(self, cell_a, cell_b):
        raise NotImplementedError
