"""
Configuration settings for Indoor Navigation System
"""

# Vision and Detection
DETECTION_CONFIG = {
    'model_path': 'yolov8n.pt',
    'confidence_threshold': 0.5,
    'important_classes': [
        'person', 'chair', 'table', 'sofa', 'bed',
        'refrigerator', 'tv', 'monitor', 'keyboard', 'mouse',
        'bottle', 'cup', 'book', 'backpack', 'handbag'
    ],
    'priority_weights': {
        'person': 3,
        'chair': 2,
        'table': 2,
        'sofa': 1,
        'bed': 1,
        'refrigerator': 2,
        'tv': 1,
        'monitor': 1,
        'keyboard': 3,
        'mouse': 3,
        'bottle': 2,
        'cup': 2,
        'book': 1,
        'backpack': 1,
        'handbag': 1
    }
}

# Depth Sensing
DEPTH_CONFIG = {
    'model_type': 'MiDaS_small',
    'distance_thresholds': {
        'very_close': 0.7,
        'close': 0.4,
        'moderate': 0.2,
        'far': 0.0
    }
}

# Voice Configuration
VOICE_CONFIG = {
    'engine': 'pyttsx3',
    'language': 'en',
    'voice_rate': 150,  # words per minute
    'volume': 1.0,  # 0.0 to 1.0
    'use_audio_queue': True,
    'feedback_cooldown': 2  # seconds
}

# Navigation Engine
NAVIGATION_CONFIG = {
    'grid_cell_size': 20,  # pixels per grid cell
    'obstacle_density_threshold': 0.5,  # for safe zones
    'danger_zone_threshold': 2.0,  # for dangerous zones
    'path_safety_score_threshold': 70,  # minimum safe percentage
    'blocked_timeout': 10  # seconds before alerting user
}

# Danger Levels
DANGER_LEVELS = {
    1: {'name': 'LOW', 'color': (0, 255, 0), 'action': 'AWARE'},
    2: {'name': 'MODERATE', 'color': (0, 255, 255), 'action': 'CAUTION'},
    3: {'name': 'HIGH', 'color': (0, 165, 255), 'action': 'MOVE CAREFULLY'},
    4: {'name': 'CRITICAL', 'color': (0, 0, 255), 'action': 'MOVE IMMEDIATELY'},
    5: {'name': 'IMMEDIATE', 'color': (0, 0, 128), 'action': 'STOP'}
}

# Camera Configuration
CAMERA_CONFIG = {
    'camera_index': 0,
    'frame_width': 640,
    'frame_height': 480,
    'fps': 30
}

# Environment Mapping
ENVIRONMENT_CONFIG = {
    'memory_file': 'environment_memory.json',
    'save_frequency': 100,  # save every N frames
    'learning_enabled': True
}

# Logging Configuration
LOGGING_CONFIG = {
    'log_file': 'navigation_log.txt',
    'log_decisions': True,
    'log_obstacles': True,
    'log_voice': True
}

# Safety Thresholds
SAFETY_CONFIG = {
    'min_corridor_width': 100,  # pixels
    'emergency_stop_distance': 0.85,  # normalized depth
    'path_blocked_threshold': 0.3,  # safe zone percentage
    'consecutive_obstacle_limit': 5  # triggers reassessment
}

# Room Detection (Optional - can be extended)
ROOM_PROFILES = {
    'living_room': ['sofa', 'table', 'tv'],
    'kitchen': ['refrigerator', 'chair', 'table'],
    'bedroom': ['bed', 'chair'],
    'bathroom': [],  # minimal obstacles expected
    'hallway': []  # should be clear path
}

# Guidance Messages
GUIDANCE_TEMPLATES = {
    'obstacle_ahead': "There's a {object} ahead, {distance}. {action}",
    'clear_path': "Path is clear. You can move forward.",
    'turn_needed': "Turn {direction} to avoid {object}.",
    'stop_warning': "STOP! {object} is too close. Do not move.",
    'safe_zone': "Safe zone ahead. Continue forward.",
    'path_blocked': "Path ahead is blocked. Move {direction}.",
    'environment_learned': "I've learned about {object} in your home.",
}

# System Limits
SYSTEM_LIMITS = {
    'max_simultaneous_detections': 5,
    'max_history_frames': 1000,
    'max_environment_map_size': 1000,  # cells
}
