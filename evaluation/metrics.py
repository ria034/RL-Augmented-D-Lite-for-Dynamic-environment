"""
Metrics computation. Each function here maps to one of the 5 evaluation
factors from the project plan -- implement plain-D*-Lite versions of these
FIRST (before any RL exists) so there's an honest baseline to compare
against later.
"""


def path_optimality(path, optimal_path_length):
    """
    Factor 1: Path optimality.
    e.g. ratio of actual path length to the shortest feasible path length
    (computed via a full-search baseline like A* on the static map, for
    environments without dynamic obstacles).
    """
    raise NotImplementedError


def time_taken(planning_times, execution_time):
    """
    Factor 2: Time taken.
    Separate planning time (compute) from execution time (how long the
    robot takes to traverse the path) -- these can trade off against each
    other and should be reported separately, not combined into one number.
    """
    raise NotImplementedError


def cross_environment_generalization(results_by_environment, trained_on):
    """
    Factor 3: Performance across different environments.
    Compare metrics on environments the policy was trained on vs. held-out
    ones -- the gap between these IS the generalization measurement, not a
    single absolute number.
    """
    raise NotImplementedError


def path_stability(path_history):
    """
    Factor 4: Path stability.
    path_history: the sequence of full paths produced at each replan event
    (see simulation/run_experiment.py -- this needs the history, not just
    the final path). Quantify how much consecutive paths differ -- e.g.
    edit distance between waypoint sequences, or area between the two
    paths -- to catch oscillation/thrashing.
    """
    raise NotImplementedError


def reorientation(path):
    """
    Factor 5: Reorientation.
    Sum of absolute heading changes along the path -- a kinematic cost
    distinct from path length (a geometrically short path can still demand
    a lot of turning).
    """
    raise NotImplementedError
