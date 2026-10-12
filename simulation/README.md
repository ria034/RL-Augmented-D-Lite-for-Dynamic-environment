# simulation

Test environments and the experiment runner.

## environments/
One config per environment "type". Current placeholders:
- `env_open_field.yaml` — baseline, few obstacles
- `env_cluttered.yaml` — dense obstacles, tests optimality under constraint
- `env_narrow_corridor.yaml` — tests reorientation + stability
- `env_dynamic_obstacles.yaml` — tests stability under changing environment
  (the main case for showing D* Lite's incremental-replanning advantage)

Train the RL policy on a subset of these, hold out at least one for
measuring cross-environment generalization honestly.

## rviz_configs/
RViz configuration files for visualizing the planner's behavior on a real
or simulated robot. Not needed for RL training itself (that happens in a
lighter-weight sim via `rl_policy/env.py`) — this is for the later
ROS2/RViz demonstration and evaluation stage.

## run_experiment.py
Runs a planner across environments and logs raw results for
`evaluation/metrics.py` to process.

## Status
Environment configs are placeholders (no actual obstacle layouts yet).
`run_experiment.py` not yet implemented.
