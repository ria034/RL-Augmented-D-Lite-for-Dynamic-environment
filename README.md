# RL-Augmented D* Lite Motion Planner

Improving mobile robot motion planning by integrating reinforcement learning
with D* Lite, evaluated in RViz across multiple environments.

## Status
Design stage — codebase scaffolded, implementation not yet started.

## Goal
D* Lite is a fast incremental replanning algorithm, but its planning
decisions (edge costs, when to replan, how to weigh competing paths) are
fixed/hand-tuned. This project adds an RL layer on top to learn better
planning decisions, evaluated against plain D* Lite as a baseline.

## Evaluation factors (what "better" means here)
1. **Path optimality** — how close to the shortest feasible path
2. **Time taken** — planning time + execution time
3. **Cross-environment generalization** — performance when placed in
   environments not seen during training
4. **Path stability** — how much the planned path changes between
   consecutive replans when the environment changes only slightly
   (avoiding oscillation/thrashing)
5. **Reorientation** — how much heading change the path demands (a
   kinematic cost, not just a geometric one)

## Architecture

```
planner_core/   <- pure D* Lite, no ROS/RL dependencies (fast, unit-testable)
rl_policy/      <- RL agent, trained independently in a lightweight sim first
integration/    <- where RL actually modifies D* Lite's planning decisions
ros2_ws/        <- ROS2 package: real/simulated robot deployment + RViz
simulation/     <- test environments + RViz configs + experiment runner
evaluation/     <- metrics computation (maps to the 5 factors above) + plots
tests/          <- unit tests for planner_core and rl_policy in isolation
docs/           <- architecture notes, experiment plan
```

## Suggested build order
1. `planner_core/` — get plain D* Lite working and tested on its own first;
   this is also your baseline for every comparison later.
2. `evaluation/metrics.py` — implement the 5 metrics against plain D* Lite
   before any RL exists, so you have a baseline to improve on.
3. `rl_policy/` — design and train the RL component against a lightweight
   simulated environment (not RViz yet — training needs many fast episodes).
4. `integration/` — combine RL policy + D* Lite.
5. `ros2_ws/` + `simulation/` — only once the above works, wire into
   ROS2/RViz for the full ones you'll actually demo/evaluate in.
