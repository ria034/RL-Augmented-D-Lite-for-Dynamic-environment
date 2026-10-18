"""
RL policy/agent wrapper using Stable-Baselines3.

Wraps standard RL algorithms (like PPO) to fit into your planning stack, 
keeping observation and action space handling clean and modular.
"""
import os
from stable_baselines3 import PPO

class RLPlanningAgent:
    def __init__(self, observation_space, action_space, policy="MlpPolicy"):
        """
        observation_space: Gym observation space
        action_space: Gym action space
        policy: SB3 policy architecture string (default 'MlpPolicy')
        """
        self.observation_space = observation_space
        self.action_space = action_space
        
        # Initialize Stable-Baselines3 PPO model with an MLP policy
        self.model = PPO(
            policy=policy,
            env=None,  # Env can be bound later during training loops
            verbose=0
        )

    def act(self, observation):
        """
        Given an observation from the grid environment, predict the action.
        Returns the action vector/scalar.
        """
        action, _states = self.model.predict(observation, deterministic=True)
        return action

    def save(self, path):
        """Saves the trained RL model checkpoint to disk."""
        self.model.save(path)

    def load(self, path):
        """Loads a pre-trained RL model checkpoint from disk."""
        if not path.endswith(".zip"):
            path += ".zip"
            
        if os.path.exists(path):
            self.model = PPO.load(path)
        else:
            raise FileNotFoundError(f"Model file not found at {path}")