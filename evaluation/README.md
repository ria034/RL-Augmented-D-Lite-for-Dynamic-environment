# evaluation

Metrics and analysis. `metrics.py`'s five functions map 1:1 onto the
project's five evaluation factors (path optimality, time taken,
cross-environment generalization, path stability, reorientation).

## Important: build this before the RL works
Implement these against **plain D* Lite first**, before any RL component
exists. That gives you an honest, uncontaminated baseline -- if you build
the metrics after RL already "looks good," it's easy to unconsciously shape
the metrics to flatter the result you already have.

## Status
Not yet implemented (stubs only).
