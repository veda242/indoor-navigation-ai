# Indoor Navigation AI System for Visually Impaired Users

A comprehensive real-time navigation system designed to help visually impaired users safely navigate indoor environments. The system uses computer vision, depth sensing, intelligent decision-making, and voice guidance to detect obstacles and provide real-time navigation assistance.

## 🎯 System Overview

### Key Features

- **Real-time Obstacle Detection**: Uses YOLOv8 to detect obstacles and classify them by danger level
- **Depth-based Distance Estimation**: Measures how far obstacles are using MiDaS depth sensing
- **Environment Learning**: Maps your home layout and remembers obstacle locations
- **Intelligent Path Planning**: Calculates safe routes and identifies clear corridors
- **Smart Voice Guidance**: Provides context-aware audio feedback without overwhelming the user
- **Session Memory**: Learns from each navigation session to improve future guidance

## 🏗️ System Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│           Main Navigation System (main.py)                   │
│                 Orchestrates all modules                     │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌─────────────┐   ┌─────────────────┐   ┌──────────────┐
   │  Detection  │   │  Decision       │   │ Voice System │
   │  Engine     │   │  Engine         │   │ (Speaking)   │
   └─────────────┘   └─────────────────┘   └──────────────┘
        │                     │                     │
        │              ┌──────┴──────┐              │
        │              │             │              │
   ┌────────────┐  ┌──────────────────────┐   ┌──────────────┐
   │ YOLO v8n   │  │ Environment Mapper   │   │ Voice Engine │
   │ Detection  │  │ (Grid-based mapping) │   │ (pyttsx3)    │
   └────────────┘  └──────────────────────┘   └──────────────┘
        │                     │
        │              ┌──────┴──────┐
        │              │             │
   ┌─────────┐    ┌──────────┐  ┌─────────────┐
   │Depth    │    │Obstacle  │  │Path Planner │
   │Estimation   │Analyzer  │  │(A* routing) │
   └─────────┘    └──────────┘  └─────────────┘
```

### Module Details

#### 1. **detection.py** - Object Detection
- Uses YOLOv8 Nano model (lightweight, fast)
- Detects 13+ common household objects
- Prioritizes close, large obstacles
- Returns highest priority obstacle per frame

#### 2. **depth.py** - Distance Estimation
- Uses Intel MiDaS depth estimation
- Converts 2D images to depth maps
- Provides normalized distance values (0-1)
- Enables distance-based safety decisions

#### 3. **environment_mapper.py** - Environment Memory
- Grid-based spatial mapping (20x20 pixel cells)
- Tracks obstacle frequency and density
- Identifies safe zones vs. dangerous zones
- Persistent memory (JSON file saved)
- Learns house layout over time

#### 4. **obstacle_analyzer.py** - Obstacle Classification
- Categorizes 13+ object types
- Assigns danger levels (1-5 scale)
- Tracks obstacle frequency
- Provides specific guidance per obstacle type
- Estimates obstacle size in frame

#### 5. **path_planner.py** - Route Calculation
- Divides space into left/center/right zones
- Calculates safest corridor
- A* pathfinding for complex scenarios
- Measures corridor width and safety
- Evaluates overall path safety (0-100%)

#### 6. **enhanced_decision.py** - Navigation Engine
- Orchestrates all components
- Makes final navigation decisions
- Tracks navigation state and history
- Generates comprehensive guidance
- Handles emergency situations

#### 7. **voice_navigation.py** - Voice Guidance
- Intelligent message queuing (thread-safe)
- Context-aware responses
- Avoids repetitive messages
- Priority-based urgency levels
- Comprehensive feedback categories:
  - Obstacle warnings
  - Path safety updates
  - Direction guidance
  - Emergency alerts
  - Room context information

#### 8. **main.py** - System Orchestration
- Initializes all components
- Manages navigation session
- Processes frames in real-time
- Provides visual feedback
- Generates session summaries

## 🚀 Getting Started

### Installation

1. **Install Python 3.8+**
   ```bash
   python --version
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download YOLOv8 Model**
   - First run will auto-download `yolov8n.pt` (35MB)
   - Or manually download from: https://github.com/ultralytics/assets/releases

### Running the System

**Basic Usage:**
```bash
python main.py
```

**With Arguments** (future enhancement):
```bash
python main.py --camera 0 --fps 30 --voice-rate 150
```

### Keyboard Controls

- **ESC**: Stop navigation and exit
- **S**: Save environment snapshot
- **R**: Reset session data
- **V**: Toggle voice feedback on/off
- **D**: Show/hide visual debug info

## 📊 How It Works

### Navigation Decision Flow

