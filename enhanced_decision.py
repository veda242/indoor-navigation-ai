"""
Enhanced Decision Engine
Orchestrates navigation decisions using all system components
"""

import numpy as np
from datetime import datetime, timedelta
from obstacle_analyzer import ObstacleAnalyzer
from environment_mapper import EnvironmentMapper
from path_planner import PathPlanner

class NavigationDecisionEngine:
    """Main decision engine for safe navigation"""
    
    def __init__(self, frame_width=640, frame_height=480):
        self.frame_width = frame_width
        self.frame_height = frame_height
        
        # Initialize system components
        self.obstacle_analyzer = ObstacleAnalyzer()
        self.environment_mapper = EnvironmentMapper(frame_width, frame_height)
        self.path_planner = PathPlanner(frame_width, frame_height)
        
        # State tracking
        self.last_decision = None
        self.last_decision_time = None
        self.consecutive_obstacles = 0
        self.is_blocked = False
        self.blocked_start_time = None
        
        # Navigation state
        self.navigation_active = False
        self.total_obstacles_encountered = 0
        self.safe_passages_found = 0
    
    def make_navigation_decision(self, detected_object, depth_map, frame):
        """Make comprehensive navigation decision"""
        decision = {
            'action': 'continue',
            'confidence': 0,
            'warnings': [],
            'guidance': {},
            'map_update': False
        }
        
        if detected_object:
            label, x1, y1, x2, y2 = detected_object
            
            # Analyze the detected obstacle
            depth_value = self._get_depth_value(depth_map, x1, y1, x2, y2)
            distance = self._classify_distance(depth_value)
            
            # Track obstacle in environment
            self.environment_mapper.add_obstacle(x1, y1, x2, y2, label, distance, depth_value)
            decision['map_update'] = True
            
            # Get obstacle analysis
            obstacle_info = self.obstacle_analyzer.classify_obstacle(label)
            danger_level = self.obstacle_analyzer.get_danger_level(label, distance)
            frequency = self.obstacle_analyzer.track_obstacle_frequency(label)
            
            # Get position in frame
            center_x = (x1 + x2) // 2
            
            # Generate comprehensive guidance
            guidance = self._generate_guidance(
                label, distance, center_x, depth_value, 
                obstacle_info, danger_level
            )
            
            decision['guidance'] = guidance
            decision['obstacle_info'] = {
                'label': label,
                'position': (x1, y1, x2, y2),
                'distance': distance,
                'danger_level': danger_level,
                'frequency': frequency
            }
            
            # Determine action
            decision = self._determine_action(
                label, distance, center_x, danger_level, decision
            )
            
            self.total_obstacles_encountered += 1
            self.consecutive_obstacles += 1
        else:
            # No obstacle detected - path is clear
            self.consecutive_obstacles = 0
            
            # Check environment for safe paths
            safe_zone, zone_scores, confidence = self.path_planner.find_safe_corridor(
                self.environment_mapper.obstacle_grid, 
                self.frame_width // 2, 
                self.frame_height // 2
            )
            
            path_safety = self.path_planner.calculate_path_safety(
                self.environment_mapper.obstacle_grid
            )
            
            if path_safety > 70:
                decision['action'] = 'move_forward'
                decision['confidence'] = 0.9
                decision['guidance']['primary'] = "Path is clear. Move forward."
                self.safe_passages_found += 1
            else:
                decision['action'] = 'move_carefully'
                decision['confidence'] = 0.5
                decision['guidance']['primary'] = f"Proceed carefully toward {safe_zone}."
        
        self.last_decision = decision
        self.last_decision_time = datetime.now()
        
        return decision
    
    def _get_depth_value(self, depth_map, x1, y1, x2, y2):
        """Extract depth value for obstacle"""
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        
        region = depth_map[
            max(0, center_y - 10):center_y + 10,
            max(0, center_x - 10):center_x + 10
        ]
        
        if region.size > 0:
            return region.mean()
        return 0.5
    
    def _classify_distance(self, depth_value):
        """Classify distance from depth value"""
        if depth_value > 0.7:
            return 'VERY CLOSE'
        elif depth_value > 0.4:
            return 'CLOSE'
        elif depth_value > 0.2:
            return 'MODERATE'
        else:
            return 'FAR'
    
    def _generate_guidance(self, label, distance, center_x, depth_value, 
                         obstacle_info, danger_level):
        """Generate comprehensive guidance"""
        guidance = {}
        
        # Position guidance
        if center_x < self.frame_width // 3:
            position_msg = "on your left"
            move_direction = "right"
        elif center_x < 2 * self.frame_width // 3:
            position_msg = "in front of you"
            move_direction = "carefully"
        else:
            position_msg = "on your right"
            move_direction = "left"
        
        guidance['primary'] = f"{label} detected {position_msg}"
        guidance['action'] = f"Move {move_direction}"
        guidance['distance_info'] = f"Distance: {distance.lower()}"
        
        # Detail message
        category = obstacle_info['category']
        if category == 'small_object':
            guidance['detail'] = f"Small {label} on the ground. Step carefully."
        elif category == 'dynamic':
            guidance['detail'] = f"Person nearby. Call out to get their attention."
        elif category == 'furniture':
            guidance['detail'] = f"{label.capitalize()} obstacle. Walk around it."
        else:
            guidance['detail'] = f"Unknown {label}. Proceed with caution."
        
        return guidance
    
    def _determine_action(self, label, distance, center_x, danger_level, decision):
        """Determine the navigation action"""
        if danger_level >= 5 or distance == 'VERY CLOSE':
            decision['action'] = 'stop_immediately'
            decision['confidence'] = 1.0
            decision['warnings'].append(f"CRITICAL: {label} too close!")
            self.is_blocked = True
            self.blocked_start_time = datetime.now()
        
        elif danger_level >= 4 or distance == 'CLOSE':
            decision['action'] = 'avoid_and_move'
            decision['confidence'] = 0.8
            
            if center_x < self.frame_width // 3:
                decision['guidance']['direction'] = "Move right to avoid"
            elif center_x < 2 * self.frame_width // 3:
                decision['guidance']['direction'] = "Choose left or right"
            else:
                decision['guidance']['direction'] = "Move left to avoid"
            
            decision['warnings'].append(f"Caution: {label} approaching")
        
        elif danger_level >= 3:
            decision['action'] = 'move_carefully'
            decision['confidence'] = 0.6
            decision['warnings'].append(f"Alert: {label} detected")
        
        else:
            decision['action'] = 'aware'
            decision['confidence'] = 0.4
            decision['guidance']['detail'] = f"Be aware of {label}"
        
        return decision
    
    def get_navigation_summary(self):
        """Get navigation session summary"""
        environment_summary = self.environment_mapper.get_environment_summary()
        
        summary = {
            'session_duration': self._get_session_duration(),
            'total_obstacles_encountered': self.total_obstacles_encountered,
            'safe_passages_found': self.safe_passages_found,
            'learned_obstacles': self.obstacle_analyzer.get_learned_obstacles(),
            'environment': environment_summary,
            'path_safety_score': self.path_planner.calculate_path_safety(
                self.environment_mapper.obstacle_grid
            )
        }
        
        return summary
    
    def _get_session_duration(self):
        """Get navigation session duration"""
        if self.navigation_active and self.last_decision_time:
            duration = datetime.now() - self.last_decision_time
            return str(duration)
        return "N/A"
    
    def start_navigation(self):
        """Start navigation session"""
        self.navigation_active = True
        self.total_obstacles_encountered = 0
        self.safe_passages_found = 0
    
    def end_navigation(self):
        """End navigation session"""
        self.navigation_active = False
        self.environment_mapper.save_environment()
    
    def is_path_clear(self, clearance_threshold=0.3):
        """Check if path is clear"""
        obstacle_density = np.mean(self.environment_mapper.obstacle_grid)
        return obstacle_density < clearance_threshold
    
    def get_safe_direction_options(self):
        """Get all safe direction options"""
        safe_zone, zone_scores, confidence = self.path_planner.find_safe_corridor(
            self.environment_mapper.obstacle_grid,
            self.frame_width // 2,
            self.frame_height // 2
        )
        
        options = []
        for direction, score in zone_scores.items():
            if score > 0.5:
                corridor_width = self.path_planner.get_corridor_width(
                    self.environment_mapper.obstacle_grid, 
                    direction
                )
                options.append({
                    'direction': direction,
                    'safety_score': score,
                    'corridor_width': corridor_width
                })
        
        return sorted(options, key=lambda x: x['safety_score'], reverse=True)
    
    def get_current_state(self):
        """Get current navigation state"""
        return {
            'is_active': self.navigation_active,
            'is_blocked': self.is_blocked,
            'consecutive_obstacles': self.consecutive_obstacles,
            'last_decision': self.last_decision,
            'path_clear': self.is_path_clear(),
            'safe_directions': self.get_safe_direction_options()
        }
