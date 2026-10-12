"""
Reward function design.

This is the single most important design decision in the project -- it
determines what "better planning" actually means to the learned policy.
It should be built from the same 5 factors used for evaluation, so training
directly optimizes what you'll measure:

TODO: design a reward combining
- path optimality      (e.g. -1 * path_length, or ratio vs. a*/d*lite optimal)
- time taken            (e.g. -1 * planning_time, or step penalty)
- path stability        (penalize large path changes between replans)
- reorientation         (penalize cumulative heading change)
- (cross-environment generalization isn't a per-step reward -- it's
   measured by training on a subset of environment types and evaluating
   generalization on held-out ones, in evaluation/)

Decide relative weights deliberately and document the reasoning here once
chosen -- these tradeoffs (e.g. optimality vs. stability) are often in
tension with each other.
"""


def compute_reward(path_before, path_after, planning_time, **kwargs):
    raise NotImplementedError
