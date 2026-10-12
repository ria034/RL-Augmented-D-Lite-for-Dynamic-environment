"""
Runs a planner (plain D* Lite, or RL-guided via integration/) across the
environment configs in environments/, logging whatever evaluation/metrics.py
needs.

TODO:
- Load an environment config
- Run the planner start-to-goal, recording the path at each replan event
  (not just the final path -- path stability needs the history)
- Save raw results (paths, timings) for evaluation/ to consume -- keep
  this script "dumb" (just runs + logs), put actual metric computation in
  evaluation/metrics.py so the two stay decoupled
"""

if __name__ == "__main__":
    raise NotImplementedError
