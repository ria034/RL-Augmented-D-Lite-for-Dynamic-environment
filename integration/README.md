# integration

Where RL actually modifies D* Lite's planning decisions. Deliberately
isolated from `planner_core/` (stays testable/RL-agnostic) and `rl_policy/`
(stays trainable/planner-agnostic on its own).

Includes a no-RL fallback mode so plain D* Lite vs. RL-guided D* Lite can be
directly A/B compared in `evaluation/`.

## Status
Not yet implemented (stub only). Depends on `rl_policy`'s action-space
design being finalized first.
