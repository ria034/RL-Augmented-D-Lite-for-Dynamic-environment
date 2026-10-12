"""
ROS2 node wrapping integration.RLGuidedDStarLite for real/simulated robot
deployment.

TODO:
- Subscribe: /map or /local_costmap (nav_msgs/OccupancyGrid), /odom
- Convert OccupancyGrid -> planner_core.GridMap here (keep this conversion
  in ros2_ws/, not in planner_core/, so the core stays ROS-free)
- Publish: /planned_path (nav_msgs/Path), markers for RViz visualization
- Trigger replanning on costmap updates (this is where D* Lite's
  incremental-replanning advantage actually gets exercised against a
  changing environment)
"""

import rclpy
from rclpy.node import Node


class PlannerNode(Node):
    def __init__(self):
        super().__init__("rl_dstar_planner_node")
        raise NotImplementedError


def main(args=None):
    rclpy.init(args=args)
    node = PlannerNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
