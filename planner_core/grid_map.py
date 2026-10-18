"""
Grid/cost-map representation supporting both Warehouse and Pedestrian scenarios.
"""
import numpy as np

class GridMap:
    def __init__(self, width=30, height=30, scenario="warehouse"):
        self.width = width
        self.height = height
        self.scenario = scenario.lower()
        
        # Grid array: 0 for free space, 100 for occupied/obstacles
        self.grid = np.zeros((height, width), dtype=np.int8)
        self.static_obstacles = set()
        self.dynamic_obstacles = []
        
        # Load the requested layout
        if self.scenario == "warehouse":
            self._init_warehouse_layout()
        elif self.scenario == "pedestrian":
            self._init_pedestrian_layout()
        else:
            raise ValueError(f"Unknown scenario '{scenario}'. Choose 'warehouse' or 'pedestrian'.")

    def _init_warehouse_layout(self):
        """Initializes structured storage racks and aisles (Warehouse scenario)."""
        shelf_blocks = [
            (2, 2, 6, 3),  (11, 2, 6, 3),  (20, 2, 6, 3),
            (2, 8, 6, 3),  (11, 8, 6, 3),  (20, 8, 6, 3),
            (2, 14, 6, 3), (11, 14, 6, 3), (20, 14, 6, 3),
            (2, 20, 6, 3), (11, 20, 6, 3), (20, 20, 6, 3),
        ]
        
        for bx, by, bw, bh in shelf_blocks:
            for x in range(bx, bx + bw):
                for y in range(by, by + bh):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.static_obstacles.add((x, y))
                        
        # Patrolling dynamic agents
        self.dynamic_obstacles = [
            {"pos": [5, 6], "direction": 1, "axis": "x", "min": 2, "max": 14},
            {"pos": [22, 12], "direction": -1, "axis": "y", "min": 5, "max": 25}
        ]

    def _init_pedestrian_layout(self):
        """Initializes irregular walls and cluttered corridors (Pedestrian scenario)."""
        wall_blocks = [
            (1, 1, 4, 2),   (7, 1, 3, 2),   (12, 1, 10, 2),  (24, 1, 5, 2),
            (1, 7, 6, 3),   (10, 7, 12, 3), (24, 7, 5, 3),
            (10, 13, 3, 2), (15, 13, 10, 2),
            (1, 18, 5, 3),  (12, 18, 4, 3), (18, 18, 10, 3)
        ]
        
        for bx, by, bw, bh in wall_blocks:
            for x in range(bx, bx + bw):
                for y in range(by, by + bh):
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.static_obstacles.add((x, y))
                        
        # Moving pedestrians crossing corridors
        self.dynamic_obstacles = [
            {"pos": [3, 4], "direction": 1, "axis": "y", "min": 3, "max": 6},
            {"pos": [15, 11], "direction": 1, "axis": "x", "min": 12, "max": 22},
            {"pos": [20, 16], "direction": -1, "axis": "y", "min": 14, "max": 22}
        ]

    def step_dynamics(self):
        """Updates the positions of dynamic obstacles."""
        for obs in self.dynamic_obstacles:
            axis_idx = 0 if obs["axis"] == "x" else 1
            obs["pos"][axis_idx] += obs["direction"]
            
            if obs["pos"][axis_idx] >= obs["max"] or obs["pos"][axis_idx] <= obs["min"]:
                obs["direction"] *= -1

    def get_costmap(self):
        """Returns the combined 2D NumPy occupancy grid (0 = free, 100 = blocked)."""
        self.grid.fill(0)
        
        for (ox, oy) in self.static_obstacles:
            if 0 <= ox < self.width and 0 <= oy < self.height:
                self.grid[oy, ox] = 100
                
        for obs in self.dynamic_obstacles:
            dx, dy = obs["pos"]
            if 0 <= dx < self.width and 0 <= dy < self.height:
                self.grid[dy, dx] = 100
                
        return self.grid

    def is_free(self, pos):
        """Checks if a coordinate is within bounds and free."""
        x, y = pos
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return self.get_costmap()[y, x] == 0