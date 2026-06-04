"""
System Testing and Diagnostics Module
Test individual components of the navigation system
"""

import cv2
import numpy as np
from detection import detect_objects
from depth import get_depth_map
from voice_navigation import VoiceNavigationSystem
from enhanced_decision import NavigationDecisionEngine
from obstacle_analyzer import ObstacleAnalyzer
import sys

class SystemDiagnostics:
    """Diagnostic tools for testing system components"""
    
    @staticmethod
    def test_camera():
        """Test camera access and basic functionality"""
        print("\n" + "="*60)
        print("CAMERA DIAGNOSTICS")
        print("="*60)
        
        try:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("✗ Camera not available")
                return False
            
            # Try to read a frame
            ret, frame = cap.read()
            
            if ret:
                print("✓ Camera is working")
                print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
                print(f"  Channels: {frame.shape[2]}")
                return True
            else:
                print("✗ Could not read from camera")
                return False
        
        except Exception as e:
            print(f"✗ Camera error: {e}")
            return False
        
        finally:
            cap.release()
    
    @staticmethod
    def test_detection():
        """Test object detection"""
        print("\n" + "="*60)
        print("OBJECT DETECTION DIAGNOSTICS")
        print("="*60)
        
        try:
            print("Loading YOLO model...")
            
            # This will download the model if needed
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("✗ Camera not available for test")
                return False
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                print("✗ Could not capture frame")
                return False
            
            print("Running detection...")
            obj = detect_objects(frame)
            
            if obj:
                label, x1, y1, x2, y2 = obj
                print(f"✓ Detection working")
                print(f"  Detected: {label}")
                print(f"  Bounding box: ({x1}, {y1}) to ({x2}, {y2})")
            else:
                print("✓ Detection working (no objects in current frame)")
            
            return True
        
        except Exception as e:
            print(f"✗ Detection error: {e}")
            return False
    
    @staticmethod
    def test_depth():
        """Test depth estimation"""
        print("\n" + "="*60)
        print("DEPTH ESTIMATION DIAGNOSTICS")
        print("="*60)
        
        try:
            print("Loading MiDaS depth model...")
            
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("✗ Camera not available for test")
                return False
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                print("✗ Could not capture frame")
                return False
            
            print("Computing depth map...")
            depth_map = get_depth_map(frame)
            
            print(f"✓ Depth estimation working")
            print(f"  Depth map shape: {depth_map.shape}")
            print(f"  Value range: {depth_map.min():.3f} to {depth_map.max():.3f}")
            print(f"  Mean value: {depth_map.mean():.3f}")
            
            return True
        
        except Exception as e:
            print(f"✗ Depth error: {e}")
            return False
    
    @staticmethod
    def test_voice():
        """Test voice system"""
        print("\n" + "="*60)
        print("VOICE SYSTEM DIAGNOSTICS")
        print("="*60)
        
        try:
            print("Initializing voice system...")
            voice = VoiceNavigationSystem()
            
            print("Testing voice output...")
            voice.say("System initialized. Voice test successful.", wait=True)
            
            print("✓ Voice system working")
            print("  You should have heard a test message.")
            
            return True
        
        except Exception as e:
            print(f"✗ Voice error: {e}")
            return False
    
    @staticmethod
    def test_obstacle_analyzer():
        """Test obstacle analysis"""
        print("\n" + "="*60)
        print("OBSTACLE ANALYZER DIAGNOSTICS")
        print("="*60)
        
        try:
            analyzer = ObstacleAnalyzer()
            
            # Test various obstacle types
            test_objects = ['chair', 'person', 'keyboard', 'table', 'unknown']
            
            print("Testing obstacle classification:")
            for obj in test_objects:
                classification = analyzer.classify_obstacle(obj)
                print(f"  {obj}: {classification}")
            
            print("\nTesting danger level calculation:")
            distances = ['VERY CLOSE', 'CLOSE', 'MODERATE', 'FAR']
            for dist in distances:
                danger = analyzer.get_danger_level('chair', dist)
                print(f"  Chair at {dist}: Danger level {danger}/5")
            
            print("✓ Obstacle analyzer working")
            return True
        
        except Exception as e:
            print(f"✗ Obstacle analyzer error: {e}")
            return False
    
    @staticmethod
    def test_decision_engine():
        """Test decision engine"""
        print("\n" + "="*60)
        print("DECISION ENGINE DIAGNOSTICS")
        print("="*60)
        
        try:
            engine = NavigationDecisionEngine()
            
            print("Testing decision engine initialization...")
            
            # Test with mock depth map
            mock_depth = np.ones((480, 640)) * 0.5
            
            # Test with object detected
            test_object = ('chair', 100, 100, 200, 200)
            decision = engine.make_navigation_decision(test_object, mock_depth, None)
            
            print(f"✓ Decision engine working")
            print(f"  Decision made: {decision.get('action')}")
            print(f"  Confidence: {decision.get('confidence')}")
            
            # Test without object
            decision2 = engine.make_navigation_decision(None, mock_depth, None)
            print(f"  No object decision: {decision2.get('action')}")
            
            return True
        
        except Exception as e:
            print(f"✗ Decision engine error: {e}")
            return False
    
    @staticmethod
    def test_environment_mapper():
        """Test environment mapping"""
        print("\n" + "="*60)
        print("ENVIRONMENT MAPPER DIAGNOSTICS")
        print("="*60)
        
        try:
            from environment_mapper import EnvironmentMapper
            
            mapper = EnvironmentMapper()
            
            print("Testing environment mapping...")
            
            # Add test obstacle
            mapper.add_obstacle(100, 100, 200, 200, 'chair', 'CLOSE', 0.6)
            
            summary = mapper.get_environment_summary()
            print(f"✓ Environment mapper working")
            print(f"  Obstacles detected: {summary['total_obstacles_detected']}")
            print(f"  Obstacle types: {summary['obstacle_types']}")
            
            return True
        
        except Exception as e:
            print(f"✗ Environment mapper error: {e}")
            return False
    
    @staticmethod
    def run_all_tests():
        """Run all diagnostic tests"""
        print("\n" + "="*70)
        print(" "*15 + "INDOOR NAVIGATION SYSTEM DIAGNOSTICS")
        print("="*70)
        
        tests = [
            ("Camera", SystemDiagnostics.test_camera),
            ("Detection", SystemDiagnostics.test_detection),
            ("Depth", SystemDiagnostics.test_depth),
            ("Voice", SystemDiagnostics.test_voice),
            ("Obstacle Analyzer", SystemDiagnostics.test_obstacle_analyzer),
            ("Decision Engine", SystemDiagnostics.test_decision_engine),
            ("Environment Mapper", SystemDiagnostics.test_environment_mapper),
        ]
        
        results = []
        
        for name, test_func in tests:
            try:
                result = test_func()
                results.append((name, result))
            except Exception as e:
                print(f"\n✗ Unexpected error in {name}: {e}")
                results.append((name, False))
        
        # Summary
        print("\n" + "="*70)
        print("DIAGNOSTIC SUMMARY")
        print("="*70)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for name, result in results:
            status = "✓ PASS" if result else "✗ FAIL"
            print(f"{status}: {name}")
        
        print("="*70)
        print(f"Result: {passed}/{total} tests passed")
        
        if passed == total:
            print("✓ System is ready to use!")
        else:
            print("✗ Some components need attention. See errors above.")
        
        print("="*70 + "\n")
        
        return passed == total


def main():
    """Run diagnostic tests"""
    SystemDiagnostics.run_all_tests()


if __name__ == "__main__":
    main()
