"""
Obstacle Analyzer Module
Analyzes and categorizes obstacles for safety assessment
"""

class ObstacleAnalyzer:
    """Analyzes obstacle characteristics and danger levels"""
    
    # Obstacle safety categories
    OBSTACLE_CATEGORIES = {
        # Static furniture obstacles
        'chair': {'category': 'furniture', 'danger_level': 2, 'height': 'medium'},
        'table': {'category': 'furniture', 'danger_level': 2, 'height': 'medium'},
        'sofa': {'category': 'furniture', 'danger_level': 2, 'height': 'medium'},
        'bed': {'category': 'furniture', 'danger_level': 1, 'height': 'medium'},
        'refrigerator': {'category': 'appliance', 'danger_level': 1, 'height': 'tall'},
        'tv': {'category': 'furniture', 'danger_level': 1, 'height': 'medium'},
        'monitor': {'category': 'electronics', 'danger_level': 1, 'height': 'medium'},
        'keyboard': {'category': 'small_object', 'danger_level': 3, 'height': 'low'},
        'mouse': {'category': 'small_object', 'danger_level': 3, 'height': 'low'},
        'book': {'category': 'small_object', 'danger_level': 2, 'height': 'low'},
        'person': {'category': 'dynamic', 'danger_level': 3, 'height': 'tall'},
        'bottle': {'category': 'small_object', 'danger_level': 2, 'height': 'low'},
        'cup': {'category': 'small_object', 'danger_level': 2, 'height': 'low'},
        'backpack': {'category': 'object', 'danger_level': 1, 'height': 'medium'},
        'handbag': {'category': 'small_object', 'danger_level': 1, 'height': 'low'},
        'suitcase': {'category': 'object', 'danger_level': 1, 'height': 'medium'},
    }
    
    # Distance-based danger classification
    DISTANCE_LEVELS = {
        'VERY CLOSE': 'critical',
        'CLOSE': 'high',
        'MODERATE': 'medium',
        'FAR': 'low'
    }
    
    def __init__(self):
        self.obstacle_history = {}
    
    def classify_obstacle(self, label):
        """Get classification for an obstacle type"""
        if label.lower() in self.OBSTACLE_CATEGORIES:
            return self.OBSTACLE_CATEGORIES[label.lower()]
        
        # Default classification for unknown objects
        return {
            'category': 'unknown',
            'danger_level': 2,
            'height': 'medium'
        }
    
    def get_danger_level(self, label, distance):
        """Calculate overall danger level (1-5, where 5 is most dangerous)"""
        classification = self.classify_obstacle(label)
        base_danger = classification['danger_level']
        
        distance_danger = {
            'critical': 5,
            'high': 4,
            'medium': 2,
            'low': 1
        }
        
        distance_level = self.DISTANCE_LEVELS.get(distance, 'low')
        distance_danger_value = distance_danger[distance_level]
        
        # Combined danger score (weighted average)
        overall_danger = (base_danger * 0.4) + (distance_danger_value * 0.6)
        return min(5, round(overall_danger))
    
    def get_safety_recommendation(self, label, distance, suggestion, depth_value):
        """Generate detailed safety recommendation"""
        danger_level = self.get_danger_level(label, distance)
        classification = self.classify_obstacle(label)
        
        # Priority-based recommendations
        if danger_level >= 5:
            urgency = "IMMEDIATE"
        elif danger_level >= 4:
            urgency = "URGENT"
        elif danger_level >= 3:
            urgency = "CAUTION"
        else:
            urgency = "AWARE"
        
        # Generate context-aware message
        recommendation = {
            'urgency': urgency,
            'object': label,
            'action': suggestion,
            'distance': distance,
            'category': classification['category'],
            'detail': self._get_detail_message(label, distance, classification)
        }
        
        return recommendation
    
    def _get_detail_message(self, label, distance, classification):
        """Generate detailed descriptive message"""
        category = classification['category']
        
        messages = {
            'furniture': f"There's a {label} in front of you at {distance.lower()} distance. ",
            'appliance': f"An appliance - {label} - is ahead of you. ",
            'electronics': f"Electronic device {label} detected at {distance.lower()} range. ",
            'small_object': f"Small object {label} on the ground - be careful. ",
            'dynamic': f"Person detected! {distance.lower()} distance ahead. ",
            'object': f"{label.capitalize()} is positioned ahead. ",
            'unknown': f"Unknown object {label} detected. "
        }
        
        detail = messages.get(category, f"{label} is ahead. ")
        
        # Add action advice
        if distance in ['VERY CLOSE', 'CLOSE']:
            detail += "STOP - assess your surroundings."
        elif category == 'small_object':
            detail += "Step carefully and feel your way."
        elif category == 'dynamic':
            detail += "Try to make contact to alert them."
        
        return detail
    
    def track_obstacle_frequency(self, label):
        """Track how frequently an obstacle appears"""
        if label not in self.obstacle_history:
            self.obstacle_history[label] = 0
        self.obstacle_history[label] += 1
        
        return self.obstacle_history[label]
    
    def get_learned_obstacles(self):
        """Get obstacles learned from the environment"""
        return self.obstacle_history
    
    def estimate_obstacle_size(self, x1, y1, x2, y2, frame_width, frame_height):
        """Estimate the size of the obstacle in the frame"""
        width = x2 - x1
        height = y2 - y1
        
        frame_area = frame_width * frame_height
        obstacle_area = width * height
        
        percentage = (obstacle_area / frame_area) * 100
        
        if percentage > 30:
            return 'large'
        elif percentage > 15:
            return 'medium'
        else:
            return 'small'
    
    def get_avoidance_strategy(self, label, position_in_frame, frame_width):
        """Get specific avoidance strategy based on obstacle position"""
        center = frame_width / 2
        relative_position = 'center'
        
        if position_in_frame < center / 2:
            relative_position = 'far left'
        elif position_in_frame < center:
            relative_position = 'left'
        elif position_in_frame < frame_width - center / 2:
            relative_position = 'center'
        elif position_in_frame < frame_width - center:
            relative_position = 'right'
        else:
            relative_position = 'far right'
        
        strategies = {
            'left': 'Move to the right to avoid it',
            'center': 'Move carefully - choose left or right',
            'right': 'Move to the left to avoid it',
            'far left': 'Stay toward the right side',
            'far right': 'Stay toward the left side'
        }
        
        return strategies.get(relative_position, 'Adjust your path')
