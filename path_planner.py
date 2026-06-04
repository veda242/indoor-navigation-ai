"""
Path Planner Module
Calculates safe navigation paths avoiding obstacles
"""

import numpy as np
from collections import deque
import heapq

class PathPlanner:
    """Plans safe paths through detected obstacles"""
    
    def __init__(self, frame_width=640, frame_height=480, grid_cell_size=20):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.grid_cell_size = grid_cell_size
        self.grid_width = frame_width // grid_cell_size
        self.grid_height = frame_height // grid_cell_size
    
    def find_safe_corridor(self, obstacle_grid, current_x, current_y, target_x=None):
        """Find the safest corridor to move forward"""
        # Create a navigability map (inverse of obstacle density)
        navigability = 1.0 / (obstacle_grid + 0.1)
        
        grid_x = max(0, min(self.grid_width - 1, current_x // self.grid_cell_size))
        grid_y = max(0, min(self.grid_height - 1, current_y // self.grid_cell_size))
        
        # Divide the grid into three zones (left, center, right)
        left_zone = navigability[:, :self.grid_width // 3]
        center_zone = navigability[:, self.grid_width // 3:2 * self.grid_width // 3]
        right_zone = navigability[:, 2 * self.grid_width // 3:]
        
        # Calculate clearance scores for each zone
        left_score = np.mean(left_zone)
        center_score = np.mean(center_zone)
        right_score = np.mean(right_zone)
        
        zones = {
            'left': left_score,
            'center': center_score,
            'right': right_score
        }
        
        # Also check proximity scores (immediate danger)
        immediate_left = self.get_immediate_threat(obstacle_grid, 'left')
        immediate_center = self.get_immediate_threat(obstacle_grid, 'center')
        immediate_right = self.get_immediate_threat(obstacle_grid, 'right')
        
        # Penalize zones with immediate threats
        if immediate_left < 0.3:
            zones['left'] *= 0.5
        if immediate_center < 0.3:
            zones['center'] *= 0.5
        if immediate_right < 0.3:
            zones['right'] *= 0.5
        
        # Find the safest zone
        safest_zone = max(zones, key=zones.get)
        confidence = zones[safest_zone]
        
        return safest_zone, zones, confidence
    
    def get_immediate_threat(self, obstacle_grid, direction):
        """Check for immediate threats in a specific direction"""
        if direction == 'left':
            zone = obstacle_grid[:, :self.grid_width // 3]
        elif direction == 'right':
            zone = obstacle_grid[:, 2 * self.grid_width // 3:]
        else:  # center
            zone = obstacle_grid[:, self.grid_width // 3:2 * self.grid_width // 3]
        
        # Check the forward-most part of the zone
        if zone.shape[0] > 0:
            front_third = zone[:zone.shape[0] // 3, :]
            return 1.0 / (np.mean(front_third) + 0.1)
        return 1.0
    
    def calculate_path_safety(self, obstacle_grid):
        """Calculate overall path safety score (0-100)"""
        non_zero_obstacles = obstacle_grid[obstacle_grid > 0]
        if len(non_zero_obstacles) == 0:
            return 100
        
        mean_obstacle_density = np.mean(non_zero_obstacles)
        safety_score = max(0, 100 - (mean_obstacle_density * 10))
        return min(100, safety_score)
    
    def a_star_search(self, obstacle_grid, start_pos, goal_pos):
        """A* pathfinding algorithm for navigation"""
        def heuristic(pos):
            return abs(pos[0] - goal_pos[0]) + abs(pos[1] - goal_pos[1])
        
        def get_neighbors(pos):
            x, y = pos
            neighbors = []
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_width and 0 <= ny < self.grid_height:
                    neighbors.append((nx, ny))
            return neighbors
        
        open_set = [(0, start_pos)]
        came_from = {}
        g_score = {start_pos: 0}
        f_score = {start_pos: heuristic(start_pos)}
        
        closed_set = set()
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == goal_pos:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_pos)
                return path[::-1]
            
            closed_set.add(current)
            
            for neighbor in get_neighbors(current):
                if neighbor in closed_set:
                    continue
                
                # Cost increases with obstacle density
                movement_cost = 1 + obstacle_grid[neighbor[1], neighbor[0]]
                tentative_g = g_score[current] + movement_cost
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor)
                    f_score[neighbor] = f
                    heapq.heappush(open_set, (f, neighbor))
        
        return []  # No path found
    
    def get_corridor_width(self, obstacle_grid, direction):
        """Calculate the width of safe corridor in a direction"""
        if direction == 'left':
            zone = obstacle_grid[:, :self.grid_width // 3]
        elif direction == 'right':
            zone = obstacle_grid[:, 2 * self.grid_width // 3:]
        else:
            zone = obstacle_grid[:, self.grid_width // 3:2 * self.grid_width // 3]
        
        safe_cells = np.sum(zone < 1.0)
        return int(safe_cells / max(1, zone.shape[0]))
