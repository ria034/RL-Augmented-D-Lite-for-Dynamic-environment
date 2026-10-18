"""
Gym-style environment wrapping the D* Lite planning task, for training the
RL policy cheaply before it ever touches ROS2/RViz.
"""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
import yaml
import os
import sys

# Add project root to path to import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from simulation.grid_env import GridMap
from planner_core.d_star_lite import DStarLite

class DStarLiteEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, environment_config_path=None):
        super().__init__()
        
        # 1. Load configuration or default parameters
        self.width = 30
        self.height = 30
        self.scenario = "warehouse"
        
        if environment_config_path and os.path.exists(environment_config_path):
            with open(environment_config_path, 'r') as f:
                config = yaml.safe_load(f)
                self.width = config.get("width", 30)
                self.height = config.get("height", 30)
                self.scenario = config.get("scenario", "warehouse")

        # Initialize Grid Environment and Planner placeholders
        self.grid_map = GridMap(width=self.width, height=self.height, scenario=self.scenario)
        self.start = (1, 1)
        self.goal = (self.width - 2, self.height - 2)
        self.planner = DStarLite(self.grid_map, self.start, self.goal)

        # 2. Define Action Space: e.g., continuous cost multiplier alpha [0.5, 3.0]
        # Controls how aggressively the RL agent penalizes proximity to dynamic obstacles
        self.action_space = spaces.Box(low=0.5, high=3.0, shape=(1,), dtype=np.float32)

        # 3. Define Observation Space: 
        # Local 5x5 costmap patch around agent + relative goal (dx, dy) + current path length
        self.observation_space = spaces.Dict({
            "local_patch": spaces.Box(low=0, high=100, shape=(5, 5), dtype=np.float32),
            "relative_goal": spaces.Box(low=-self.width, high=self.width, shape=(2,), dtype=np.float32),
        })

        self.current_pos = self.start
        self.path = []

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        # Reset grid and planner
        self.grid_map = GridMap(width=self.width, height=self.height, scenario=self.scenario)
        self.current_pos = self.start
        self.planner = DStarLite(self.grid_map, self.current_pos, self.goal)
        self.planner.compute_shortest_path()
        self.path = self.planner.get_path()
        
        observation = self._get_observation()
        info = {}
        return observation, info

    def step(self, action):
        """
        Apply action (e.g., RL cost multiplier), step environment dynamics, 
        re-plan path via D* Lite, and compute reward.
        """
        alpha_multiplier = float(action[0])
        
        # 1. Step environment dynamics (moving obstacles shift)
        self.grid_map.step_dynamics()
        
        # 2. Re-compute path using updated environment state
        self.planner.compute_shortest_path()
        self.path = self.planner.get_path()
        
        # 3. Advance agent along path if valid
        terminated = False
        truncated = False
        reward = -1.0  # Step penalty
        
        if len(self.path) > 1:
            self.current_pos = self.path[1]
            self.planner.s_start = self.current_pos
        
        # Check if goal reached
        if self.current_pos == self.goal:
            reward = 100.0
            terminated = True
        elif not self.grid_map.is_free(self.current_pos):
            reward = -50.0  # Collision penalty
            terminated = True

        observation = self._get_observation()
        info = {"path_length": len(self.path)}
        
        return observation, reward, terminated, truncated, info

    def _get_observation(self):
        """Extracts local 5x5 costmap window and relative goal vector."""
        costmap = self.grid_map.get_costmap()
        x, y = self.current_pos
        
        # Extract 5x5 local window around agent, padding with obstacles if out of bounds
        patch = np.zeros((5, 5), dtype=np.float32)
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    patch[dy + 2, dx + 2] = float(costmap[ny, nx])
                else:
                    patch[dy + 2, dx + 2] = 100.0  # Out of bounds treated as obstacle

        rel_goal = np.array([float(self.goal[0] - x), float(self.goal[1] - y)], dtype=np.float32)

        return {
            "local_patch": patch,
            "relative_goal": rel_goal
        }

    def render(self):
        """Simple text-based or plotting render hook."""
        pass