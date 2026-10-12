# ros2_ws

ROS2 package for deploying the planner on a real or simulated robot, with
RViz visualization. This is the LAST piece to build — everything in
`planner_core/`, `rl_policy/`, and `integration/` should work and be tested
independently first; ROS2 adds deployment overhead you don't want while
still iterating on the core algorithm or RL training.

## Status
Package skeleton only (`package.xml`, `setup.py`, empty launch file, a node
stub). Not functional yet.
