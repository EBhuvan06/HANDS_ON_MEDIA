# MPV Gesture Control v2.0 - User Guide
## Invalid Gesture Detection with Interactive Help System

**Last Updated:** February 19, 2026  
**Version:** 2.0 (Smart Help System)  
**Hardware:** VVDN-JN-NN (Jetson Nano 4GB)  
**Software:** TensorFlow Lite + MediaPipe + OpenCV  
**Status:** Production Ready ✅

---

## 📋 Table of Contents

1. [What's New in v2.0](#whats-new-in-v20)
2. [Quick Start Guide](#quick-start-guide)
3. [Invalid Gesture Detection System](#invalid-gesture-detection-system)
4. [Interactive Help Menu](#interactive-help-menu)
5. [The 8 Gesture Commands](#the-8-gesture-commands)
6. [Smart Cooldown System](#smart-cooldown-system)
7. [Interface Overview](#interface-overview)
8. [Usage Examples](#usage-examples)
9. [Performance Metrics](#performance-metrics)
10. [Troubleshooting](#troubleshooting)

---

## What's New in v2.0

### 🎯 Invalid Gesture Detection
**Automatically detects unclear or incorrect hand gestures**

- **Real-time monitoring:** Tracks gesture confidence levels
- **Smart threshold:** Detects when confidence falls below 65%
- **Counter system:** Keeps track of invalid gestures
- **Immediate feedback:** Visual warning when gesture unclear

### 📋 Interactive Help Menu
**Auto-displays gesture guide when you need it**

- **Automatic trigger:** Shows when invalid gesture detected
- **Complete reference:** All 8 gestures with hand requirements
- **Timed display:** Shows for 5 seconds, then auto-dismisses
- **Learning-friendly:** Helps you correct mistakes in real-time

### ⚡ Smart Per-Gesture Cooldown
**Different cooldown times for different actions**

- **Fast actions:** 0.3-0.4s for volume & seeking
- **Medium actions:** 1.5s for play/pause
- **Slow actions:** 2.0-3.0s for playlist navigation
- **Adaptive:** Adjusts based on gesture confidence

### 🎨 Enhanced Visual Feedback
**Better on-screen information**

- **Color-coded confidence:** Green/Yellow/Orange boxes
- **Real-time stats:** FPS, latency, command success rate
- **Action history:** Last 5 gestures executed
- **Invalid count:** Track how many unclear gestures made

---

## Quick Start Guide

### Step 1: Start MPV Media Player

```bash
# Terminal 1
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf your_video.mp4
```

### Step 2: Enable Performance Mode

```bash
# Terminal 2
cd ~/hands_on_gesture
sudo nvpmodel -m 0
sudo jetson_clocks
```

### Step 3: Start Gesture Control v2.0

```bash
python3 version_2.py
```

### Expected Startup Output

```
======================================================================
MPV GESTURE CONTROL - VERSION 1.0 (Enhanced)
Smart Cooldown + Invalid Gesture Detection + No Mirror
======================================================================

[STEP 1] Checking MPV connection...
[+] MPV connected!

[STEP 2] Loading TFLite model...
[+] TFLite model loaded!

[STEP 3] Loading gesture labels...
[+] Loaded 9 valid gestures

[STEP 4] Initializing smart cooldown system...
[+] Per-gesture cooldowns configured

[STEP 5] Initializing hand detection...
[libprotobuf WARNING external/com_google_protobuf/src/google/protobuf/text_format.cc:324] Warning parsing text-format mediapipe.CalculatorGraphConfig: 125:5: text format contains deprecated field "use_gpu"
WARNING: Logging before InitGoogleLogging() is written to STDERR
I20260219 17:00:12.111609  8911 gl_context_egl.cc:163] Successfully initialized EGL. Major : 1 Minor: 5
I20260219 17:00:12.320807  8951 gl_context.cc:331] GL version: 3.2 (OpenGL ES 3.2 NVIDIA 32.6.1)
I20260219 17:00:12.321201  8911 gl_context_egl.cc:163] Successfully initialized EGL. Major : 1 Minor: 5
I20260219 17:00:12.416904  8952 gl_context.cc:331] GL version: 3.2 (OpenGL ES 3.2 NVIDIA 32.6.1)
[+] MediaPipe initialized!

[STEP 6] Opening camera...
W20260219 17:00:12.463513  8951 tflite_model_loader.cc:32] Trying to resolve path manually as GetResourceContents failed: ; Can't find file: mediapipe/modules/palm_detection/palm_detection.tflite
INFO: Created TensorFlow Lite delegate for GPU.
[+] Camera ready! (No mirror mode)
[*] Camera FPS: 30 | Resolution: 640x480

======================================================================
SYSTEM READY - VERSION 1.0 (Enhanced)
======================================================================

[FEATURES]
  - Smart per-gesture cooldown
  - Invalid gesture detection with help
  - No mirror image (natural view)
  - Fast volume/skip controls

[*] Press 'q' to quit
======================================================================
```

**Camera window opens - System ready!**

---

## Invalid Gesture Detection System

### How It Works

The system continuously monitors the **confidence level** of your hand gestures:

**Confidence Thresholds:**
```
Gesture Confidence >= 70%  → VALID (executes command)
Gesture Confidence 65-70%  → LOW CONFIDENCE (warning)
Gesture Confidence < 65%   → INVALID (help menu shows)
```

### What Triggers Invalid Detection?

**Common Causes:**

1. **Unclear Hand Position**
   - Fingers not fully extended or closed
   - Hand at awkward angle
   - Partial hand visibility

2. **Wrong Hand Used**
   - Using RIGHT hand for SKIP_RIGHT (needs LEFT)
   - Using LEFT hand for PREVIOUS (needs RIGHT)

3. **Poor Lighting**
   - Shadows obscuring fingers
   - Backlit setup (light behind you)
   - Dim environment

4. **Movement During Gesture**
   - Hand shaking or trembling
   - Transitioning between gestures
   - Not holding steady

5. **Ambiguous Form**
   - Between two gesture positions
   - Doesn't match any trained gesture clearly

### Invalid Gesture Counter

**Displayed in Help Menu:**
```
Invalid gestures: 5
```

- Increments each time invalid gesture detected
- Resets when you exit program
- Shows in final performance report

### Benefits of Invalid Detection

✅ **Learning Tool:** Helps you understand what went wrong  
✅ **Quick Reference:** Shows correct gestures immediately  
✅ **Improves Accuracy:** Encourages clearer hand positions  
✅ **Saves Time:** No guessing why gesture didn't work

---

## Interactive Help Menu

### When Does It Appear?

The help menu **automatically displays** when:
- Gesture confidence falls below 65%
- Hand is detected but unclear
- Invalid gesture counter increments

### What You'll See

**Phase 1: Gesture Guide Table (5 seconds)**

```
╔═══════════════════════════════════════════════════════════╗
║       PLEASE USE THESE GESTURES TO CONTROL                ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  # Gesture      Hand Position              Hand Required  ║
║  ─────────────────────────────────────────────────────────║
║  1 PLAY         Index & middle fingers up  Either         ║
║  2 PAUSE        Open palm                  Either         ║
║  3 VOLUME_UP    Index finger up            Either         ║
║  4 VOLUME_DOWN  Index finger down          Either         ║
║  5 SKIP_RIGHT   Thumb up + index,middle -->LEFT hand      ║
║  6 SKIP_LEFT    Thumb up + index,middle <--RIGHT hand     ║
║  7 NEXT         Thumb up + index -->       LEFT hand      ║
║  8 PREVIOUS     Thumb up + index <--       RIGHT hand     ║
║                                                           ║
║  Invalid gestures: 3  Make a valid gesture to continue... ║
╚═══════════════════════════════════════════════════════════╝
```

**Phase 2: Resume Message (2 seconds)**

```
╔═══════════════════════════╗
║                           ║
║  Great! Let's continue... ║
║                           ║
║  Show a valid gesture to  ║
║     control MPV           ║
║                           ║
╚═══════════════════════════╝
```

**Phase 3: Auto-Dismiss**
- Total display time: 7 seconds
- Returns to normal operation automatically
- Ready to recognize next gesture

### How to Use the Help Menu

**First-Time Users:**
1. Deliberately make an unclear gesture
2. Help menu appears automatically
3. Study the gesture table
4. Note hand requirements (LEFT/RIGHT/Either)
5. Practice each gesture one by one

**During Regular Use:**
1. Invalid gesture detected
2. Quick glance at help table
3. See which hand or position needed
4. Correct your gesture
5. Continue using system

**Learning Strategy:**
- Use help as quick reference guide
- Check "Hand Required" column carefully
- Practice gestures from table
- Build muscle memory over time

---

## The 8 Gesture Commands

### 1. PLAY ✌️

**Hand Position:** Index & middle fingers up  
**Hand Required:** Either  
**Cooldown:** 1.5 seconds

```
        INDEX and MIDDLE    (UP)
        RING PINKY          (folded/closed)
        THUMB               (down/tucked)
```

**Action:** Resume video playback  
**Tip:** Make a clear "V" shape with fingers separated

---

### 2. PAUSE ✋

**Hand Position:** Open palm  
**Hand Required:** Either  
**Cooldown:** 1.5 seconds

```
     All 5 fingers    (extended)   
     PALM FLAT
```

**Action:** Pause video playback  
**Tip:** Easiest gesture - spread fingers wide

---

### 3. VOLUME_UP 🔊

**Hand Position:** Index finger up  
**Hand Required:** Either  
**Cooldown:** 0.4 seconds

```
        INDEX              (straight UP)
        Other 4 fingers    (closed in fist)
        THUMB              (tucked in fist)
```

**Action:** Increase volume +5%  
**Tip:** Point straight up, hold for rapid increase

---

### 4. VOLUME_DOWN 🔉

**Hand Position:** Index finger down  
**Hand Required:** Either  
**Cooldown:** 0.4 seconds

```
        INDEX               (straight DOWN)
        Other 4 fingers      (closed in fist)
        THUMB                (tucked in fist)
       
```

**Action:** Decrease volume -5%  
**Tip:** Point straight down, hold for rapid decrease

---

### 5. SKIP_RIGHT ⏩

**Hand Position:** Thumb up + index,middle →  
**Hand Required:** LEFT hand ONLY ⚠️  
**Cooldown:** 0.3 seconds

```
        THUMB               (pointing UP)
        INDEX and MIDDLE    (pointing RIGHT →)
        LEFT HAND!          (Right hand WON'T work)
```

**Action:** Skip forward +5 seconds  
**Tip:** Use LEFT hand, 2 fingers pointing right

---

### 6. SKIP_LEFT ⏪

**Hand Position:** Thumb up + index,middle ←  
**Hand Required:** RIGHT hand ONLY ⚠️  
**Cooldown:** 0.3 seconds

```
        THUMB               (pointing UP)
        INDEX and MIDDLE    (pointing LEFT ←)
        RIGHT HAND!         (Left hand WON'T work)
```

**Action:** Skip backward -5 seconds  
**Tip:** Use RIGHT hand, 2 fingers pointing left

---

### 7. NEXT ⏭️

**Hand Position:** Thumb up + index →  
**Hand Required:** LEFT hand ONLY ⚠️  
**Cooldown:** 2.0 seconds

```
        THUMB            (pointing UP)
        INDEX finger     (pointing RIGHT → ONLY)
        MIDDLE finger    (CLOSED! - KEY!)
        LEFT HAND!       (Right hand WON'T work)
```

**Action:** Next playlist item  
**Tip:** Only 1 finger (index), not 2 like SKIP_RIGHT

---

### 8. PREVIOUS ⏮️

**Hand Position:** Thumb up + index ←  
**Hand Required:** RIGHT hand ONLY ⚠️  
**Cooldown:** 2.0 seconds

```
        THUMB            (pointing UP)
        INDEX finger     (pointing LEFT ← ONLY)
        MIDDLE finger    (CLOSED! - KEY!)
        RIGHT HAND!      (Left hand WON'T work)
```

**Action:** Previous playlist item  
**Tip:** Only 1 finger (index), not 2 like SKIP_LEFT

---

### Quick Reference Table

| # | Gesture | Hand Position | Hand | Cooldown | Action |
|---|---------|---------------|------|----------|--------|
| 1 | PLAY | Index & middle up | Either | 1.5s | Resume |
| 2 | PAUSE | Open palm | Either | 1.5s | Pause |
| 3 | VOLUME_UP | Index up | Either | 0.4s | +5% vol |
| 4 | VOLUME_DOWN | Index down | Either | 0.4s | -5% vol |
| 5 | SKIP_RIGHT | Thumb+2 fingers → | LEFT | 0.3s | +5s |
| 6 | SKIP_LEFT | Thumb+2 fingers ← | RIGHT | 0.3s | -5s |
| 7 | NEXT | Thumb+index → | LEFT | 2.0s | Next track |
| 8 | PREVIOUS | Thumb+index ← | RIGHT | 2.0s | Prev track |

---

## Smart Cooldown System

### What Are Cooldowns?

**Cooldowns prevent:**
- Accidental double-triggering
- Rapid repeated commands
- Unintended gesture spam

**How they work:**
- Each gesture has its own cooldown period
- After execution, that gesture is blocked temporarily
- Other gestures can execute immediately

### Cooldown Times

**Fast Actions (0.3-0.4s):**
```
SKIP_RIGHT:    0.3s  ← Fastest
SKIP_LEFT:     0.3s  ← Fastest
VOLUME_UP:     0.4s  ← Fast
VOLUME_DOWN:   0.4s  ← Fast
```
*Why fast?* Need rapid adjustment capability

**Medium Actions (1.5s):**
```
PLAY:          1.5s
PAUSE:         1.5s
```
*Why medium?* Prevent accidental toggle

**Slow Actions (2.0-3.0s):**
```
NEXT:          2.0s
PREVIOUS:      2.0s
STOP:          3.0s  ← Slowest
```
*Why slow?* Critical actions, prevent mistakes

### Confidence-Based Adjustment

**High Confidence (>95%):**
- Cooldown reduced by 10%
- Example: 1.5s → 1.35s
- Rewards clear gestures

**Low Confidence (70-80%):**
- Cooldown increased by 10%
- Example: 1.5s → 1.65s
- Prevents uncertain triggers

**Normal Confidence (80-95%):**
- Standard cooldown applies
- No adjustment

### Cooldown Display

**On Screen:**
```
┌─────────────────────┐
│  VOLUME_UP          │
│  95% | CD:0.4s <--- │ Cooldown shown here
└─────────────────────┘
```

**In Console:**
```
[ACTION] VOLUME_UP    | 95% | 2.3ms | 0.36s CD | Volume +5
                                        ↑
                              Actual cooldown used
```

---

## Interface Overview

### Main Display Elements

**Title Bar:**
```
MPV Control v2.0    FPS:25.3 Lat:42.5ms    MPV: 45/0
```
- Version number
- Real-time FPS
- Total latency
- MPV commands (success/failed)

**Current Gesture Box (when valid gesture detected):**
```
┌──────────────────────┐
│    VOLUME_UP         │ ← Gesture name
│    95% | CD:0.4s     │ ← Confidence | Cooldown
└──────────────────────┘
```

**Color Coding:**
- 🟢 **Green** (85-100%): High confidence - reliable
- 🟡 **Yellow** (70-85%): Medium confidence - good
- 🟠 **Orange** (<70%): Low confidence - may fail

**Recent Actions (bottom right):**
```
Recent:
  PAUSE (2s ago)
  VOLUME_UP (5s ago)
  PLAY (8s ago)
```

**Status Messages:**
```
"No hand"          ← No hand detected
"Multiple hands"   ← Multiple hands (use only one)
[Help Menu]        ← Invalid gesture detected
```

---

## Usage Examples

### Example 1: First-Time User

**Starting the System:**
```bash
# Terminal 1
mpv --input-ipc-server=/tmp/mpvsocket movie.mp4

# Terminal 2
cd ~/hands_on_gesture
sudo nvpmodel -m 0
sudo jetson_clocks
python3 version_2.py
```

**Learning Gestures:**
1. Camera window opens
2. Make an unclear gesture (testing)
3. **Help menu appears automatically**
4. Study the gesture table for 5 seconds
5. Help dismisses with "Let's continue..."
6. Try PAUSE (easiest - open palm)
7. See green box appear → Success!
8. Practice other gestures

**Console Output:**
```
[INVALID] Confidence: 58% | Count: 1 | Help displayed
(help shown for 7 seconds)
[ACTION] PAUSE        | 92% | 2.1ms | 1.5s CD | Pause
[ACTION] PLAY         | 88% | 2.3ms | 1.5s CD | Resume
```

### Example 2: Watching a Movie

**Scenario:** Watching a 2-hour movie

```
1. Movie starts playing
2. Too loud → VOLUME_DOWN gesture
   Hold for 1 second → Volume decreased
   
3. Want to pause → PAUSE gesture
   Open palm → Video pauses
   
4. Resume → PLAY gesture
   Peace sign → Video resumes
   
5. Skip intro (90 seconds):
   Use LEFT hand
   Make SKIP_RIGHT (thumb + 2 fingers →)
   HOLD for 6 seconds → Skips ~100 seconds
```

**Console Output:**
```
[ACTION] VOLUME_DOWN  | 94% | 2.3ms | 0.36s CD | Volume -5
[ACTION] VOLUME_DOWN  | 95% | 2.2ms | 0.36s CD | Volume -5
[ACTION] PAUSE        | 92% | 2.1ms | 1.5s CD | Pause
[ACTION] PLAY         | 88% | 2.3ms | 1.5s CD | Resume
[ACTION] SKIP_RIGHT   | 89% | 2.6ms | 0.3s CD | Seek +5s
[ACTION] SKIP_RIGHT   | 91% | 2.5ms | 0.3s CD | Seek +5s
... (repeats while held)
```

### Example 3: Playlist Navigation

**Scenario:** Music playlist with 20 songs

```
1. Current song not interesting
2. Use LEFT hand
3. NEXT gesture (thumb + 1 finger →)
4. Wait 2 seconds (cooldown)
5. Want previous song back
6. Use RIGHT hand
7. PREVIOUS gesture (thumb + 1 finger ←)
8. Song changes back
```

**Console Output:**
```
[ACTION] NEXT         | 86% | 3.2ms | 2.0s CD | Next playlist item
(2 second cooldown)
[ACTION] PREVIOUS     | 84% | 3.1ms | 2.0s CD | Previous playlist item
```

### Example 4: Invalid Gesture Recovery

**Scenario:** Accidentally make unclear gesture

```
1. Trying to make PLAY gesture
2. Fingers not separated enough
3. **Help menu appears**
4. Shows: "1 PLAY   Index & middle fingers up   Either"
5. Study requirement: fingers must be separated
6. Help dismisses after 7 seconds
7. Make corrected PLAY gesture
8. Success!
```

**What You See:**
```
[INVALID] Confidence: 62% | Count: 1 | Help displayed

[Help Menu Shows]
═══════════════════════════════════════
1 PLAY    Index & middle fingers up  Either
...
Invalid gestures: 1  Make a valid gesture...
═══════════════════════════════════════

[After 7 seconds]
Great! Let's continue...
Show a valid gesture to control MPV

[Back to normal]
[ACTION] PLAY         | 88% | 2.3ms | 1.5s CD | Resume
```

---

## Performance Metrics

### Real-Time Display

**On Screen (Top Right):**
```
FPS:25.3 Lat:42.5ms
MPV: 45/0
```

**Metrics Explained:**
- **FPS:** Frames per second (target: >20)
- **Lat:** Total latency in milliseconds (target: <150ms)
- **MPV:** Commands success/failed

### Console Output (Per Action)

```
[ACTION] PLAY | 88% | 2.3ms | 1.5s CD | Resume
         ↑      ↑      ↑       ↑        ↑
      Gesture  Conf  Exec   Cooldown  Result
```

### Final Report (on exit with 'q')

```
======================================================================
FINAL REPORT - VERSION 2.0 (Smart Help System)
======================================================================

[TIMING]
 FPS: 17.88
 Latency: 24.56ms
 Hand: 24.35ms | Inference: 0.20ms | Cmd: 4.31ms

[ACCURACY]
 Prediction Accuracy: 94.32%
 Commands Executed: 197
 Invalid Gestures: 11

[MPV]
 Success: 198 | Failed: 0

[COOLDOWN STATS]
 VOLUME_UP    CD:0.4s  Exec: 45  Rate: 97.8%
 VOLUME_DOWN  CD:0.4s  Exec: 32  Rate: 96.9%
 PLAY         CD:1.5s  Exec: 12  Rate: 92.3%
 PAUSE        CD:1.5s  Exec: 15  Rate: 93.8%
 SKIP_RIGHT   CD:0.3s  Exec: 18  Rate: 94.7%
 NEXT         CD:2.0s  Exec:  3  Rate: 100.0%
 PREVIOUS     CD:2.0s  Exec:  2  Rate: 100.0%

[INVALID GESTURES]
 Total Detected: 11
 Help Shown: 11 times
======================================================================
```

### Performance Targets

| Metric | Target | Good | Excellent |
|--------|--------|------|-----------|
| FPS | >20 | 25-30 | 30 |
| Latency | <150ms | 40-60ms | <40ms |
| Accuracy | >80% | 90-95% | >95% |

---

## Troubleshooting

### Issue: Help Menu Appearing Too Often

**Symptom:**
- Help menu shows repeatedly
- Hard to make valid gestures
- Most gestures <65% confidence

**Causes & Solutions:**

**1. Poor Lighting (Most Common)**
```
Problem: Shadows on hand, dim environment
Solution:
  - Add front lighting
  - Use natural daylight
  - Remove backlighting
  - Ensure >500 lux brightness
```

**2. Unclear Hand Positions**
```
Problem: Fingers not fully extended/closed
Solution:
  - Exaggerate gestures
  - Fully separate fingers for PLAY
  - Fully close fist for VOLUME gestures
  - Study help table carefully
```

**3. Wrong Hand Used**
```
Problem: Using wrong hand for directional gestures
Solution:
  - SKIP_RIGHT → Use LEFT hand
  - SKIP_LEFT → Use RIGHT hand
  - NEXT → Use LEFT hand
  - PREVIOUS → Use RIGHT hand
  (Check "Hand Required" in help table)
```

**4. Hand Too Close/Far**
```
Problem: Camera can't see hand properly
Solution:
  - Position hand 40-60cm from camera
  - Hand should fill 40-60% of frame
  - Keep entire hand visible
```

### Issue: Specific Gestures Always Invalid

**Symptom:**
- PAUSE works (95%+ confidence)
- But NEXT never works (<50% confidence)

**Explanation:**
- Simple gestures easier (PAUSE, PLAY)
- Complex gestures harder (NEXT, PREVIOUS, SKIP)

**Solutions:**

**1. Perfect Lighting for Complex Gestures**
```
- Very bright light
- No shadows between fingers
- Clear finger separation visible
```

**2. Exaggerated Positions**
```
For NEXT (thumb + 1 finger):
  - Thumb FULLY extended up
  - Index FULLY extended right
  - All other fingers TIGHTLY closed
  - Wide gap between thumb & index
```

**3. Direct Camera Angle**
```
- Camera faces palm directly
- Not shooting from side
- Fingers clearly separated in view
```

### Issue: Gestures Recognized But MPV Doesn't Respond

**Symptom:**
- Green boxes appear (valid gestures)
- But video doesn't pause/play
- Console shows [ACTION] lines

**Solution:**

**1. Check MPV Socket**
```bash
# Verify socket exists
ls -l /tmp/mpvsocket
# Should show: srw-rw-rw-

# If missing, restart MPV
pkill mpv
mpv --input-ipc-server=/tmp/mpvsocket video.mp4
```

**2. Restart Both Programs**
```bash
# Terminal 1
pkill python3

# Terminal 2  
pkill mpv
mpv --input-ipc-server=/tmp/mpvsocket video.mp4

# Terminal 1 (restart gesture control)
cd ~/hands_on_gesture
python3 version_2.py
```

### Issue: Low FPS (<15)

**Symptom:**
- FPS showing 10-14
- Jerky camera feed
- Slow gesture response

**Solutions:**

**1. Enable Performance Mode**
```bash
sudo nvpmodel -m 0
sudo jetson_clocks

# Verify
sudo nvpmodel -q
# Should show: MAXN
```

**2. Close Background Apps**
```bash
pkill chrome
pkill firefox
pkill code
```

**3. Check Temperature**
```bash
cat /sys/devices/virtual/thermal/thermal_zone0/temp
# Divide by 1000 = temperature in °C
# Should be <60°C

# If too hot:
- Check fan working
- Reduce ambient temperature
- Wait for cooldown
```

### Issue: Invalid Count Keeps Increasing

**Symptom:**
- Invalid gesture count at 20, 30, 50+
- Even valid gestures sometimes counted as invalid

**Possible Causes:**

**1. Threshold Too Strict**
```python
# Check configuration in version_2.py
INVALID_GESTURE_THRESHOLD = 0.65

# If too many invalids, increase to:
INVALID_GESTURE_THRESHOLD = 0.60  # More forgiving
```

**2. Lighting Inconsistent**
```
- Light flickering
- Moving shadows
- Changing brightness
Solution: Use steady, constant light source
```

**3. Hand Position Drifting**
```
- Hand slowly moving out of frame
- Distance changing
- Angle shifting
Solution: Keep hand in same position, 40-60cm
```

---

## Tips for Best Results

### Lighting Setup

**✅ Ideal:**
- Bright, even illumination (>500 lux)
- Light source in front of you
- No harsh shadows on hand
- Natural daylight best

**❌ Avoid:**
- Backlighting (light behind you)
- Dim rooms (<200 lux)
- Strong directional shadows
- Flickering fluorescent lights

### Camera Positioning

**Optimal:**
- **Distance:** 40-60cm from camera
- **Fill:** Hand fills 40-60% of frame
- **Angle:** Face palm directly at camera
- **Height:** Camera at chest level

### Gesture Technique

**The 3-Step Process:**

1. **Position** (0.2s):
   - Bring hand to center of frame
   - Ensure camera sees entire hand

2. **Form** (0.3s):
   - Make gesture clearly
   - Fully extend or close fingers
   - Check correct hand (left/right)

3. **Hold** (0.5-1.0s):
   - Stay completely still
   - Wait for recognition
   - See gesture box appear

**Total:** ~1-1.5 seconds per gesture

### Learning Strategy

**Week 1: Master Simple Gestures**
- Practice PAUSE (easiest)
- Practice PLAY
- Practice VOLUME_UP/DOWN
- Get 95%+ confidence consistently

**Week 2: Add Complex Gestures**
- Practice SKIP_RIGHT (LEFT hand)
- Practice SKIP_LEFT (RIGHT hand)
- Remember hand requirements

**Week 3: Full Control**
- Add NEXT and PREVIOUS
- Practice transitions
- Build speed

---

## Quick Reference Card

### Gesture Summary

```
┌──────────────────────────────────────────────────┐
│              GESTURE REFERENCE                   │
├──────────────────────────────────────────────────┤
│ PLAY         ✌️   Index+middle up     Either     │
│ PAUSE        ✋   Open palm           Either     │
│ VOLUME_UP    ☝️   Index up            Either     │
│ VOLUME_DOWN  👇   Index down          Either     │
│ SKIP_RIGHT   👍➡️  Thumb+2 fingers →   LEFT     │
│ SKIP_LEFT    ⬅️👍  Thumb+2 fingers ←   RIGHT    │
│ NEXT         👍➡️  Thumb+index →       LEFT     │
│ PREVIOUS     ⬅️👍  Thumb+index ←       RIGHT    │
├───────────────────────────────────────────────────┤
│ Tip: Hold 0.5+ sec | Good light | Correct hand    │
│ Help: Make unclear gesture → Guide appears        │
└───────────────────────────────────────────────────┘
```

### Daily Startup

```bash
# Every time before using:
cd ~/hands_on_gesture
sudo nvpmodel -m 0
sudo jetson_clocks
python3 version_2.py
```

### Emergency Reset

```bash
# If system hangs:
pkill python3
pkill mpv

# Restart everything:
mpv --input-ipc-server=/tmp/mpvsocket video.mp4 &
cd ~/hands_on_gesture && python3 version_2.py
```

---

## Summary

### What You Get

**Features:**
- 8 hand gestures for complete media control
- Invalid gesture detection with counter
- Auto-displaying help menu
- Smart per-gesture cooldowns
- Real-time confidence feedback
- 100% offline, touchless operation

**Performance:**
- 20-30 FPS (smooth)
- 40-60ms latency (fast)
- 90-95% accuracy (reliable)
- Learning-friendly help system

**Requirements:**
- Good lighting
- Clear hand positions
- 0.5+ second hold
- Correct hand (left/right/either)

---

**Version:** 2.0  
**Date:** February 19, 2026  
**Status:** Production Ready   
**Feature:** Invalid Gesture Detection with Interactive Help Menu

**For setup instructions, see:** SETUP_GUIDE_V2.md
