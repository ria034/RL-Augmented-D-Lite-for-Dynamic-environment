"""
RL policy/agent.

TODO:
- Pick an algorithm. For this kind of low-dimensional, planning-adjacent
  action space, PPO or SAC (if continuous action, e.g. cost-weighting) or
  DQN (if discrete, e.g. replan/don't-replan) are reasonable starting
  points -- an existing library (e.g. Stable-Baselines3) is a sensible
  starting point rather than writing an RL algorithm from scratch, unless
  there's a specific reason to.
- Decide what the network sees (observation space, from env.py) and
  outputs (action space, from env.py) before writing this.
"""


class RLPlanningAgent:
    def __init__(self, observation_space, action_space):
        raise NotImplementedError

    def act(self, observation):
        raise NotImplementedError

    def save(self, path):
        raise NotImplementedError

    def load(self, path):
        raise NotImplementedError
