"""
Environment Mapper Module
Maps and remembers the house layout, obstacles, and safe zones
"""

import numpy as np
import json
import os
from datetime import datetime
from collections import defaultdict

class EnvironmentMapper:
    """Maps the house environment and tracks obstacles"""
    
    def __init__(self, frame_width=640, frame_height=480, grid_cell_size=20):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.grid_cell_size = grid_cell_size
        
        # Create grid for environment mapping
        self.grid_width = frame_width // grid_cell_size
        self.grid_height = frame_height // grid_cell_size
        
        # Track obstacles in grid (frequency map)
        self.obstacle_grid = np.zeros((self.grid_height, self.grid_width), dtype=np.float32)
        
        # Track obstacle types
        self.obstacle_types = defaultdict(lambda: np.zeros((self.grid_height, self.grid_width), dtype=np.int32))
        
        # Session data
        self.session_data = {
            'obstacles_detected': [],
            'safe_zones': [],
            'dangerous_zones': [],
            'timestamps': []
        }
        
        self.environment_file = "environment_memory.json"
        self.load_environment()
    
    def add_obstacle(self, x1, y1, x2, y2, label, distance, depth_value):
        """Add obstacle to the map"""
        # Convert to grid coordinates
        grid_x1 = max(0, min(self.grid_width - 1, x1 // self.grid_cell_size))
        grid_x2 = max(0, min(self.grid_width - 1, x2 // self.grid_cell_size))
        grid_y1 = max(0, min(self.grid_height - 1, y1 // self.grid_cell_size))
        grid_y2 = max(0, min(self.grid_height - 1, y2 // self.grid_cell_size))
        
        # Update obstacle grid with depth-based weighting
        weight = 1.0 / (depth_value + 0.1)  # Closer obstacles have higher weight
        self.obstacle_grid[grid_y1:grid_y2+1, grid_x1:grid_x2+1] += weight
        
        # Track obstacle type
        self.obstacle_types[label][grid_y1:grid_y2+1, grid_x1:grid_x2+1] += 1
        
        # Record in session
        self.session_data['obstacles_detected'].append({
            'label': label,
            'position': (x1, y1, x2, y2),
            'distance': distance,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_safe_zones(self, threshold=0.5):
        """Identify safe zones with low obstacle density"""
        safe_zones = np.where(self.obstacle_grid < threshold)
        return list(zip(safe_zones[1], safe_zones[0]))  # Return (x, y) grid coordinates
    
    def get_dangerous_zones(self, threshold=2.0):
        """Identify dangerous zones with high obstacle density"""
        dangerous_zones = np.where(self.obstacle_grid >= threshold)
        return list(zip(dangerous_zones[1], dangerous_zones[0]))  # Return (x, y) grid coordinates
    
    def get_zone_at_position(self, x, y):
        """Get the hazard level at a specific position"""
        grid_x = max(0, min(self.grid_width - 1, x // self.grid_cell_size))
        grid_y = max(0, min(self.grid_height - 1, y // self.grid_cell_size))
        return self.obstacle_grid[grid_y, grid_x]
    
    def get_safe_direction(self, current_x, current_y, width):
        """Determine the safest direction to move"""
        center = width // 2
        left_score = np.mean(self.obstacle_grid[:, :self.grid_width // 3])
        center_score = np.mean(self.obstacle_grid[:, self.grid_width // 3:2 * self.grid_width // 3])
        right_score = np.mean(self.obstacle_grid[:, 2 * self.grid_width // 3:])
        
        scores = {
            'left': left_score,
            'center': center_score,
            'right': right_score
        }
        
        return min(scores, key=scores.get), scores
    
    def get_environment_summary(self):
        """Get summary of detected environment"""
        obstacle_types_summary = {}
        for label, grid in self.obstacle_types.items():
            count = np.sum(grid > 0)
            obstacle_types_summary[label] = int(count)
        
        return {
            'total_obstacles_detected': len(self.session_data['obstacles_detected']),
            'obstacle_types': obstacle_types_summary,
            'safe_zones_count': len(self.get_safe_zones()),
            'dangerous_zones_count': len(self.get_dangerous_zones())
        }
    
    def save_environment(self):
        """Save environment map to file"""
        data = {
            'obstacle_grid': self.obstacle_grid.tolist(),
            'obstacle_types': {label: grid.tolist() for label, grid in self.obstacle_types.items()},
            'session_data': self.session_data,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(self.environment_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_environment(self):
        """Load saved environment map"""
        if os.path.exists(self.environment_file):
            try:
                with open(self.environment_file, 'r') as f:
                    data = json.load(f)
                
                self.obstacle_grid = np.array(data.get('obstacle_grid', 
                    np.zeros((self.grid_height, self.grid_width)).tolist()))
                
                for label, grid in data.get('obstacle_types', {}).items():
                    self.obstacle_types[label] = np.array(grid, dtype=np.int32)
                
                self.session_data = data.get('session_data', self.session_data)
            except Exception as e:
                print(f"Error loading environment: {e}")
    
    def reset_session(self):
        """Reset session data while keeping learned environment"""
        self.session_data = {
            'obstacles_detected': [],
            'safe_zones': [],
            'dangerous_zones': [],
            'timestamps': []
        }
