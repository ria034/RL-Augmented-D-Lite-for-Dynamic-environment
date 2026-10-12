# Architecture Decisions

Open decisions to make before/while implementing — fill these in as you
decide, so the reasoning is recorded alongside the code.

## 1. What does the RL policy actually control?
Options: edge-cost adjustments, replan/don't-replan decision, heuristic
weighting. This determines `rl_policy/env.py`'s action space and all of
`integration/`.

**Decision:** _TBD_

## 2. What representation does the grid/cost map use?
Dense array vs. sparse graph. Affects `planner_core/grid_map.py` and how
`ros2_ws/` converts from `nav_msgs/OccupancyGrid`.

**Decision:** _TBD_

## 3. Reward function weighting
How are the 5 factors (optimality, time, stability, reorientation,
generalization-via-held-out-envs) weighted against each other in
`rl_policy/reward.py`? These trade off against each other.

**Decision:** _TBD_

## 4. RL algorithm choice
PPO / SAC / DQN / other, in `rl_policy/agent.py`.

**Decision:** _TBD_
