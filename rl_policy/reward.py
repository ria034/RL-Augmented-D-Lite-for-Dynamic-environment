"""
Reward function design for RL-augmented D* Lite planning.

Tradeoff Documentation:
- Optimality vs. Stability: A purely optimal planner creates unstable, 
  twitchy trajectories when obstacles shift slightly. Conversely, maximizing 
  stability by never changing the path leads to collisions. The weights 
  below balance this tension so the agent learns to deviate *only* when necessary.
- Smoothness (Reorientation): Penalizes zigzagging or abrupt heading changes 
  to ensure kinematic feasibility for physical mobile robots.
"""
import numpy as np

def compute_reward(path_before, path_after, planning_time, success=False, collision=False, **kwargs):
    """
    Computes the step reward based on path optimality, computation time, 
    path stability (disruption between replans), and reorientation/smoothness.
    
    Parameters:
    - path_before: List of (x, y) tuples representing the planned path *before* dynamic update
    - path_after: List of (x, y) tuples representing the newly computed path
    - planning_time: Float representing how long the D* Lite replan took (seconds)
    - success: Boolean indicating if the agent reached the goal
    - collision: Boolean indicating if a collision occurred
    
    Returns:
    - total_reward: Float scalar reward value
    """
    # --- Terminal Sparse Rewards ---
    if collision:
        return -100.0
    if success:
        return 150.0

    # --- Configurable Weights (The Tradeoff Tuning knobs) ---
    w_optimality = 1.0     # Penalizes longer path lengths
    w_time = 5.0           # Penalizes slow replanning computation
    w_stability = 2.5      # Penalizes large deviations from the previous plan (Disruption penalty)
    w_smoothness = 0.5     # Penalizes sharp heading changes / reorientation

    # 1. Path Optimality Factor: Penalize path length
    # (Shorter paths yield less negative/higher values)
    path_length = len(path_after) if path_after else 0
    r_optimality = -1.0 * path_length

    # 2. Time Taken Factor: Penalize computational overhead
    r_time = -1.0 * planning_time

    # 3. Path Stability Factor (Disruption Penalty): 
    # Measure maximum or mean spatial deviation between path_before and path_after
    r_stability = 0.0
    if path_before and path_after:
        # Compute mean distance shift between corresponding waypoints or nearest points
        deviations = []
        for pt_new in path_after:
            min_dist = min([np.hypot(pt_new[0] - pt_old[0], pt_new[1] - pt_old[1]) for pt_old in path_before])
            deviations.append(min_dist)
        mean_deviation = np.mean(deviations)
        r_stability = -1.0 * mean_deviation

    # 4. Reorientation / Smoothness Factor: Penalize cumulative heading changes
    r_smoothness = 0.0
    if len(path_after) >= 3:
        angles = []
        for i in range(len(path_after) - 2):
            p1, p2, p3 = path_after[i], path_after[i+1], path_after[i+2]
            v1 = np.array([p2[0] - p1[0], p2[1] - p1[1]])
            v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
            
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)
            if norm_v1 > 0 and norm_v2 > 0:
                cos_theta = np.dot(v1, v2) / (norm_v1 * norm_v2)
                cos_theta = np.clip(cos_theta, -1.0, 1.0)
                angle = np.arccos(cos_theta)
                angles.append(angle)
        
        if angles:
            total_heading_change = np.sum(angles)
            r_smoothness = -1.0 * total_heading_change

    # --- Combine into Total Reward ---
    total_reward = (
        (w_optimality * r_optimality) +
        (w_time * r_time) +
        (w_stability * r_stability) +
        (w_smoothness * r_smoothness) - 
        0.1  # Small standard step penalty to encourage speed
    )

    return float(total_reward)