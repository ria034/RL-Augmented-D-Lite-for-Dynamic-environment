"""
Training entry point.

Instantiates vectorized DStarLiteEnv instances for sample efficiency, 
trains the PPO agent, logs metrics, and saves checkpoints to a results directory.
"""
import os
import sys
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.callbacks import CheckpointCallback

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from simulation.env import DStarLiteEnv

def main():
    # Setup results and logs directory
    results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../results'))
    tensorboard_dir = os.path.join(results_dir, "tensorboard_logs/")
    checkpoint_dir = os.path.join(results_dir, "checkpoints/")
    
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(checkpoint_dir, exist_ok=True)

    print("Initializing Vectorized Environments...")
    # Instantiate vectorized DStarLiteEnv across multiple parallel instances for sample efficiency
    num_envs = 4
    vec_env = make_vec_env(DStarLiteEnv, n_envs=num_envs)

    print("Initializing PPO Agent...")
    # Use 'MultiInputPolicy' because DStarLiteEnv uses a Gymnasium Dict observation space 
    # (containing both the local costmap patch and the relative goal vector).
    model = PPO(
        policy="MultiInputPolicy",
        env=vec_env,
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        n_epochs=10,
        gamma=0.99,
        verbose=1,
        tensorboard_log=tensorboard_dir
    )

    # Setup Checkpoint Callback to save model weights periodically
    checkpoint_callback = CheckpointCallback(
        save_freq=max(10000 // num_envs, 1),
        save_path=checkpoint_dir,
        name_prefix="ppo_dstarlite_agent"
    )

    print("Starting Training Loop...")
    # Train the agent
    total_timesteps = 100000
    model.learn(
        total_timesteps=total_timesteps, 
        callback=checkpoint_callback,
        progress_bar=True
    )

    # Save final model checkpoint
    final_model_path = os.path.join(results_dir, "ppo_dstarlite_final.zip")
    model.save(final_model_path)
    print(f"Training finished successfully! Final model saved to {final_model_path}")

if __name__ == "__main__":
    main()