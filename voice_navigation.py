"""
Enhanced Voice Navigation System
Provides intelligent voice guidance for navigation
"""

import pyttsx3
import queue
import threading
from datetime import datetime, timedelta

class VoiceNavigationSystem:
    """Intelligent voice guidance system for navigation"""
    
    def __init__(self, rate=150):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', 1.0)
        
        # Track voice feedback to avoid repetition
        self.last_feedback = {}
        self.feedback_cooldown = 2  # seconds
        
        # Queue for voice commands
        self.voice_queue = queue.Queue()
        self.voice_thread = threading.Thread(target=self._process_voice_queue, daemon=True)
        self.voice_thread.start()
        
        # Voice feedback history
        self.feedback_history = []
        
        # Guidance templates
        self.templates = {
            'obstacle_ahead': "There's a {object} ahead, {distance}. {action}",
            'clear_path': "Path is clear. You can move forward.",
            'turn_needed': "Turn {direction} to avoid {object}.",
            'stop_warning': "STOP! {object} is too close. Do not move.",
            'safe_zone': "Safe zone ahead. Continue forward.",
            'path_blocked': "Path ahead is blocked. Move {direction}.",
            'corner_alert': "Corner detected on your {direction}.",
            'object_learned': "I've learned about {object} in your home.",
            'navigation_start': "Navigation started. I'll guide you safely.",
            'navigation_end': "Navigation complete.",
            'environment_summary': "I've detected {count} types of obstacles in this area."
        }
    
    def _process_voice_queue(self):
        """Process voice commands from queue in a separate thread"""
        while True:
            try:
                message = self.voice_queue.get(timeout=1)
                self.engine.say(message)
                self.engine.runAndWait()
            except queue.Empty:
                continue
    
    def say(self, message, priority='normal', wait=False):
        """Queue a voice message"""
        if wait:
            self.engine.say(message)
            self.engine.runAndWait()
        else:
            self.voice_queue.put(message)
        
        # Log in history
        self.feedback_history.append({
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'priority': priority
        })
    
    def provide_obstacle_guidance(self, obstacle_info):
        """Provide comprehensive obstacle guidance"""
        label = obstacle_info.get('object')
        distance = obstacle_info.get('distance')
        action = obstacle_info.get('action')
        urgency = obstacle_info.get('urgency')
        
        # Create message based on urgency
        if urgency == 'IMMEDIATE':
            message = f"STOP! {label} is right in front of you! {action}!"
        elif urgency == 'URGENT':
            message = f"Alert! {label} ahead at {distance}. {action} immediately!"
        elif urgency == 'CAUTION':
            message = f"Watch out! {label} ahead at {distance}. Please {action}."
        else:
            message = f"{label} detected. {distance}. {action}."
        
        # Check cooldown to avoid repetitive messages
        key = f"{label}_{distance}_{action}"
        now = datetime.now()
        
        if key not in self.last_feedback or \
           (now - self.last_feedback[key]) > timedelta(seconds=self.feedback_cooldown):
            self.say(message, priority=urgency)
            self.last_feedback[key] = now
    
    def provide_path_guidance(self, path_info):
        """Provide path safety and direction guidance"""
        safest_zone = path_info.get('safest_zone')
        confidence = path_info.get('confidence', 0)
        
        if confidence > 0.7:
            message = f"Path is clear on your {safest_zone}. Move in that direction."
        elif confidence > 0.4:
            message = f"You can move {safest_zone}, but be cautious."
        else:
            message = f"All paths are blocked. Stop and assess your surroundings."
        
        self.say(message, priority='normal')
    
    def provide_safety_alert(self, alert_type, details=None):
        """Provide specific safety alerts"""
        alerts = {
            'immediate_danger': "CRITICAL! Immediate danger detected. STOP!",
            'blocked_path': "The path ahead is completely blocked. Do not proceed.",
            'unknown_object': "Unknown obstacle detected. Proceed with caution.",
            'moving_object': "Movement detected nearby. Be alert!",
            'corner_ahead': "Corner or wall edge detected ahead.",
            'open_space': "Large open space detected ahead.",
            'enclosed_space': "Enclosed area detected. Move carefully.",
            'high_step': "Step or high edge detected ahead.",
            'multiple_obstacles': f"Multiple obstacles detected in this area.",
            'path_clear': "Immediate area is clear. Safe to move forward."
        }
        
        message = alerts.get(alert_type, "Alert: Be careful ahead.")
        
        if details:
            message += f" {details}"
        
        self.say(message, priority='high')
    
    def provide_directional_guidance(self, direction, obstacles_to_avoid=None):
        """Provide directional guidance"""
        directions = {
            'left': "Turn slightly to your left",
            'right': "Turn slightly to your right",
            'straight': "Continue straight ahead",
            'far_left': "Turn sharply to your left",
            'far_right': "Turn sharply to your right",
            'stop': "Stop immediately",
            'backtrack': "Move backward carefully"
        }
        
        message = directions.get(direction, "Adjust your direction")
        
        if obstacles_to_avoid:
            obstacles = ", ".join(obstacles_to_avoid)
            message += f" to avoid {obstacles}."
        else:
            message += "."
        
        self.say(message, priority='normal')
    
    def provide_room_feedback(self, room_type, obstacles_found):
        """Provide feedback about room characteristics"""
        room_context = {
            'living_room': "You're in the living room. Watch out for furniture.",
            'kitchen': "You're in the kitchen. Be careful with appliances.",
            'bedroom': "You're in the bedroom. Watch for the bed.",
            'hallway': "You're in a hallway. Stay centered.",
            'bathroom': "You're in the bathroom. Watch for slippery surfaces.",
            'stairway': "You're near stairs. Be extremely careful.",
            'unknown': "Analyzing the space around you."
        }
        
        message = room_context.get(room_type, "Analyzing the space around you.")
        
        if obstacles_found:
            obstacles_str = ", ".join(obstacles_found)
            message += f" Obstacles detected: {obstacles_str}."
        
        self.say(message, priority='normal')
    
    def provide_navigation_summary(self, summary_info):
        """Provide summary of the navigation experience"""
        obstacles_detected = summary_info.get('obstacles_detected', 0)
        safe_passages = summary_info.get('safe_passages', 0)
        
        message = f"Navigation summary. "
        message += f"Detected {obstacles_detected} obstacles. "
        message += f"Found {safe_passages} safe passages. "
        
        learned_obstacles = summary_info.get('learned_obstacles', {})
        if learned_obstacles:
            obstacles_list = ", ".join(learned_obstacles.keys())
            message += f"Learned about: {obstacles_list}."
        
        self.say(message, priority='normal')
    
    def provide_continuous_guidance(self, path_safety_score):
        """Provide continuous guidance based on path safety"""
        if path_safety_score >= 80:
            messages = [
                "Path is very clear. Continue forward.",
                "Safe to move ahead.",
                "No obstacles detected. Proceed."
            ]
        elif path_safety_score >= 60:
            messages = [
                "Path is mostly clear. Move forward cautiously.",
                "Some obstacles nearby. Watch your step.",
                "Be alert. Some objects ahead."
            ]
        elif path_safety_score >= 40:
            messages = [
                "Multiple obstacles detected. Move carefully.",
                "Caution. Several objects in your path.",
                "Proceed slowly. Obstacles detected."
            ]
        else:
            messages = [
                "Area is heavily congested. Stop and assess.",
                "Many obstacles ahead. Do not proceed.",
                "Too many obstructions. Choose a different path."
            ]
        
        # Cycle through messages to avoid repetition
        message = messages[len(self.feedback_history) % len(messages)]
        self.say(message, priority='normal')
    
    def emergency_stop(self):
        """Emergency stop announcement"""
        self.say("EMERGENCY STOP! Do not move! Analyze your surroundings!", priority='critical')
    
    def reset(self):
        """Reset voice system"""
        self.last_feedback = {}
        self.feedback_history = []
