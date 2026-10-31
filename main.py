"""
Complete Indoor Navigation System for Visually Impaired Users
Real-time obstacle detection, environment mapping, path planning, and voice guidance
"""

import cv2
import numpy as np
from detection import detect_objects
from depth import get_depth_map
from voice_navigation import VoiceNavigationSystem
from enhanced_decision import NavigationDecisionEngine
from obstacle_analyzer import ObstacleAnalyzer

class IndoorNavigationSystem:
    """Complete navigation system for visually impaired users"""
    
    def __init__(self, use_camera=True):
        self.use_camera = use_camera
        
        # Initialize components
        self.decision_engine = NavigationDecisionEngine(frame_width=640, frame_height=480)
        self.voice_system = VoiceNavigationSystem(rate=150)
        self.obstacle_analyzer = ObstacleAnalyzer()
        
        # Session state
        self.frame_count = 0
        self.is_running = False
        self.depth_min_ema = None
        self.depth_max_ema = None
        
        # For visualization
        self.show_visualization = True
        self.last_guidance_time = None
        
        # Camera setup
        if use_camera:
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    def start(self):
        """Start navigation system"""
        self.is_running = True
        self.decision_engine.start_navigation()
        self.voice_system.say("Navigation started. I will guide you safely.", wait=True)
        print("✓ Indoor Navigation System Started")
        print("✓ Voice Guidance Enabled")
        print("✓ Environment Mapping Active")
        print("Press ESC to end navigation\n")
    
    def stop(self):
        """Stop navigation system"""
        self.is_running = False
        self.decision_engine.end_navigation()
        self.voice_system.say("Navigation ended. Thank you for using this system.")
        
        # Display summary
        self._display_navigation_summary()
    
    def run(self):
        """Main navigation loop"""
        self.start()
        
        while self.is_running:
            # Get frame
            if self.use_camera:
                ret, frame = self.cap.read()
                if not ret:
                    break
            else:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
            
            height, width, _ = frame.shape
            
            # Get depth map
            depth_map = get_depth_map(frame)
            
            # Normalize depth using a smoothed min/max across frames, so a single
            # frame's nearest pixel doesn't always get stretched to "very close"
            # ponytail: relative-depth model has no true distance calibration; this
            # only reduces frame-to-frame noise, upgrade to a calibrated sensor if
            # false "very close" triggers persist
            min_val, max_val = depth_map.min(), depth_map.max()
            if self.depth_min_ema is None:
                self.depth_min_ema, self.depth_max_ema = min_val, max_val
            else:
                alpha = 0.1
                self.depth_min_ema = alpha * min_val + (1 - alpha) * self.depth_min_ema
                self.depth_max_ema = alpha * max_val + (1 - alpha) * self.depth_max_ema
            normalized_depth = (depth_map - self.depth_min_ema) / (self.depth_max_ema - self.depth_min_ema + 1e-6)
            normalized_depth = np.clip(normalized_depth, 0, 1)
            
            # Detect objects
            obj = detect_objects(frame)
            
            # Make navigation decision
            decision = self.decision_engine.make_navigation_decision(
                obj, normalized_depth, frame
            )
            
            # Process decision
            self._process_decision(decision, frame, width, height, obj)
            
            # Display visualization
            if self.show_visualization:
                self._draw_visualization(frame, decision, obj, width, height)
                cv2.imshow("Indoor Navigation - Visual Feedback", frame)
            
            # Check for exit
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                break
            
            self.frame_count += 1
        
        self.stop()
    
    def _process_decision(self, decision, frame, width, height, obj):
        """Process navigation decision and provide guidance"""
        action = decision.get('action')
        guidance = decision.get('guidance', {})
        warnings = decision.get('warnings', [])
        
        # Provide voice guidance
        if action == 'stop_immediately':
            obstacle_info = decision.get('obstacle_info', {})
            x1, y1, x2, y2 = obstacle_info.get('position', (0, 0, 0, 0))
            center_x = (x1 + x2) // 2
            if center_x < width // 3:
                position = "on your left"
            elif center_x < 2 * width // 3:
                position = "right in front of you"
            else:
                position = "on your right"
            self.voice_system.emergency_stop(
                obstacle_label=obstacle_info.get('label'),
                position=position
            )
        
        elif obj:
            obstacle_info = decision.get('obstacle_info', {})
            self.voice_system.provide_obstacle_guidance(
                {
                    'object': obstacle_info.get('label'),
                    'distance': obstacle_info.get('distance'),
                    'action': guidance.get('direction', guidance.get('action', 'Be careful')),
                    'urgency': self._get_urgency(obstacle_info.get('danger_level', 2)),
                    'other_objects_count': obstacle_info.get('other_objects_count', 0)
                }
            )
        else:
            # No obstacle - check path safety
            if action == 'move_forward':
                self.voice_system.say("Path is clear. Move forward.")
            elif action == 'move_carefully':
                self.voice_system.provide_path_guidance({
                    'safest_zone': 'your preferred direction',
                    'confidence': decision.get('confidence', 0)
                })
    
    def _get_urgency(self, danger_level):
        """Map danger level to urgency"""
        if danger_level >= 5:
            return 'IMMEDIATE'
        elif danger_level >= 4:
            return 'URGENT'
        elif danger_level >= 3:
            return 'CAUTION'
        else:
            return 'AWARE'
    
    def _draw_visualization(self, frame, decision, objects, width, height):
        """Draw visualization on frame"""
        if objects:
            obstacle_info = decision.get('obstacle_info', {})
            primary_position = obstacle_info.get('position')
            action = decision.get('action')

            for label, x1, y1, x2, y2 in objects:
                is_primary = (x1, y1, x2, y2) == primary_position
                if is_primary and action == 'stop_immediately':
                    color = (0, 0, 255)  # Red for danger
                elif is_primary and action in ['avoid_and_move', 'move_carefully']:
                    color = (0, 165, 255)  # Orange for caution
                elif is_primary:
                    color = (0, 255, 0)  # Green for safe
                else:
                    color = (200, 200, 0)  # Dim cyan for other, non-primary obstacles

                thickness = 3 if is_primary else 1
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

                if is_primary:
                    distance = obstacle_info.get('distance', 'UNKNOWN')
                    danger_level = obstacle_info.get('danger_level', 0)
                    label_text = f"{label} - {distance} (Danger: {danger_level}/5)"
                else:
                    label_text = label
                cv2.putText(frame, label_text, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Draw action guidance
        guidance = decision.get('guidance', {})
        primary = guidance.get('primary', '')
        action = guidance.get('action', '')
        
        if primary:
            cv2.putText(frame, f"→ {primary}", (20, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        if action:
            cv2.putText(frame, f"→ {action}", (20, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
        
        # Draw environment status
        state = self.decision_engine.get_current_state()
        path_status = "CLEAR" if state['path_clear'] else "CONGESTED"
        status_color = (0, 255, 0) if state['path_clear'] else (0, 0, 255)
        
        cv2.putText(frame, f"Path: {path_status}", (20, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        
        # Draw frame counter
        cv2.putText(frame, f"Frame: {self.frame_count}", (width - 150, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    
    def _display_navigation_summary(self):
        """Display navigation session summary"""
        summary = self.decision_engine.get_navigation_summary()
        
        print("\n" + "="*60)
        print("NAVIGATION SESSION SUMMARY")
        print("="*60)
        print(f"Total Obstacles Encountered: {summary['total_obstacles_encountered']}")
        print(f"Safe Passages Found: {summary['safe_passages_found']}")
        print(f"Path Safety Score: {summary['path_safety_score']:.1f}%")
        print(f"\nLearned Obstacles:")
        for obstacle, count in summary['learned_obstacles'].items():
            print(f"  • {obstacle.capitalize()}: {count} times")
        print(f"\nEnvironment Summary:")
        env = summary['environment']
        print(f"  • Total Detections: {env['total_obstacles_detected']}")
        print(f"  • Safe Zones: {env['safe_zones_count']}")
        print(f"  • Dangerous Zones: {env['dangerous_zones_count']}")
        print("="*60)
        print("✓ Environment map saved to 'environment_memory.json'")
        print("✓ Navigation session complete")
        print("="*60 + "\n")
    
    def cleanup(self):
        """Cleanup resources"""
        if self.use_camera:
            self.cap.release()
        cv2.destroyAllWindows()


def main():
    """Main entry point"""
    try:
        # Create and run navigation system
        navigation = IndoorNavigationSystem(use_camera=True)
        navigation.run()
    
    except KeyboardInterrupt:
        print("\n✓ Navigation interrupted by user")
    
    except Exception as e:
        print(f"✗ Error: {e}")
    
    finally:
        navigation.cleanup()


if __name__ == "__main__":
    main()
cv2.destroyAllWindows()