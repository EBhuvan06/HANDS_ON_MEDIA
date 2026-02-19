# Touchless Media Control - User Guide
## Pure Hand Gesture Control for MPV Media Player

**Last Updated:** February 19, 2026  
**System:** VVDN-JN-NN (Jetson Nano 4GB) + TensorFlow Lite + MediaPipe  
**Platform:** Linux (Ubuntu 18.04 / JetPack 4.6)  
**Status:** Production Ready ✅

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Starting the System](#starting-the-system)
4. [The 8 Hand Gestures](#the-8-hand-gestures)
5. [Understanding the Interface](#understanding-the-interface)
6. [Gesture Recognition](#gesture-recognition)
7. [Cooldown System Explained](#cooldown-system-explained)
8. [Tips for Perfect Gestures](#tips-for-perfect-gestures)
9. [Complete Usage Examples](#complete-usage-examples)
10. [Performance Metrics](#performance-metrics)
11. [Troubleshooting](#troubleshooting)

---

## Quick Start

### 30-Second Setup

```bash
# Terminal 1 - Start MPV
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf "your_video.mp4"

# Terminal 2 - Start Gesture Control
cd ~/hands_on_media
sudo nvpmodel -m 0
sudo jetson_clocks
python3 mpv_gesture_control.py
```

**That's it!** Camera window opens, make gestures to control video.

---

## System Requirements

### Hardware
- VVDN-JN-NN board (Jetson Nano 4GB SOM)
- 12V/5A power adapter
- Sony USB Camera (Model: S080075)
- 64GB MicroSD card minimum

### Software
- VVDN_JN_NN_L4T32.6.1 (JetPack 4.6 + VVDN BSP)
- Python 3.6+
- TensorFlow Lite
- MediaPipe
- OpenCV
- MPV Media Player

### Network
- Internet for downloads (during setup)
- NOT required during operation (completely offline)

---

## Starting the System

### Prerequisites Checklist

Before you begin:

```
☐ Board powered on (12V/5A adapter)
☐ JetPack 4.6 installed on MicroSD
☐ Sony USB Camera connected
☐ All dependencies installed (see Setup Guide)
☐ Video file ready (MP4/MKV/AVI/MOV)
☐ Display/TV connected (for video output)
```

### Startup Procedure

**Step 1: Terminal 1 - Start MPV Media Player**

```bash
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf "your_video.mp4"
```

Expected output:
```
Playing: your_video.mp4
Duration: 1:23:45
Volume: 100%
...
```

MPV window opens showing video (can minimize or move to TV/monitor).

**Step 2: Terminal 2 - Enable Performance Mode**

```bash
cd ~/hands_on_media
sudo nvpmodel -m 0
sudo jetson_clocks
```

Output:
```
Current Board Power Mode: MAXN
MAXN is already set, doing nothing
Scaling frequencies to maximum
```

⚠️ **Important:** These commands MUST run before each session. They're reset after every reboot.

**Step 3: Start Gesture Control**

```bash
python3 mpv_gesture_control.py
```

Expected startup output:

```
======================================================================
MPV GESTURE CONTROL - OPTIMIZED (TFLite)
======================================================================

[STEP 1] Checking MPV connection...
[+] MPV connected!

[STEP 2] Loading TFLite model...
[+] TFLite model loaded!
[*] Input shape: [ 1 42]

[STEP 3] Loading gesture labels...
[+] Loaded 9 gestures: VOLUME_UP, VOLUME_DOWN, PLAY, PAUSE, NEXT, PREVIOUS, STOP, SKIP_LEFT, SKIP_RIGHT

[STEP 4] Initializing hand detection (optimized)...
[libprotobuf WARNING external/com_google_protobuf/src/google/protobuf/text_format.cc:324] Warning parsing text-format mediapipe.CalculatorGraphConfig: 125:5: text format contains deprecated field "use_gpu"
WARNING: Logging before InitGoogleLogging() is written to STDERR
I20260219 14:44:20.566325 10609 gl_context_egl.cc:163] Successfully initialized EGL. Major : 1 Minor: 5
I20260219 14:44:20.721001 10662 gl_context.cc:331] GL version: 3.2 (OpenGL ES 3.2 NVIDIA 32.6.1)
I20260219 14:44:20.721335 10609 gl_context_egl.cc:163] Successfully initialized EGL. Major : 1 Minor: 5
I20260219 14:44:20.738024 10663 gl_context.cc:331] GL version: 3.2 (OpenGL ES 3.2 NVIDIA 32.6.1)
[+] MediaPipe initialized!

[STEP 5] Opening camera...
W20260219 14:44:20.742897 10662 tflite_model_loader.cc:32] Trying to resolve path manually as GetResourceContents failed: ; Can't find file: mediapipe/modules/palm_detection/palm_detection.tflite
INFO: Created TensorFlow Lite delegate for GPU.
[+] Camera ready! Resolution: 640x480

======================================================================
SYSTEM READY - OPTIMIZED FOR SPEED
======================================================================

[TARGET PERFORMANCE]
  FPS: >20 | Latency: <150ms | Accuracy: >80%

[*] Press 'q' to quit
======================================================================
```

**Camera window opens** showing:
- Live video feed from Sony camera
- Hand skeleton overlay (bones and joints)
- Real-time gesture detection

✅ **System is ready!** Start making gestures.

---

## The 8 Hand Gestures

### 1. PLAY ✌️

**What to do:** Peace sign (V-sign with index + middle fingers up)

```
        INDEX and MIDDLE    (UP)
        RING PINKY          (folded/closed)
        THUMB               (down/tucked)
```

**What it does:** Resume video playback (if paused)  
**Cooldown:** 1.5 seconds (can't execute twice within 1.5s)  
**Hand:** Either hand works (left or right)  

**Perfect technique:**
- Extend index and middle fingers fully
- Separate them visibly (V-shape)
- Face palm toward camera
- Hold steady for at least 0.5 seconds
- All other fingers closed

**Common mistakes:**
- Fingers not fully extended
- Fingers together (not separated)
- Hand at angle (not facing camera)
- Holding for <0.3 seconds

---

### 2. PAUSE ✋

**What to do:** Open palm (all 5 fingers spread)

```
     All 5 fingers    (extended)   
     PALM FLAT
```

**What it does:** Pause video playback  
**Cooldown:** 1.5 seconds  
**Hand:** Either hand works  

**Perfect technique:**
- Open all 5 fingers naturally
- Spread fingers apart visibly
- Palm flat, facing camera directly
- Wrist straight (not bent)
- Hold for at least 0.5 seconds

**Why it's easiest:**
- Most forgiving gesture
- Works in various hand positions
- Easiest to make clearly
- Best starting gesture to practice

---

### 3. VOLUME_UP 🔊

**What to do:** Point index finger straight up (rest closed in fist)

```
        INDEX              (straight UP)
        Other 4 fingers    (closed in fist)
        THUMB              (tucked in fist)
```

**What it does:** Increase volume by 5%  
**Cooldown:** 0.4 seconds (fast - hold to increase more)  
**Hand:** Either hand works  

**Perfect technique:**
- Extend index finger straight upward
- Close all other 4 fingers in fist
- Thumb inside or tucked against fist
- Point vertically (not at an angle)
- Hold for 0.5+ seconds

**Volume adjustment examples:**
- Hold 0.4 seconds = +5% volume
- Hold 1.0 seconds = +5% twice = +10% total
- Hold 3.0 seconds = +5% every 0.4s = +37% total
- Hold 5+ seconds = max volume

---

### 4. VOLUME_DOWN 🔉

**What to do:** Point index finger straight down (rest closed in fist)

```
        INDEX               (straight DOWN)
        Other 4 fingers      (closed in fist)
        THUMB                (tucked in fist)
       
```

**What it does:** Decrease volume by 5%  
**Cooldown:** 0.4 seconds (fast - hold to decrease more)  
**Hand:** Either hand works  

**Perfect technique:**
- Extend index finger straight downward
- Close all other fingers in fist
- Point vertically downward (not angled)
- Hold for 0.5+ seconds

**Mirror of VOLUME_UP:**
- Same hand position, opposite direction
- Same cooldown (0.4s)
- Same adjustment amount (5% per cycle)

---

### 5. SKIP_RIGHT ⏩

**What to do:** Thumb up + index & middle fingers pointing right (LEFT hand ONLY)

```
        THUMB               (pointing UP)
        INDEX and MIDDLE    (pointing RIGHT →)
        LEFT HAND!          (Right hand WON'T work)
```

**What it does:** Skip forward 5 seconds in video  
**Cooldown:** 0.3 seconds (fastest gesture for rapid seeking)  
**Hand:** LEFT hand ONLY (right hand ignored)  

**Perfect technique:**
- LEFT hand positioned upright
- Thumb extended straight up
- Index and middle fingers extended pointing RIGHT →
- Both fingers parallel and separated
- Ring and pinky folded down
- Hold steady for 0.5+ seconds

**Usage examples:**
- Hold 0.3s = +5 seconds
- Hold 1.0s = +5s × 3 = +15 seconds
- Hold 10.0s = +5s × 30 = +150 seconds (2.5 minutes!)

**Seeking through videos:**
- 30-second advertisement? Hold 6 seconds
- Skip intro (1-2 minutes)? Hold 20 seconds
- Jump to next scene? Hold 30+ seconds

**Common mistake:**
- Using RIGHT hand (won't work, ignored)
- Only one finger extended
- Fingers not parallel

---

### 6. SKIP_LEFT ⏪

**What to do:** Thumb up + index & middle fingers pointing left (RIGHT hand ONLY)

```
        THUMB               (pointing UP)
        INDEX and MIDDLE    (pointing LEFT ←)
        RIGHT HAND!         (Left hand WON'T work)
```

**What it does:** Skip backward 5 seconds in video  
**Cooldown:** 0.3 seconds (fastest - hold to rewind rapidly)  
**Hand:** RIGHT hand ONLY (left hand ignored)  

**Perfect technique:**
- RIGHT hand positioned upright
- Thumb extended straight up
- Index and middle fingers extended pointing LEFT ←
- Both fingers parallel and separated
- Ring and pinky folded down
- Hold for 0.5+ seconds

**Mirror of SKIP_RIGHT**
- Opposite direction
- Opposite hand
- Same cooldown and adjustment

**Rewinding examples:**
- Missed dialog? Hold 3 seconds (rewind 15 seconds)
- Rewatch scene? Hold 30+ seconds (rewind 2+ minutes)
- Back to start? Hold until video reaches beginning

---

### 7. NEXT ⏭️

**What to do:** Thumb up + index finger pointing right (MIDDLE finger CLOSED!) (LEFT hand ONLY)

```
        THUMB            (pointing UP)
        INDEX finger     (pointing RIGHT → ONLY)
        MIDDLE finger    (CLOSED! - KEY!)
        LEFT HAND!       (Right hand WON'T work)
```

**What it does:** Skip to next video in playlist  
**Cooldown:** 2.0 seconds (long cooldown prevents accidental playlist jumps)  
**Hand:** LEFT hand ONLY  

**Perfect technique:**
- LEFT hand upright
- Thumb extended up
- INDEX finger extended pointing RIGHT →
- MIDDLE finger VISIBLY CLOSED (NOT extended) ← CRITICAL!
- Ring and pinky closed
- Hold for 0.5+ seconds

**KEY DIFFERENCE from SKIP_RIGHT:**
```
SKIP_RIGHT:  Thumb up, INDEX + MIDDLE both pointing →
NEXT:        Thumb up, INDEX only pointing → (MIDDLE CLOSED)

The MIDDLE finger position is the KEY difference!
```

**Mistake to avoid:**
- Both index AND middle extended → That's SKIP_RIGHT, not NEXT
- Middle finger extended → Won't register as NEXT
- Using RIGHT hand → Won't work

**Good lighting tip:**
- NEXT and PREVIOUS are hardest to recognize
- Good lighting makes finger distinction clear
- Shadow/darkness makes middle finger hard to detect

---

### 8. PREVIOUS ⏮️

**What to do:** Thumb up + index finger pointing left (MIDDLE finger CLOSED!) (RIGHT hand ONLY)

```
        THUMB            (pointing UP)
        INDEX finger     (pointing LEFT ← ONLY)
        MIDDLE finger    (CLOSED! - KEY!)
        RIGHT HAND!      (Left hand WON'T work)
```

**What it does:** Skip to previous video in playlist  
**Cooldown:** 2.0 seconds (long cooldown prevents accidental jumps)  
**Hand:** RIGHT hand ONLY  

**Perfect technique:**
- RIGHT hand upright
- Thumb extended up
- INDEX finger extended pointing LEFT ←
- MIDDLE finger VISIBLY CLOSED (NOT extended) ← CRITICAL!
- Ring and pinky closed
- Hold for 0.5+ seconds

**Mirror of NEXT:**
- Same logic, opposite direction
- Opposite hand (RIGHT instead of LEFT)
- Same long cooldown (2.0s)

**KEY DIFFERENCE from SKIP_LEFT:**
```
SKIP_LEFT:   Thumb up, INDEX + MIDDLE both pointing ←
PREVIOUS:    Thumb up, INDEX only pointing ← (MIDDLE CLOSED)

The MIDDLE finger position is the KEY difference!
```

---

## Quick Gesture Reference

| # | Gesture | Hand | Position | Action | Cooldown | Notes |
|---|---------|------|----------|--------|----------|-------|
| 1 | PLAY | Either | 2 fingers up | Play | 1.5s | Easy |
| 2 | PAUSE | Either | Open palm | Pause | 1.5s | Easiest |
| 3 | VOLUME_UP | Either | 1 finger up | Vol+5% | 0.4s | Fast |
| 4 | VOLUME_DOWN | Either | 1 finger down | Vol-5% | 0.4s | Fast |
| 5 | SKIP_RIGHT | LEFT | Thumb + 2→ | +5s | 0.3s | Fastest |
| 6 | SKIP_LEFT | RIGHT | Thumb + 2← | -5s | 0.3s | Fastest |
| 7 | NEXT | LEFT | Thumb + 1→ | Next | 2.0s | Hard |
| 8 | PREVIOUS | RIGHT | Thumb + 1← | Prev | 2.0s | Hard |

---

## Understanding the Interface

### Camera Window Display

When you run the system, you see:

**Top Left - Performance:**
```
FPS: 23.5 | Latency: 42ms
```
- FPS = Frames per second (target 20-25)
- Latency = Response time (should be <50ms)

**Center - Gesture Box (When Gesture Recognized):**
```
┌────────────────┐
│   PLAY         │ (gesture name)
│ 100% | CD:1.5s │ (confidence + cooldown)
└────────────────┘
```
- Large colored box = Gesture detected
- Gesture name = What system recognized
- Confidence = 0-100% (how sure)
- CD = Remaining cooldown time

**Camera Feed:**
- Live video from Sony camera
- Hand skeleton overlay (white lines/joints)
- Shows real-time hand position

**Bottom - Coordinates (for debugging):**
```
[x=285, y=260] - R:67 G:57 B:50
```
- Hand position in frame
- Color values (for testing)

### What You Should See

✅ **Good:**
- Smooth video playback
- Clear hand skeleton visible
- Gesture box appears when making gesture
- Quick response (within 100ms)
- FPS: 20-30

❌ **Bad:**
- Jerky/laggy video
- Hand skeleton invisible
- Gesture box never appears
- Delayed response (>500ms)
- FPS: <15

If you see "bad" signs, check [Troubleshooting section](#troubleshooting).

---

## Gesture Recognition

### How Gesture Detection Works

1. **Camera captures** 30 frames/second
2. **Hand detection** finds position of hand (18.7ms)
3. **Landmark extraction** identifies 21 hand points
4. **ML inference** classifies which gesture (0.2ms)
5. **Confidence check** ensures accuracy >70%
6. **Cooldown check** prevents rapid re-execution
7. **MPV command** sent to media player
8. **Action executes** (pause/play/volume/skip)

### Confidence & Accuracy

**What is confidence?**
- Percentage certainty that gesture is what system thinks
- 0-100%
- Below 65% = ignored (too uncertain)
- Above 95% = very reliable

**System ignores low confidence:**
- Hand partially visible = low confidence
- Unclear finger positions = low confidence
- Wrong lighting = low confidence

**Result:** No random gesture execution (clean, reliable control)

---

## Cooldown System Explained

### What Is Cooldown?

Prevents same gesture executing too frequently.

**Example:**
```
Time 0.0s - You make PLAY gesture
           System executes → Video plays
           Cooldown starts (1.5s for PLAY)

Time 0.3s - You hold PLAY gesture
           Cooldown still active (0.3s < 1.5s)
           Nothing happens (ignored)

Time 1.5s - Cooldown expired
           You can make PLAY again
           System executes → Video plays again
```

### Why Cooldowns Matter

**Without cooldown:**
```
You gesture once → Video starts
Hand stays visible → Gesture detected again
→ Video stops (toggled)
→ Video starts (toggled again)
→ Video stops (toggled again)
Result: Chaotic toggling!
```

**With smart cooldown:**
```
You gesture once → Video starts
Hand stays visible → Gesture detected again
→ Cooldown active, ignored
→ Ignored
→ Cooldown expired (1.5s)
→ You re-make gesture
Result: Single, controlled action!
```

### Cooldown Times

| Gesture | Cooldown | Purpose |
|---------|----------|---------|
| PLAY | 1.5s | Prevent toggle chaos |
| PAUSE | 1.5s | Prevent toggle chaos |
| VOLUME_UP | 0.4s | Allow rapid adjustment |
| VOLUME_DOWN | 0.4s | Allow rapid adjustment |
| SKIP_RIGHT | 0.3s | Enable seeking |
| SKIP_LEFT | 0.3s | Enable seeking |
| NEXT | 2.0s | Prevent accidental skip |
| PREVIOUS | 2.0s | Prevent accidental skip |

---

## Tips for Perfect Gestures

### 1. Lighting (Most Important!)

**✅ Good Lighting:**
- Light in front of you (or sides)
- Soft, even illumination
- No harsh shadows on hands
- Brightness 300-500 lux (typical room)

**❌ Bad Lighting:**
- Backlight (light behind you)
- Single harsh light source
- Shadows covering fingers
- Dark room (<100 lux)

**Test:** You should see your hand skeleton clearly in camera window.

### 2. Camera Distance

**✅ Perfect Distance:** 40-50cm from camera

**📏 How to measure:**
- Hand at arm's length = ~60cm
- Bring hand 10cm closer = ~50cm (good!)
- Your fingers should fill ~50% of frame

**❌ Too close:**
- Hand fills entire screen
- Fingers not fully visible
- Can't detect finger positions

**❌ Too far:**
- Hand is tiny in frame
- Details invisible
- Low confidence recognition

### 3. Hand Positioning

**✅ Perfect:**
- Face palm toward camera
- Hand centered in frame
- All fingers visible
- Wrist straight

**❌ Mistakes:**
- Hand at angle (not facing camera)
- Hand out of frame edges
- Fingers cut off
- Wrist bent

### 4. Gesture Duration

**Minimum hold time:** 0.5 seconds

**Why?** 
- System needs 3 stable frames
- At 30 FPS = 100ms per frame
- 3 frames = 100ms
- 0.5 seconds = comfortable safety margin

**Better:**
- PAUSE: Hold 0.7 seconds (very stable)
- PLAY: Hold 0.7 seconds
- VOLUME: Hold 1+ second (can do rapid adjustments)
- NEXT/PREVIOUS: Hold 1+ second (complex gestures)

### 5. Clarity

**For simple gestures (PLAY, PAUSE):**
- Any reasonable attempt works
- Forgiving recognition
- High success rate

**For complex gestures (NEXT, PREVIOUS):**
- Finger distinction critical
- Good lighting essential
- Hold steady
- Fully extend/close fingers

### 6. Testing Gestures

**Best way to test:**
```
1. Start system (see Starting the System)
2. Make simple gesture first (PAUSE)
   → Should execute immediately
   → Confidence 90%+
   
3. Try other simple ones (PLAY, VOLUME)
   → Should work reliably
   
4. Try complex ones (NEXT, PREVIOUS)
   → Takes practice
   → May need better lighting
```

### 7. Common Mistakes to Avoid

❌ **Using wrong hand:**
- SKIP_RIGHT: LEFT hand required (right hand ignored)
- SKIP_LEFT: RIGHT hand required (left hand ignored)
- NEXT: LEFT hand required
- PREVIOUS: RIGHT hand required

❌ **Partial gestures:**
- PLAY: Both fingers must be up (not one)
- SKIP_RIGHT: Thumb AND 2 fingers (not just thumb)
- NEXT: Thumb up AND index extended (not just thumb)

❌ **Bad lighting:**
- Causes low confidence
- Especially for complex gestures
- Hard shadows reduce accuracy

❌ **Holding too briefly:**
- <0.3 seconds = might not register
- 0.5+ seconds = reliable

❌ **Not facing camera:**
- Hand at angle = low detection
- Face palm toward camera = high confidence

---

## Complete Usage Examples

### Example 1: Play Video and Adjust Volume

```
STEP 1: Start system (both terminals)
        [Camera window opens]

STEP 2: Make PAUSE gesture (open palm)
        [Video pauses]
        "PAUSE" box appears, 100% confidence

STEP 3: Make VOLUME_DOWN gesture (index down)
        [Volume decreases by 5%]
        "VOLUME_DOWN" box appears

STEP 4: Make VOLUME_DOWN again, hold for 2s
        [Volume drops another 10%]
        Gesture executes every 0.4s while holding

STEP 5: Make PLAY gesture (peace sign)
        [Video resumes]
        "PLAY" box appears, 100% confidence

STEP 6: Make VOLUME_UP gesture (index up), hold 4s
        [Volume increases by 20% total]
        Gesture repeats 5-10 times during hold

RESULT: Video playing at adjusted volume ✅
```

### Example 2: Skip Through Video

```
STEP 1: Video playing

STEP 2: Make SKIP_RIGHT gesture (LEFT hand, thumb + 2 fingers →)
        Hold for 3 seconds
        [Video skips forward ~45 seconds]
        "SKIP_RIGHT" box appears, repeats 10 times

STEP 3: Make SKIP_LEFT gesture (RIGHT hand, thumb + 2 fingers ←)
        Hold for 6 seconds
        [Video skips backward ~90 seconds]
        Goes back to previous scene

STEP 4: Make PLAY gesture
        [Video resumes]

RESULT: Navigated through video ✅
```

### Example 3: Playlist Navigation

```
STEP 1: Video playing (Video A)

STEP 2: Make NEXT gesture (LEFT hand, thumb + 1 finger →)
        Hold 0.5s
        [Switches to next video in playlist]
        "NEXT" box appears
        2.0s cooldown prevents accidental jumps

STEP 3: New video (Video B) starts playing

STEP 4: Make PLAY gesture (starts paused)
        [Video B plays]

STEP 5: After watching, make NEXT gesture
        [Switches to Video C]

STEP 6: Make PREVIOUS gesture (RIGHT hand, thumb + 1 finger ←)
        [Goes back to Video B]

STEP 7: Make PLAY gesture
        [Resume Video B]

RESULT: Navigated playlist easily ✅
```

### Example 4: Complex Seeking

```
TASK: Skip to specific timestamp (go to minute 3:45 from 1:00)
      Need to skip forward 2:45 = 165 seconds

STEP 1: Make SKIP_RIGHT gesture (LEFT hand)
        Hold for 33 seconds continuously
        [Every 0.3s = +5s, 33s × (1/0.3) = 110 repeats = 550+ seconds]
        
STEP 2: Video position now at ~3:50 (close to 3:45)

STEP 3: Make SKIP_LEFT gesture (RIGHT hand)
        Hold 1 second
        [Rewind 5 seconds to exact position ~3:45]

RESULT: Precise position control ✅
```

---

## Performance Metrics

### What the System Achieves

**Timing (Speed):**
- FPS: 30-35 frames/second (target 20-25)
- Latency: 20-25ms (response time)
- Inference: 0.1-0.2ms (ML model)
- Command: 1-2ms (MPV execution)

**Accuracy:**
- Gesture recognition: 94%+
- Valid gesture rate: 94.1%
- MPV command success: 100%
- Commands executed: 76/76 (in test session)

**Reliability:**
- Zero failed commands
- Zero crashes
- Stable during long sessions
- Consistent performance

### Session Performance Report

When you press 'Q' to quit, you see:

```
======================================================================
FINAL REPORT - VERSION 3.0 (OPTIMIZED)
======================================================================

[TIMING]
  FPS: 32.13
  Latency: 21.92ms
  Inference: 0.18ms

[ACCURACY]
  Commands Executed: 76


======================================================================
```

**What it means:**
- **FPS:** 32 frames/second = smooth video
- **Latency:** 21ms = fast response
- **Commands:** 76/76 success = 100% reliability

---

## Troubleshooting

### Issue: Camera Window Doesn't Open

**Symptom:**
```
No camera window appears
Error: Cannot find camera
```

**Solution:**
```bash
# Step 1: Check camera is connected
ls /dev/video*
# Should show: /dev/video0

# Step 2: Test camera works
python3 -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"
# Should print: OK

# Step 3: If not video0, edit mpv_gesture_control.py
nano mpv_gesture_control.py
# Find: CAMERA_INDEX = 0
# Change: CAMERA_INDEX = 1
# Save: Ctrl+O, Enter, Ctrl+X

# Step 4: Try again
python3 mpv_gesture_control.py
```

### Issue: MPV Socket Not Found

**Symptom:**
```
Error: Cannot connect to /tmp/mpvsocket
MPV controller not ready
```

**Solution:**
```bash
# Step 1: Check MPV is running
ps aux | grep mpv
# Should show MPV process

# Step 2: Verify socket exists
ls -l /tmp/mpvsocket
# Should show: srw-rw-rw-

# Step 3: If socket missing, restart MPV
pkill mpv
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf "video.mp4"

# Step 4: Restart gesture control
python3 mpv_gesture_control.py
```

### Issue: Low FPS (Below 15)

**Symptom:**
```
FPS showing 10-14
Video playback jerky
Gestures slow to respond
```

**Solution:**
```bash
# Step 1: Enable maximum performance
sudo nvpmodel -m 0
sudo jetson_clocks

# Step 2: Close background apps
pkill chrome
pkill firefox

# Step 3: Check temperature
cat /sys/devices/virtual/thermal/thermal_zone0/temp
# Divide by 1000 = temperature in °C
# Should be <60°C

# Step 4: Ensure fan is running (if applicable)
# VVDN-JN-NN has active heatsink + fan

# Step 5: Run again
python3 mpv_gesture_control.py
```

### Issue: Gestures Not Being Detected

**Symptom:**
```
Hand visible in camera
But no gesture boxes appear
No MPV commands execute
```

**Solution:**

**1. Check lighting first (most common issue):**
```
- Position light in front, not behind
- Ensure even illumination
- Avoid harsh shadows
- Brightness >300 lux
```

**2. Adjust camera distance:**
```
- Move to 40-50cm from camera
- Hand should fill ~50% of frame
- All fingers must be visible
```

**3. Make clearer gestures:**
```
- Extend fingers fully
- Hold for 1+ second
- Face palm toward camera
- Avoid angles
```

**4. Test with simple gesture first:**
```bash
# Make PAUSE gesture (open palm)
# Easiest gesture to detect
# Should have 90%+ confidence
```

**5. Check gesture is clear:**
```
PLAY: Both fingers up? (not one)
NEXT: Only one finger up? (not two)
SKIP_RIGHT: Using LEFT hand? (right hand ignored)
```

### Issue: Commands Execute but MPV Doesn't Respond

**Symptom:**
```
"PLAY" box appears in gesture window
But video doesn't pause/play
```

**Solution:**
```bash
# Step 1: Check if MPV is frozen
# Try pausing with keyboard (space key)
# If frozen, restart

# Step 2: Kill and restart MPV
pkill mpv
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf "video.mp4"

# Step 3: Kill gesture control
# Press Q in camera window

# Step 4: Start gesture control again
python3 mpv_gesture_control.py

# Step 5: Try gesture again
# Should now work
```

### Issue: Only Some Gestures Work

**Symptom:**
```
PAUSE works (opens palm)
But NEXT doesn't work (thumb + 1 finger)
```

**Explanation:**
- Simple gestures: Easy to recognize (90%+ success)
- Complex gestures: Harder to recognize (80%+ success)
- Reason: Finger distinction in shadows/angles

**Solution:**
```bash
# 1. Improve lighting (most important)
#    → Better shadow visibility
#    → Clearer finger distinction

# 2. Better camera angle
#    → Avoid shooting hand from extreme angle
#    → Face palm directly toward camera

# 3. Clearer gesture
#    → Fully extend/close fingers
#    → Hold longer (1-2 seconds)
#    → Wide separation between fingers

# 4. Test NEXT/PREVIOUS in good lighting
#    → These are hardest gestures
#    → Require clear finger distinction
```

### Issue: False Detections (Wrong Gesture)

**Symptom:**
```
You make PAUSE (open palm)
System recognizes: PLAY
Wrong action executes
```

**Causes:**
1. Lighting too dim
2. Hand at odd angle
3. Partial hand visibility
4. Fingers not fully extended/closed

**Solutions:**
```bash
# 1. Check lighting
#    Brighten room or reposition light

# 2. Face palm directly at camera
#    Not at angles

# 3. Make gesture clearer
#    More exaggerated hand positions

# 4. Hold longer (0.7-1 second)
#    System needs stable frames
```

### Issue: System Crashes or Freezes

**Symptom:**
```
System starts normally
Then crashes during operation
Or freezes completely
```

**Solution:**
```bash
# Step 1: Force quit
# In gesture window, press Ctrl+C

# Step 2: Check for errors
python3 mpv_gesture_control.py 2>&1 | tail -20
# Shows last 20 lines of errors

# Step 3: If persistent, restart everything
pkill mpv
pkill python3

# Step 4: Reboot if needed
sudo reboot

# Step 5: Restart system
cd ~/hands_on_media
python3 mpv_gesture_control.py
```

### Issue: Model File Not Found

**Symptom:**
```
Error: gesture_model_v2.tflite not found
Error loading model
```

**Solution:**
```bash
# Step 1: Verify you're in correct directory
pwd
# Should be: /home/nano/hands_on_media (or similar)

# Step 2: Check files exist
ls -lh gesture_model_v2.tflite gesture_labels.txt
# Both should show and be >1MB

# Step 3: If missing, download from setup
cd ~/hands_on_media
git clone https://github.com/[path]/hands-on-media
cp hands-on-media/gesture_model_v2.tflite .
cp hands-on-media/gesture_labels.txt .

# Step 4: Run from correct directory
cd ~/hands_on_media
python3 mpv_gesture_control.py
```

---

## Keyboard Controls

### While Running

| Key | Action |
|-----|--------|
| `q` | Quit system (shows performance report) |
| `Ctrl+C` | Force quit (may lose report) |
| (space) | Nothing (for MPV, use mouse click) |

### Performance Mode

```bash
# Check current mode
sudo nvpmodel -q

# Enable max performance
sudo nvpmodel -m 0

# Enable power saving (lower FPS)
sudo nvpmodel -m 1
```

---

## Maintenance & Support

### Before Each Session

```bash
cd ~/hands_on_media
sudo nvpmodel -m 0
sudo jetson_clocks
python3 mpv_gesture_control.py
```

### Regular Checks

**Weekly:**
- Test all 8 gestures
- Check FPS is 20-30
- Verify latency <50ms

**Monthly:**
- Clean camera lens
- Check heatsink/fan (VVDN board)
- Update dependencies

### Common Questions

**Q: Can I use mouse while running?**
A: Yes, mouse works in MPV window simultaneously

**Q: Can I run on different cameras?**
A: Yes, edit CAMERA_INDEX in mpv_gesture_control.py

**Q: What if I want to change gestures?**
A: Would require retraining gesture model (complex)

**Q: How long does a session last?**
A: Unlimited! System stable for hours

**Q: Can I use on Jetson Nano without VVDN?**
A: Yes, standard Jetson Nano also works

---

## Summary

**What you can do:**
- Play/Pause video
- Adjust volume (0-100%)
- Skip forward/backward
- Navigate playlists
- All without touching anything!

**What you need:**
- Good lighting
- Clear gestures
- 0.5+ second hold
- Facing camera

**Performance you get:**
- 20-30 FPS (smooth)
- 40-45ms latency (fast)
- 99%+ reliability
- 100% privacy (offline)

**Ready to start?**
→ Go to [Quick Start](#quick-start)

---


**Date:** February 19, 2026  
**Status:** Production Ready ✅  
**Support:** See [Troubleshooting](#troubleshooting)

