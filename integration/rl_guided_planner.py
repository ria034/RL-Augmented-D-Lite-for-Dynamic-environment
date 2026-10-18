"""
Combines planner_core.DStarLite with rl_policy's trained agent.

This layer implements RL-integrated D* Lite while keeping planner_core 
RL-agnostic and rl_policy planner-agnostic.
"""
import numpy as np
from planner_core.d_star_lite import DStarLite


class RLGuidedDStarLite(DStarLite):
    def __init__(self, grid_map, start, goal, rl_agent=None):
        """
        grid_map: GridMap instance
        start, goal: (x, y) coordinates
        rl_agent: RLPlanningAgent instance (or None for plain D* Lite baseline)
        """
        super().__init__(grid_map, start, goal)
        self.rl_agent = rl_agent
        self.current_alpha = 1.0  # Default cost multiplier (no RL effect)

    def _get_observation(self):
        """Extracts local observation matching the training environment's observation space."""
        costmap = self.grid_map.get_costmap()
        x, y = self.s_start
        
        # Extract 5x5 local window around current start state
        patch = np.zeros((5, 5), dtype=np.float32)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_map.width and 0 <= ny < self.grid_map.height:
                    patch[dy + 2, dx + 2] = float(costmap[ny, nx])
                else:
                    patch[dy + 2, dx + 2] = 100.0  # Out of bounds treated as obstacle

        rel_goal = np.array([float(self.goal[0] - x), float(self.goal[1] - y)], dtype=np.float32)

        return {
            "local_patch": patch,
            "relative_goal": rel_goal
        }

    def _cost(self, s_start, s_end):
        """Overrides base cost to incorporate RL-guided cost scaling multiplier (alpha)."""
        base_cost = super()._cost(s_start, s_end)
        if base_cost == float('inf'):
            return float('inf')
        return base_cost * self.current_alpha

    def compute_shortest_path(self):
        """
        On each planning step: 
        1. Get observation from current planner state.
        2. Get action from policy (if rl_agent is provided).
        3. Apply action scaling factor and run D* Lite shortest path computation.
        """
        if self.rl_agent is not None:
            obs = self._get_observation()
            action = self.rl_agent.act(obs)
            
            # Handle action format from Stable-Baselines3 (scalar or array)
            if isinstance(action, np.ndarray):
                self.current_alpha = float(action.flatten()[0])
            else:
                self.current_alpha = float(action)
        else:
            self.current_alpha = 1.0  # Fallback to plain D* Lite baseline

        # Invoke base D* Lite search using the updated RL-influenced cost function
        super().compute_shortest_path()