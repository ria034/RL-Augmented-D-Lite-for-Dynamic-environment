"""
Combines planner_core.DStarLite with rl_policy's trained agent.

This is the layer that actually implements "RL-integrated D* Lite" -- kept
separate from both planner_core (which stays RL-agnostic/testable) and
rl_policy (which stays planner-agnostic/trainable on its own), so either
side can be changed independently.

TODO:
- Load a trained RL policy (from rl_policy/agent.py)
- On each planning step: get observation from current planner state,
  get action from policy, apply it to the D* Lite instance (however that
  was defined in rl_policy/env.py's action space), then call
  compute_shortest_path()
- This is also the natural place to fall back to plain D* Lite (no RL
  influence) for baseline comparisons in evaluation/
"""

from planner_core.d_star_lite import DStarLite


class RLGuidedDStarLite:
    def __init__(self, grid_map, start, goal, rl_agent=None):
        """
        rl_agent=None should produce behavior identical to plain D* Lite --
        this makes A/B comparison in evaluation/ straightforward.
        """
        raise NotImplementedError

    def compute_shortest_path(self):
        raise NotImplementedError