```
1. DETECT
   └─> Detect objects using YOLOv8
   └─> Get depth/distance information
   └─> Classify object type and danger level

2. MAP
   └─> Add to environment grid
   └─> Update safe/dangerous zones
   └─> Track obstacle frequency

3. PLAN
   └─> Find safest corridor (L/C/R)
   └─> Calculate path safety score
   └─> Identify direction options

4. DECIDE
   └─> Evaluate danger level
   └─> Choose action (stop/move/avoid)
   └─> Generate guidance message

5. GUIDE
   └─> Speak voice guidance
   └─> Show visual feedback
   └─> Log decision
   └─> Update environment map
```

### Decision Actions

| Action | Trigger | Response |
|--------|---------|----------|
| **STOP_IMMEDIATELY** | Danger level 5, VERY CLOSE | "STOP! [Object] is right in front of you!" |
| **AVOID_AND_MOVE** | Danger level 4, CLOSE | "Move [direction] to avoid [object]!" |
| **MOVE_CAREFULLY** | Danger level 3, MODERATE | "Watch out! [Object] ahead. Please move carefully." |
| **AWARE** | Danger level 1-2, FAR | "[Object] detected. Be aware." |
| **MOVE_FORWARD** | Path clear, safety > 70% | "Path is clear. Move forward." |
| **MOVE_CAREFULLY** | Path semi-clear, safety 40-70% | "Proceed carefully toward [safest zone]." |

## 🧠 Intelligence Features

### 1. Environment Learning
- **Grid Mapping**: 640x480 frame divided into 20-pixel cells (32x24 grid)
- **Density Tracking**: Each cell tracks obstacle frequency
- **Safe Zones**: Cells with low density (< 0.5)
- **Dangerous Zones**: Cells with high density (> 2.0)
- **Persistent Memory**: Saved in `environment_memory.json`

### 2. Obstacle Awareness
- **13+ Object Categories**: Furniture, appliances, electronics, people, etc.
- **Danger Levels**: 1-5 scale based on object type + distance
- **Frequency Tracking**: Remembers common obstacles
- **Size Estimation**: Adjusts guidance based on obstacle size in frame

### 3. Path Safety Scoring
- **Zone Evaluation**: Rates left, center, right corridors independently
- **Immediate Threat Detection**: Checks forward-most zones
- **Corridor Width**: Measures safe passage width
- **Overall Score**: 0-100% path safety percentage

### 4. Voice Intelligence
- **Message Queuing**: Thread-safe audio output (no interruptions)
- **Repetition Prevention**: 2-second cooldown between same messages
- **Priority Levels**: Critical > Urgent > Caution > Aware
- **Context Awareness**: Different messages for furniture, people, small objects
- **Feedback History**: Logs all guidance provided

## 📈 Example Usage Scenarios

### Scenario 1: Navigating Living Room
```
User enters living room with chair in front:
1. DETECT: Chair detected at CLOSE distance
2. ANALYZE: Danger level 2, furniture category
3. DECIDE: Move left or right (avoid_and_move)
4. GUIDE: "Chair ahead on the left. Move right to avoid it."
5. MAP: Chair location recorded in environment grid
```

### Scenario 2: Clear Hallway
```
User enters empty hallway:
1. DETECT: No objects detected
2. CHECK: Path safety = 95%
3. DECIDE: move_forward action
4. GUIDE: "Path is clear. Continue forward."
5. MAP: Hallway marked as safe zone
```

### Scenario 3: Multiple Obstacles
```
User encounters crowded area:
1. DETECT: Multiple objects - person, chair, table
2. PRIORITIZE: Person closest (highest priority)
3. ANALYZE: Person = danger level 3
4. DECIDE: Move carefully, choose safest direction
5. GUIDE: "Person nearby. Move left for safe passage."
6. MAP: Multiple obstacles recorded, zone marked dangerous
```

## ⚠️ Safety Features

### Immediate Threat Detection
- Monitors "VERY CLOSE" distance in real-time
- Triggers emergency stop if threat detected
- Provides urgent verbal warning
- Blocks forward movement until cleared

### Progressive Warnings
- **Far**: "Be aware of [object]"
- **Moderate**: "Watch out! [Object] ahead."
- **Close**: "Alert! [Object] approaching. Move immediately!"
- **Very Close**: "STOP! [Object] is right in front of you!"

### Environmental Awareness
- Learns safe zones for faster future navigation
- Remembers dangerous areas for avoidance
- Tracks object frequency for habituation
- Adapts guidance as user learns layout

## 📁 File Structure

