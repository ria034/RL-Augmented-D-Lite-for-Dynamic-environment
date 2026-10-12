# rl_policy

The RL component, trained independently of ROS2/RViz using a lightweight
simulated environment built on top of `planner_core`. Training needs many
fast episodes -- RViz/Gazebo are too slow for this step.

## Files
- `env.py` — Gym-style environment wrapping the D* Lite planning task
- `reward.py` — reward function (built from the same 5 factors as `evaluation/`)
- `agent.py` — the RL policy itself
- `train.py` — training entry point

## Key open design decision
What does the RL policy actually control? (edge costs? replan timing? a
heuristic weight?) This decision shapes `env.py`'s action space, `agent.py`'s
output layer, and all of `integration/` — decide and document it before
implementing.

## Status
Not yet implemented (stubs only).
