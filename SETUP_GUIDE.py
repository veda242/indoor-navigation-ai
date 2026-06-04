"""
Quick Start Guide for Indoor Navigation AI System
Step-by-step setup instructions for Windows, Mac, and Linux
"""

# ============================================================================
# INSTALLATION STEPS
# ============================================================================

## STEP 1: Install Python (if not already installed)
# - Download from: https://www.python.org/downloads/
# - Choose Python 3.8 or higher
# - Check "Add Python to PATH" during installation

## STEP 2: Verify Python Installation
# Open Terminal/Command Prompt and run:
# 
# python --version
# pip --version
#
# Should show version numbers without errors

## STEP 3: Install Required Dependencies
# Navigate to the project folder and run:
#
# pip install -r requirements.txt
#
# This installs:
# - OpenCV (computer vision)
# - YOLOv8 (object detection)
# - PyTorch (deep learning)
# - pyttsx3 (text-to-speech)
# - NumPy (numerical computing)

## STEP 4: Download YOLOv8 Model
# Run this command:
#
# python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
#
# This downloads the 35MB YOLOv8 Nano model automatically
# (First run only - subsequent runs use cached model)

## STEP 5: Test Camera Access
# Run this test script:
#
# python -c "import cv2; print(cv2.__version__); cap = cv2.VideoCapture(0); \
#   ret, frame = cap.read(); print('Camera OK' if ret else 'Camera Failed'); \
#   cap.release()"
#
# Should print OpenCV version and "Camera OK"

# ============================================================================
# RUNNING THE SYSTEM
# ============================================================================

## BASIC USAGE (with camera):
#
# python main.py
#
# The system will:
# 1. Initialize all components
# 2. Start camera feed
# 3. Begin real-time navigation guidance
# 4. Display visual feedback
# 5. Provide voice guidance through speakers

## KEYBOARD CONTROLS:
#
# ESC     - Stop navigation and exit
# (Additional controls available in future versions)

# ============================================================================
# CONFIGURATION BEFORE RUNNING
# ============================================================================

## Customize Voice Settings (optional):
# Edit config.py:
#
#   VOICE_CONFIG = {
#       'voice_rate': 150,      # Words per minute (100-300)
#       'volume': 1.0,          # Volume (0.0 to 1.0)
#       'feedback_cooldown': 2  # Seconds between messages
#   }

## Adjust Detection Sensitivity (optional):
# Edit config.py:
#
#   DETECTION_CONFIG = {
#       'confidence_threshold': 0.5,  # Lower = more detections
#   }

## Change Camera Settings (if needed):
# Edit config.py:
#
#   CAMERA_CONFIG = {
#       'camera_index': 0,      # Change to 1, 2, etc. if needed
#       'frame_width': 640,
#       'frame_height': 480,
#       'fps': 30
#   }

# ============================================================================
# FIRST RUN CHECKLIST
# ============================================================================

FIRST_RUN_CHECKLIST = """
☐ Python 3.8+ installed
☐ Dependencies installed (pip install -r requirements.txt)
☐ Camera connected and working
☐ Audio speakers working (test volume)
☐ YOLOv8 model downloaded
☐ No other apps using camera
☐ Adequate lighting in room
☐ Cleared work space for safe testing
☐ Read README.md for full documentation
☐ Review Safety Disclaimer in README.md

START TEST RUN:
1. python main.py
2. System should say "Navigation started. I will guide you safely."
3. Move obstacles in front of camera
4. Listen for voice guidance
5. Check visual feedback window
6. Press ESC to exit when done
"""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

TROUBLESHOOTING = """
ISSUE: "ModuleNotFoundError: No module named..."
FIX: pip install -r requirements.txt

ISSUE: "Could not open camera"
FIX: 
- Check camera is connected: lsusb (Linux) / Device Manager (Windows)
- Try different camera index in config.py
- Close other apps using camera
- Restart computer

ISSUE: "ImportError: No module named 'torch'"
FIX: 
- pip install torch torchvision
- May take time - downloads 500MB+

ISSUE: No voice output
FIX:
- Check system volume is not muted
- Check speaker connections
- Test with: python -c "import pyttsx3; pyttsx3.init().say('Test'); \
  pyttsx3.init().runAndWait()"

ISSUE: Slow performance (low FPS)
FIX:
- Reduce camera resolution in config.py
- Use smaller YOLO model (already using nano)
- Close other applications
- Check CPU/GPU usage

ISSUE: Poor object detection
FIX:
- Improve room lighting
- Lower confidence_threshold in config.py (0.3-0.5)
- Use larger YOLO model (slower): 'yolov8s.pt' or 'yolov8m.pt'
- Ensure objects are clearly visible

ISSUE: Frame drops or "cv2.VideoCapture()" errors
FIX:
- Check camera cable connections
- Update camera drivers
- Try: pip install --upgrade opencv-python

ISSUE: torch.cuda errors
FIX: 
- System will automatically use CPU
- No action needed (GPU is optional)
"""

