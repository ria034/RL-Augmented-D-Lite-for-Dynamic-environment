# Experiment Plan

## Baseline (do this first, before any RL exists)
Run plain D* Lite (via `planner_core` directly, or `integration` with
`rl_agent=None`) across all environments in `simulation/environments/`.
Record all 5 metrics. This is what RL needs to beat.

## Training
Train on a subset of environment types (decide which — e.g. open_field +
cluttered), holding out at least one entirely (e.g. dynamic_obstacles, or
narrow_corridor) for generalization testing.

## Evaluation
Run RL-guided planner across ALL environments (trained-on and held-out),
same 5 metrics. Compare against baseline:
- Trained-on environments: does RL improve over baseline?
- Held-out environments: does the improvement transfer, or does it
  overfit to training environment types?

## Reporting
Report both trained-on and held-out results separately and honestly — a
result that only holds on trained environments is a real finding, just a
more limited one, and should be reported as such rather than implied to
generalize further than it does.
