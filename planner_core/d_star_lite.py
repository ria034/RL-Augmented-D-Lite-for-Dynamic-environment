"""
Core D* Lite implementation.

NO RL implementation here, tested the performance of D_lite in asblation 
"""
import numpy as np
import heapq

class DStarLite:
    def __init__(self, grid_map, start, goal):
        """
        grid_map: planner_core.grid_map.GridMap (or compatible interface)
        start, goal: (x, y) grid coordinates
        """
        self.grid_map = grid_map
        self.start = tuple(start)
        self.goal = tuple(goal)
        
        self.s_start = self.start
        self.s_last = self.start
        self.k_m = 0.0
        
        self.U = []     # Priority queue (min-heap)
        self.g = {}     # Cost-to-goal estimates
        self.rhs = {}   # One-step lookahead cost estimates
        
        # Initialize search structures and seed goal
        self._initialize()

    def _heuristic(self, s1, s2):
        """Euclidean distance heuristic."""
        return np.hypot(s1[0] - s2[0], s1[1] - s2[1])

    def _calculate_key(self, s):
        """Calculates priority key tuple for queue sorting."""
        min_val = min(self.g.get(s, float('inf')), self.rhs.get(s, float('inf')))
        return (min_val + self._heuristic(self.s_start, s) + self.k_m, min_val)

    def _get_neighbors(self, s):
        """Returns valid, collision-free neighbors from the grid map."""
        x, y = s
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
            nx, ny = x + dx, y + dy
            if self.grid_map.is_free((nx, ny)):
                neighbors.append((nx, ny))
        return neighbors

    def _cost(self, s_start, s_end):
        """Traversal cost between two adjacent states."""
        if not self.grid_map.is_free(s_end):
            return float('inf')
        return np.hypot(s_end[0] - s_start[0], s_end[1] - s_start[1])

    def _initialize(self):
        """Clears and seeds the initial goal into priority queue."""
        self.g.clear()
        self.rhs.clear()
        self.U.clear()
        
        self.rhs[self.goal] = 0.0
        self.g[self.goal] = float('inf')
        self.g[self.s_start] = float('inf')
        self.rhs[self.s_start] = float('inf')
        
        heapq.heappush(self.U, (self._calculate_key(self.goal), self.goal))

    def _update_vertex(self, u):
        """Updates rhs value of vertex u and manages its state in the queue."""
        if u != self.goal:
            self.rhs[u] = min(
                [self.g.get(s, float('inf')) + self._cost(u, s) for s in self._get_neighbors(u)],
                default=float('inf')
            )
        
        # Remove u from priority queue if present
        self.U = [item for item in self.U if item[1] != u]
        heapq.heapify(self.U)
        
        # If inconsistent, push back into queue
        if self.g.get(u, float('inf')) != self.rhs.get(u, float('inf')):
            heapq.heappush(self.U, (self._calculate_key(u), u))

    def compute_shortest_path(self):
        """Run (or re-run, incrementally) the D* Lite search."""
        while len(self.U) > 0 and (
            self.U[0][0] < self._calculate_key(self.s_start) or
            self.rhs.get(self.s_start, float('inf')) > self.g.get(self.s_start, float('inf'))
        ):
            k_old, u = heapq.heappop(self.U)
            k_new = self._calculate_key(u)
            
            if k_old < k_new:
                heapq.heappush(self.U, (k_new, u))
            elif self.g.get(u, float('inf')) > self.rhs.get(u, float('inf')):
                self.g[u] = self.rhs[u]
                for s in self._get_neighbors(u):
                    self._update_vertex(s)
            else:
                g_old = self.g.get(u, float('inf'))
                self.g[u] = float('inf')
                for s in list(self._get_neighbors(u)) + [u]:
                    if self.rhs.get(s, float('inf')) == g_old + self._cost(s, u):
                        if s != self.goal:
                            self.rhs[s] = min(
                                [self.g.get(s_prime, float('inf')) + self._cost(s, s_prime) for s_prime in self._get_neighbors(s)],
                                default=float('inf')
                            )
                    self._update_vertex(s)
                self.compute_shortest_path()

    def update_edge_cost(self, u, v, new_cost=None):
        """Called when the environment changes (new/cleared obstacle, etc.)."""
        self._update_vertex(u)
        self._update_vertex(v)
        self.compute_shortest_path()

    def get_path(self):
        """Return the current best path from start to goal."""
        path = [self.s_start]
        curr = self.s_start
        while curr != self.goal:
            neighbors = self._get_neighbors(curr)
            if not neighbors:
                break
            curr = min(
                neighbors,
                key=lambda s: self.g.get(s, float('inf')) + self._cost(curr, s)
            )
            path.append(curr)
            if len(path) > self.grid_map.width * self.grid_map.height:
                break
        return path