"""
Standalone Python simulation runner with live Matplotlib visualization.
"""
import time
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Add root directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from planner_core.grid_map import GridMap
from integration.rl_guided_planner import RLGuidedDStarLite
from rl_policy.agent import RLPlanningAgent

def main():
    print("Initializing Simulation Environment & Visualizer...")
    grid_map = GridMap(width=30, height=30, scenario="warehouse")
    start, goal = (1, 1), (28, 28)
    
    planner = RLGuidedDStarLite(grid_map, start, goal, rl_agent=None)
    
    print("Computing Initial Shortest Path...")
    planner.compute_shortest_path()
    path = planner.get_path()
    
    # Setup Matplotlib Interactive Plot
    fig, ax = plt.subplots(figsize=(7, 7))
    
    for step in range(100):
        # 1. Step environment dynamics (moving obstacles shift)
        grid_map.step_dynamics()
        
        # 2. Re-compute path incrementally via D* Lite
        planner.compute_shortest_path()
        path = planner.get_path()
        
        # 3. Advance agent along path if valid
        if len(path) > 1:
            planner.s_start = path[1]
            
        # --- Rendering Frame ---
        ax.clear()
        costmap = grid_map.get_costmap()
        
        # Display costmap grid (0: free, 100: obstacles)
        ax.imshow(costmap, origin='lower', cmap='binary', alpha=0.8)
        
        # Draw path if available
        if path:
            px, py = zip(*path)
            ax.plot(px, py, color='tab:blue', linewidth=3, marker='o', markersize=3, label='Planned Path')
            
        # Draw Start, Goal, and Current Agent Position
        ax.plot(start[0], start[1], 'go', markersize=10, label='Start')
        ax.plot(goal[0], goal[1], 'ro', markersize=10, label='Goal')
        ax.plot(planner.s_start[0], planner.s_start[1], 'mo', markersize=10, label='Agent')
        
        ax.set_xlim(-0.5, grid_map.width - 0.5)
        ax.set_ylim(-0.5, grid_map.height - 0.5)
        ax.set_title(f"RL-Guided D* Lite Simulation (Step {step+1})")
        ax.legend(loc='upper right')
        
        plt.draw()
        plt.pause(0.1)  # Refresh frame delay
        
        if planner.s_start == goal:
            print("Goal reached successfully!")
            break
            
    print("Simulation finished. Close plot window to exit.")
    plt.show()

if __name__ == "__main__":
    main()