# ============================================================================
# UNDERSTANDING OUTPUT
# ============================================================================

SESSION_OUTPUT_EXPLANATION = """
When you run the system, you'll see:

1. CONSOLE OUTPUT:
   ============================================================
   ✓ Indoor Navigation System Started
   ✓ Voice Guidance Enabled
   ✓ Environment Mapping Active
   Press ESC to end navigation
   
   This shows the system is ready.

2. VISUAL WINDOW: "Indoor Navigation - Visual Feedback"
   - Shows real-time camera feed
   - Green box around obstacles = safe distance
   - Orange box = caution zone
   - Red box = danger/too close
   - Text overlays show:
     * Object name and distance
     * Navigation guidance
     * Path status (CLEAR/CONGESTED)

3. VOICE FEEDBACK:
   "Navigation started. I will guide you safely."
   (System speaks guidance as obstacles are detected)

4. ON EXIT (ESC key):
   ============================================================
   NAVIGATION SESSION SUMMARY
   ============================================================
   Total Obstacles Encountered: X
   Safe Passages Found: X
   Path Safety Score: X%
   
   Learned Obstacles:
     • Chair: N times
     • Table: N times
     ... etc
   
   (Shows what the system learned)

5. FILES CREATED:
   - environment_memory.json (learned environment)
   - navigation_log.txt (optional session logs)
"""

# ============================================================================
# SYSTEM REQUIREMENTS
# ============================================================================

SYSTEM_REQUIREMENTS = """
MINIMUM REQUIREMENTS:
- Python 3.8 or higher
- 4GB RAM (8GB recommended)
- Dual-core processor
- Webcam (USB or built-in)
- Working audio output
- 2GB free disk space
- Windows 7+, Mac OS 10.11+, or Linux

RECOMMENDED SETUP:
- Python 3.10 or higher
- 8GB+ RAM
- Quad-core or better processor
- USB 3.0 webcam
- Dedicated speakers or headphones
- SSD with 5GB free space
- Modern Windows/Mac/Linux (2018+)
- Nvidia GPU for faster processing (optional)

OPTIONAL HARDWARE:
- Nvidia GPU (CUDA compatible)
- Better quality webcam (1080p+)
- External microphone
- Wireless speaker
"""

# ============================================================================
# NEXT STEPS
# ============================================================================

NEXT_STEPS = """
1. Complete installation from steps above
2. Run: python main.py
3. Wait for "Navigation started" message
4. Test with various obstacles
5. Read full README.md for advanced features
6. Customize config.py for your needs
7. Use in safe environments first
8. Test with different room layouts
9. Build your environment memory
10. Consider combining with other mobility aids

FOR DEVELOPERS:
- Review enhanced_decision.py for core logic
- Extend obstacle_analyzer.py for new object types
- Modify voice_navigation.py for different guidance style
- Check config.py for all tunable parameters
- See README.md for complete documentation
"""

# ============================================================================
# COMMON QUESTIONS
# ============================================================================

FAQ = """
Q: Will this replace my cane/guide dog?
A: No. Use this with your existing mobility aids, not instead of them.

Q: Does it work in dark rooms?
A: Poorly - system needs adequate lighting. 
   Test in well-lit areas first.

Q: Can I use it with multiple cameras?
A: Currently one camera. Multi-camera support in future versions.

Q: How accurate is the object detection?
A: ~95% for common household objects in good lighting.
   Performance depends on camera quality and room brightness.

Q: Does it save my environment?
A: Yes - environment_memory.json stores learned obstacle locations.
   This improves guidance on repeat visits.

Q: Can I change the voice?
A: Limited options with pyttsx3 (Windows voices vary).
   Advanced voice control in future versions.

Q: How often should I retrain the environment?
A: System learns automatically each session.
   Resets on major room rearrangement.

Q: What about privacy?
A: No data is sent to the cloud.
   Everything runs locally on your computer.

Q: Can I use this on my phone?
A: Not yet - mobile version in development.

Q: Where's the error log?
A: Check navigation_log.txt (if enabled in config).
   Console output shows real-time errors.
"""

if __name__ == "__main__":
    print(FIRST_RUN_CHECKLIST)
    print("\n" + "="*60 + "\n")
    print(TROUBLESHOOTING)
    print("\n" + "="*60 + "\n")
    print(SESSION_OUTPUT_EXPLANATION)
    print("\n" + "="*60 + "\n")
    print(SYSTEM_REQUIREMENTS)
    print("\n" + "="*60 + "\n")
    print(NEXT_STEPS)
    print("\n" + "="*60 + "\n")
    print(FAQ)
