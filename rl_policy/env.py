"""
Gym-style environment wrapping the D* Lite planning task, for training the
RL policy cheaply before it ever touches ROS2/RViz.

TODO:
- Define the action space: what does the RL policy actually control?
  (e.g. edge-cost adjustments, a replan/don't-replan decision, a
  heuristic-weighting parameter -- decide this before implementing, it
  determines the whole integration/ design)
- Define the observation space: local costmap patch? distance-to-goal?
  recent path history (for the stability metric)?
- Define step(): apply action -> call into planner_core -> compute reward
- Load environment variants from simulation/environments/*.yaml so training
  can sample across the same environment types used for evaluation later
"""

import gymnasium as gym


class DStarLiteEnv(gym.Env):
    def __init__(self, environment_config_path):
        raise NotImplementedError

    def reset(self, seed=None, options=None):
        raise NotImplementedError

    def step(self, action):
        raise NotImplementedError