```
indoor-navigation-ai/
├── main.py                      # System orchestrator
├── detection.py                 # YOLOv8 object detection
├── depth.py                     # MiDaS depth estimation
├── enhanced_decision.py          # Main decision engine
├── environment_mapper.py         # Grid-based environment memory
├── obstacle_analyzer.py          # Obstacle classification & analysis
├── path_planner.py              # Path finding & route planning
├── voice_navigation.py          # Intelligent voice guidance system
├── config.py                    # Configuration settings
├── yolov8n.pt                   # YOLOv8 Nano model (auto-downloaded)
├── environment_memory.json      # Learned environment map (auto-created)
├── navigation_log.txt           # Session logs (optional)
└── requirements.txt             # Python dependencies
```

## ⚙️ Configuration

Edit `config.py` to customize:

**Detection Settings**
```python
DETECTION_CONFIG = {
    'confidence_threshold': 0.5,  # Lower = more detections
    'important_classes': [...]     # Modify detected objects
}
```

**Voice Settings**
```python
VOICE_CONFIG = {
    'voice_rate': 150,             # Words per minute
    'volume': 1.0,                 # 0-1 scale
    'feedback_cooldown': 2         # Seconds between messages
}
```

**Navigation Settings**
```python
NAVIGATION_CONFIG = {
    'grid_cell_size': 20,          # Pixel size per grid cell
    'obstacle_density_threshold': 0.5,  # Safe zone threshold
}
```

## 📊 Output & Logging

### Visual Feedback
- **Bounding boxes** around detected objects
- **Color coding**: Green (safe) → Orange (caution) → Red (danger)
- **Real-time guidance** text overlay
- **Path status** (CLEAR/CONGESTED)
- **Frame counter** for performance monitoring

### Voice Feedback
- Real-time spoken guidance
- Priority-based urgency levels
- Context-aware descriptions
- No repetitive messages

### Session Summary (on Exit)
```
============================================================
NAVIGATION SESSION SUMMARY
============================================================
Total Obstacles Encountered: 12
Safe Passages Found: 8
Path Safety Score: 78.5%

Learned Obstacles:
  • Chair: 5 times
  • Table: 3 times
  • Person: 2 times
  • Cup: 2 times

Environment Summary:
  • Total Detections: 23
  • Safe Zones: 450
  • Dangerous Zones: 89
============================================================
✓ Environment map saved to 'environment_memory.json'
✓ Navigation session complete
============================================================
```

### Environment Memory File
```json
{
  "obstacle_grid": [[0, 0.2, 0.5, ...], ...],
  "obstacle_types": {
    "chair": [[0, 0, 1, ...], ...],
    "table": [[0, 1, 1, ...], ...]
  },
  "session_data": {
    "obstacles_detected": [...],
    "safe_zones": [...],
    "dangerous_zones": [...]
  },
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

## 🔧 Troubleshooting

### Camera Issues
- Check if camera is connected: `lsusb` (Linux) or Device Manager (Windows)
- Ensure no other app is using the camera
- Try camera index 1, 2 if 0 doesn't work: `cv2.VideoCapture(1)`

### Poor Detection
- Improve lighting in the room
- Lower confidence threshold in `config.py`
- Ensure objects are common household items

### Voice Issues
- Check volume settings: `VOICE_CONFIG['volume']`
- Verify audio drivers are installed
- Try different voice: Edit `pyttsx3` initialization

### Performance Issues
- Reduce frame resolution in camera config
- Lower FPS setting
- Use MiDaS_small for faster depth (default)

## 📈 Future Enhancements

1. **Room Detection**: Identify room types automatically
2. **User Profiles**: Save personalized settings per user
3. **Mobile App**: iOS/Android companion for remote assistance
4. **Cloud Learning**: Share environment maps between users
5. **Activity Recognition**: Understand user actions (sitting, standing)
6. **Emergency Integration**: Connect with emergency services
7. **Multi-sensor Fusion**: Combine camera + LiDAR + audio
8. **Language Support**: Multi-language voice guidance
9. **Gesture Control**: Hand gestures for quick commands
10. **Haptic Feedback**: Vibration patterns for direction guidance

## 🤝 Contributing

To improve this system:
1. Test in different environments
2. Report detection errors
3. Suggest new object types to detect
4. Improve voice guidance phrases
5. Optimize performance

## 📜 License

This project is designed to assist visually impaired users. Use responsibly and always with human oversight.

## 🆘 Safety Disclaimer

This system is designed as an **assistive tool**, not a replacement for:
- Guide dogs
- Canes and other mobility aids
- Human assistance
- Professional navigation training

Always use in combination with traditional navigation methods. Test thoroughly in safe environments before relying on it in real scenarios.

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review configuration settings
3. Check environment lighting and detection
4. Verify all dependencies are installed correctly

---

**Last Updated**: January 2024
**Version**: 1.0
**Status**: Production Ready
