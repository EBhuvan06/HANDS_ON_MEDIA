# MPV Gesture Control v2.0 - Setup Guide  
## Installation & Configuration (Invalid Gesture Detection System)

**Last Updated:** February 19, 2026  
**Version:** 2.0 (Smart Help System)  
**Platform:** VVDN-JN-NN (Jetson Nano 4GB)  
**Setup Time:** 30-45 minutes  
**Difficulty:** Beginner-Friendly ✅

---

## 📋 Table of Contents

1. [What's New in v2.0 Setup](#whats-new-in-v20-setup)
2. [System Requirements](#system-requirements)
3. [Hardware Setup](#hardware-setup)
4. [Software Installation](#software-installation)
5. [Project Setup](#project-setup)
6. [Configuration Guide](#configuration-guide)
7. [Testing & Verification](#testing--verification)
8. [Performance Tuning](#performance-tuning)
9. [Troubleshooting](#troubleshooting)

---

## What's New in v2.0 Setup

### Version 2.0 Changes

**New Features Added:**
-  Invalid gesture detection system
-  Interactive help overlay
-  Smart per-gesture cooldown timers
-  Enhanced confidence monitoring

**Setup Differences from v1.0:**
- **Same hardware** - No new components needed
- **Same dependencies** - TensorFlow Lite, MediaPipe, OpenCV
- **New config parameters** - Cooldowns & thresholds
- **Enhanced testing** - Help menu verification

**Note:** This version does NOT include face recognition  
- Simpler setup than face-gated version
- Focus on gesture quality and user guidance
- No additional face detection libraries needed

---

## System Requirements

### Hardware Checklist

```
✅ REQUIRED:
   ☐ VVDN-JN-NN Board (Jetson Nano 4GB SOM)
   ☐ 12V/5A Power Supply (IMPORTANT: correct voltage!)
   ☐ 64GB MicroSD Card (Class 10, V30+ recommended)
   ☐ Sony USB Camera Model S080075
   ☐ USB Keyboard + Mouse (for setup)
   ☐ HDMI Display or TV

⚙️ OPTIONAL (recommended):
   ☐ Heatsink + Fan (VVDN has built-in)
   ☐ Ethernet cable (faster than WiFi)
   ☐ USB Hub (for multiple devices)
```

### Software Requirements

```
✅ Operating System:
   - VVDN_JN_NN_L4T32.6.1 (JetPack 4.6 + VVDN BSP)
   - Linux kernel 4.9+

✅ Python Environment:
   - Python 3.6 or higher
   - pip3 package manager

✅ Core Libraries:
   - TensorFlow Lite 2.5+
   - MediaPipe 0.8+ (ARM64 build for Jetson)
   - OpenCV 4.5+
   - NumPy 1.19+

✅ Media Player:
   - MPV (latest version with IPC support)

✅ Storage:
   - 10GB free space minimum
```

### Network Requirements

```
🌐 During Setup:
   - Internet connection required for:
     • Downloading OS image
     • Installing packages
     • Downloading models

🌐 During Operation:
   - NO internet required
   - Completely offline
   - 100% local processing
```

---

## Hardware Setup

### Step 1: Prepare MicroSD Card

**What You Need:**
- 64GB MicroSD card (Class 10 or better)
- Card reader
- Computer with USB port

**Format the Card:**

**Windows:**
```
1. Download SD Card Formatter
2. Insert MicroSD card
3. Select card drive
4. Click "Format"
5. Wait for completion
```

**Mac:**
```
1. Open Disk Utility
2. Select MicroSD card
3. Click "Erase"
4. Format: MS-DOS (FAT32)
5. Click "Erase"
```

**Linux:**
```bash
# List devices
lsblk

# Format (replace sdX with your card)
sudo mkfs.ext4 /dev/sdX
```

⚠️ **Warning:** Formatting erases ALL data!

### Step 2: Install JetPack OS Image

**Download OS:**
```
Image: VVDN_JN_NN_L4T32.6.1.tar.gz
Source: VVDN support website or provided USB

Extract:
tar -xzf VVDN_JN_NN_L4T32.6.1.tar.gz
```

**Write Image (Recommended: Balena Etcher)**

```
1. Download Balena Etcher (balena.io/etcher)
2. Open Etcher
3. "Select Image" → Choose extracted .img file
4. "Select Target" → Choose MicroSD card
5. Click "Flash"
6. Wait 5-10 minutes
7. "Flash Complete!" → Remove card
```

**Alternative: Using dd (Linux/Mac)**
```bash
# Identify card
lsblk  # Linux
diskutil list  # Mac

# Unmount
sudo umount /dev/sdX*  # Linux
diskutil unmountDisk /dev/diskN  # Mac

# Write image (CAREFUL - double-check device!)
sudo dd if=VVDN_JN_NN_L4T32.6.1.img of=/dev/sdX bs=4M status=progress

# Takes 15-20 minutes
# Be patient!
```

### Step 3: Install MicroSD & Power On

**Install Card:**
```
1. Locate MicroSD slot on VVDN carrier board
2. Insert card (contacts facing down/inward)
3. Push until it clicks into place
4. Card should sit flush, not protruding
```

**First Boot:**
```
1. Connect 12V/5A power adapter
2. Green LED indicates power
3. Blue LED indicates activity
4. Wait 30-60 seconds
5. Ubuntu login screen appears

Default Login:
Username: nano
Password: nano
```

---

## Software Installation

### Step 1: Initial System Update

```bash
# Log in to Jetson Nano
# Username: nano
# Password: nano

# Update package lists
sudo apt-get update

# Upgrade system packages
sudo apt-get upgrade -y

# Install essential build tools
sudo apt-get install -y build-essential git wget curl vim

# This takes 5-10 minutes
```

### Step 2: Network Configuration

**Ethernet (Recommended):**
```bash
# Plug in ethernet cable
# Auto-configured

# Verify connection
ifconfig
# Should show inet address (e.g., 192.168.1.100)

# Test internet
ping -c 4 google.com
```

**WiFi (Alternative):**
```bash
# Use network manager UI
sudo nmtui

# Or command line
sudo nmcli device wifi connect "YourSSID" password "YourPassword"
```

### Step 3: Python & pip Setup

```bash
# Check Python version
python3 --version
# Should be: Python 3.6.9 or higher

# Install pip3
sudo apt-get install -y python3-pip

# Upgrade pip
sudo pip3 install --upgrade pip

# Verify
python3 -m pip --version
# Should be: pip 21.3 or higher
```

### Step 4: Install Core Python Libraries

```bash
# NumPy (mathematical operations)
sudo pip3 install numpy==1.19.4

# SciPy (scientific computing)
sudo pip3 install scipy

# This takes 5 minutes
```

### Step 5: Install TensorFlow Lite

**NVIDIA's Optimized Build for Jetson:**

```bash
# Download NVIDIA's TensorFlow wheel (JetPack 4.6)
cd ~/
wget https://developer.download.nvidia.com/compute/redist/jp/v46/tensorflow/tensorflow-2.5.0+nv21.8-cp36-cp36m-linux_aarch64.whl

# Install
sudo pip3 install tensorflow-2.5.0+nv21.8-cp36-cp36m-linux_aarch64.whl

# Takes 10-15 minutes

# Verify installation
python3 -c "import tensorflow as tf; print('TensorFlow', tf.__version__)"
# Should output: TensorFlow 2.5.0
```

### Step 6: Install MediaPipe (Critical!)

**⚠️ Important:** MediaPipe requires special installation for Jetson Nano (ARM architecture)

**Step 6a: Create Swap File (Required!)**

```bash
# Clone swap installer
cd ~/
git clone https://github.com/JetsonHacksNano/installSwapfile.git
cd installSwapfile/

# Run installer
./installSwapfile.sh

# Creates 6GB swap file (takes 2-3 minutes)

# Verify swap active
swapon --show
# Should show: /mnt/swapfile with 6G size

free -h
# Should show swap space
```

**Step 6b: Install MediaPipe Dependencies**

```bash
# System packages
sudo apt-get update
sudo apt-get install -y \
    libhdf5-serial-dev hdf5-tools libhdf5-dev \
    zlib1g-dev zip libjpeg8-dev \
    liblapack-dev libblas-dev gfortran

# Python dependencies (specific versions required!)
sudo pip3 install -U pip testresources setuptools==49.6.0

sudo pip3 install -U --no-deps \
    numpy==1.19.4 \
    future==0.18.2 \
    mock==3.0.5 \
    keras_preprocessing==1.1.2 \
    keras_applications==1.0.8 \
    gast==0.4.0 \
    protobuf \
    pybind11 \
    cython \
    pkgconfig

# h5py (specific install method)
sudo env H5PY_SETUP_REQUIRES=0 pip3 install -U h5py==3.1.0

# Takes 5-10 minutes total
```

**Step 6c: Download & Install MediaPipe**

```bash
# Clone pre-built MediaPipe wheels repository
cd ~/
git clone https://github.com/PINTO0309/mediapipe-bin
cd mediapipe-bin

# Install the wheel (Python 3.6, CUDA 10.2, ARM64)
pip3 install v0.8.5/v0.8.5/numpy119x/py36/mediapipe-0.8.5_cuda102-cp36-cp36m-linux_aarch64.whl

# Takes 2-3 minutes

# Verify installation
python3 << 'EOF'
import mediapipe as mp
print("MediaPipe version:", mp.__version__)
print("MediaPipe location:", mp.__file__)
EOF
# Should output version and path
```

**Step 6d: Fix Import Conflicts (CRITICAL!)**

```bash
# Check if ~/mediapipe folder exists (causes conflicts)
ls -la ~/mediapipe

# If it exists, rename it
if [ -d ~/mediapipe ]; then
    mv ~/mediapipe ~/mediapipe-source
    echo "Renamed conflicting mediapipe folder"
fi

# Verify fix
python3 -c "import mediapipe as mp; print('✓ MediaPipe working correctly')"
```

### Step 7: Install OpenCV

```bash
# System OpenCV with Python bindings
sudo apt-get install -y python3-opencv

# Verify
python3 << 'EOF'
import cv2
print("OpenCV version:", cv2.__version__)
EOF
# Should show: OpenCV 4.x
```

### Step 8: Install MPV Media Player

```bash
# Install MPV with IPC support
sudo apt-get install -y mpv

# Verify installation
mpv --version
# Should show version info

# Test IPC support
mpv --help | grep input-ipc-server
# Should show: --input-ipc-server=<filename>
```

---

## Project Setup

### Step 9: Create Project Directory

```bash
# Create main project folder
mkdir -p ~/hands_on_gesture
cd ~/hands_on_gesture

# Create subdirectories
mkdir -p models    # For TFLite model & labels
mkdir -p logs      # For log files
mkdir -p videos    # For test videos
```

### Step 10: Download Project Files

**Option A: Git Clone (if repository available)**
```bash
cd ~/hands_on_gesture
git clone https://github.com/[your-repo]/mpv-gesture-control-v2.git .
```

**Option B: Manual Copy**
```bash
# Copy these files to ~/hands_on_gesture/:
# 
# Main program:
#   version_2.py
#
# Model files (to ~/hands_on_gesture/models/):
#   gesture_model_v2.tflite  (gesture recognition model)
#   gesture_labels.txt       (gesture names)
```

### Step 11: Verify Project Structure

```bash
cd ~/hands_on_gesture

# List files
ls -lh

# Expected output:
# version_2.py
# models/
# logs/
# videos/

# Check models directory
ls -lh models/

# Expected:
# gesture_model_v2.tflite  (~5-10 MB)
# gesture_labels.txt       (small text file)
```

### Step 12: Set Permissions

```bash
# Make main script executable
chmod +x version_2.py

# Verify file sizes
ls -lh models/gesture_model_v2.tflite
# Should be >5 MB (if smaller, file may be corrupt)

# Check labels file
cat models/gesture_labels.txt
# Should list 9 gesture names
```

---

## Configuration Guide

### Step 13: Understanding Configuration

Open `version_2.py` and locate the configuration section (lines 31-74):

```python
# ==================== CONFIGURATION ====================

# Model paths
MODEL_PATH = '~/hands_on_gesture/models/gesture_model_v2.tflite'
LABELS_PATH = '~/hands_on_gesture/models/gesture_labels.txt'
MPV_SOCKET = '/tmp/mpvsocket'

# Camera settings
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAMERA_INDEX = 0

# MediaPipe hand detection
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# Gesture recognition
CONFIDENCE_THRESHOLD = 0.70
STABLE_FRAMES = 3
INVALID_GESTURE_THRESHOLD = 0.65

# Smart cooldown timers
ACTION_COOLDOWNS = {
    'PLAY': 1.5,
    'PAUSE': 1.5,
    'VOLUME_UP': 0.4,
    'VOLUME_DOWN': 0.4,
    'SKIP_RIGHT': 0.3,
    'SKIP_LEFT': 0.3,
    'NEXT': 2.0,
    'PREVIOUS': 2.0,
    'STOP': 3.0
}

# Help menu timing
HELP_SHOW_DURATION = 5.0    # Table display time
HELP_RESUME_DURATION = 2.0  # Resume message time
```

### Step 14: Key Configuration Parameters

**Camera Settings:**
```python
CAMERA_INDEX = 0  # Change if camera not at /dev/video0

# To find your camera:
# Run: ls -l /dev/video*
# Or test: python3 -c "import cv2; cv2.VideoCapture(0).isOpened()"
```

**Detection Confidence:**
```python
MIN_DETECTION_CONFIDENCE = 0.5  # Hand detection sensitivity
# Lower (0.3) = more sensitive, more false positives
# Higher (0.7) = less sensitive, might miss hands

MIN_TRACKING_CONFIDENCE = 0.5   # Hand tracking stability
# Lower = tracks unstable hands
# Higher = requires very stable hands
```

**Gesture Recognition:**
```python
CONFIDENCE_THRESHOLD = 0.70  # Minimum to execute gesture
# Higher (0.80) = stricter, fewer false triggers
# Lower (0.60) = more forgiving, might misrecognize

INVALID_GESTURE_THRESHOLD = 0.65  # Triggers help menu
# When confidence < this value, help appears
# Adjust based on your lighting conditions
```

**Cooldown Timers:**
```python
# Adjust these based on your preferences:

# Fast actions (for rapid adjustment):
'VOLUME_UP': 0.4,      # Can change to 0.3 for faster
'VOLUME_DOWN': 0.4,
'SKIP_RIGHT': 0.3,
'SKIP_LEFT': 0.3,

# Medium actions (prevent accidental triggers):
'PLAY': 1.5,           # Can increase to 2.0
'PAUSE': 1.5,

# Slow actions (critical, rare use):
'NEXT': 2.0,           # Can increase to 3.0
'PREVIOUS': 2.0,
'STOP': 3.0,           # Can increase to 5.0
```

**Help Menu Timing:**
```python
HELP_SHOW_DURATION = 5.0    # How long table shows
# Increase to 7.0 for more reading time
# Decrease to 3.0 for faster dismissal

HELP_RESUME_DURATION = 2.0  # Resume message duration
# Adjust as needed (1.0 - 3.0 seconds)
```

### Step 15: Camera Detection & Configuration

**Find Your Camera:**
```bash
# List video devices
ls -l /dev/video*
# Example output: /dev/video0, /dev/video1

# Test each camera
python3 << 'EOF'
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"✓ Camera found at /dev/video{i}")
        ret, frame = cap.read()
        if ret:
            print(f"  Resolution: {frame.shape[1]}x{frame.shape[0]}")
        cap.release()
    else:
        print(f"✗ No camera at /dev/video{i}")
EOF
```

**Update Configuration:**
```python
# If camera is at /dev/video1 (not video0):
CAMERA_INDEX = 1  # Change this line in version_2.py
```

---

## Testing & Verification

### Step 16: Enable Performance Mode

**CRITICAL - Run before every session:**

```bash
# Set to maximum performance mode
sudo nvpmodel -m 0

# Lock CPU/GPU clocks to maximum
sudo jetson_clocks

# Verify mode
sudo nvpmodel -q
# Output should show: NV Power Mode: MAXN

# Check CPU frequency
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
# Should be: 1479000 (1.479 GHz) or higher
```

### Step 17: Test MPV Connection

**Terminal 1: Start MPV**
```bash
# Test with simple video or image
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf \
    /usr/share/pixmaps/debian-logo.png

# MPV window should open showing Debian logo
```

**Terminal 2: Verify Socket**
```bash
# Check socket was created
ls -l /tmp/mpvsocket
# Should show: srw-rw-rw- (socket file)

# If it exists, MPV is ready!
# Press 'q' in MPV window to quit
```

### Step 18: First Run - System Initialization

**Terminal 1: Restart MPV with test video**
```bash
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf test_video.mp4
```

**Terminal 2: Start Gesture Control**
```bash
cd ~/hand_on_gesture
python3 version_2.py
```

**Expected Startup Output:**
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

**Camera window should open showing:**
- Live video feed
- Hand skeleton when hand detected
- FPS and latency in top-right corner

✅ **If you see this, setup is successful!**

### Step 19: Test Invalid Gesture Detection

**Test Procedure:**
```
1. Camera window is open
2. Make an UNCLEAR gesture (fingers half-closed)
3. Watch for help menu to appear
4. Verify help table shows all 8 gestures
5. Check "Invalid gestures: 1" counter
6. Wait 5 seconds
7. "Great! Let's continue..." message appears
8. Wait 2 more seconds
9. Help dismisses automatically
10. System back to normal
```

**What to verify:**
- ✅ Help table displays correctly
- ✅ All 8 gestures listed with hand requirements
- ✅ Invalid counter increments
- ✅ Auto-dismissal after 7 seconds total
- ✅ System resumes normal operation

**Console Output:**
```
[INVALID] Confidence: 58% | Count: 1 | Help displayed
(Help shown for 5 seconds)
(Resume message for 2 seconds)
(Back to normal operation)
```

### Step 20: Test Valid Gestures

**Test Each Gesture:**

**1. PAUSE (Easiest)**
```
Gesture: Open palm, all 5 fingers spread
Expected: Green box with "PAUSE" and 90%+ confidence
MPV Action: Video pauses
Console: [ACTION] PAUSE | 92% | 2.1ms | 1.5s CD | Pause
```

**2. PLAY**
```
Gesture: Peace sign (index + middle up)
Expected: Green box, 85%+ confidence
MPV Action: Video resumes
Console: [ACTION] PLAY | 88% | 2.3ms | 1.5s CD | Resume
```

**3. VOLUME_UP**
```
Gesture: Index finger up (fist)
Expected: Green box, 90%+ confidence
MPV Action: Volume increases +5%
Console: [ACTION] VOLUME_UP | 95% | 2.2ms | 0.36s CD | Volume +5
```

**4. SKIP_RIGHT (LEFT hand!)**
```
Gesture: Thumb up, 2 fingers pointing right, LEFT hand
Expected: Green box, 85%+ confidence
MPV Action: Skips forward +5 seconds
Console: [ACTION] SKIP_RIGHT | 89% | 2.6ms | 0.3s CD | Seek +5s
```

**Test all 8 gestures!**

### Step 21: Test Cooldown System

**Test Volume Adjustment:**
```
1. Make VOLUME_UP gesture
2. HOLD for 2 seconds
3. Should execute multiple times (every 0.4s)
4. Console shows multiple [ACTION] VOLUME_UP lines
5. Release hand
6. Make PAUSE gesture
7. Should work immediately (different gesture)
```

**Expected Console Output:**
```
[ACTION] VOLUME_UP    | 95% | 2.2ms | 0.36s CD | Volume +5
[ACTION] VOLUME_UP    | 96% | 2.1ms | 0.36s CD | Volume +5
[ACTION] VOLUME_UP    | 94% | 2.3ms | 0.36s CD | Volume +5
[ACTION] VOLUME_UP    | 95% | 2.2ms | 0.36s CD | Volume +5
[ACTION] PAUSE        | 92% | 2.1ms | 1.5s CD | Pause
```

**Verify:**
- ✅ Fast gestures repeat quickly (0.3-0.4s)
- ✅ Medium gestures have 1.5s cooldown
- ✅ Different gestures don't block each other

### Step 22: Performance Verification

**Check On-Screen Metrics:**
```
FPS:25.3        ← Should be >20
Lat:42.5ms      ← Should be <150ms
MPV: 10/0       ← Success/Failed commands
```

**Exit and View Final Report:**
```
======================================================================
FINAL REPORT - VERSION 1.0 (Enhanced)
======================================================================

[TIMING]
  FPS: 17.88
  Latency: 24.56ms
  Hand: 24.36ms | Inference: 0.20ms | Cmd: 4.31ms

[ACCURACY]
  Prediction Accuracy: 8.54%
  Commands Executed: 197
  Invalid Gestures: 11

[MPV]
  Success: 198 | Failed: 0

[COOLDOWN STATS]
  NEXT         CD:2.0s Exec: 15 Rate:  3.5%
  PAUSE        CD:1.5s Exec: 20 Rate:  4.7%
  PLAY         CD:1.5s Exec:  7 Rate:  4.8%
  PREVIOUS     CD:2.0s Exec: 10 Rate:  4.3%
  SKIP_LEFT    CD:0.3s Exec: 32 Rate: 20.4%
  SKIP_RIGHT   CD:0.3s Exec: 23 Rate: 18.9%
  VOLUME_DOWN  CD:0.4s Exec: 36 Rate: 15.9%
  VOLUME_UP    CD:0.4s Exec: 54 Rate: 15.8%

======================================================================
```

**Verification Checklist:**
```
FPS 17.88
Latency 24.56ms
Accuracy > 90%
No MPV failures
Invalid gestures low (<10 during testing)
Help menu works
All gestures recognized
```

---

## Performance Tuning

### Step 23: Optimize for Your Environment

**Adjust for Lighting Conditions:**

**Bright Environment:**
```python
# Edit version_2.py configuration:

MIN_DETECTION_CONFIDENCE = 0.6  # More sensitive
CONFIDENCE_THRESHOLD = 0.75      # Stricter
INVALID_GESTURE_THRESHOLD = 0.70  # Higher threshold
```

**Dim Environment:**
```python
MIN_DETECTION_CONFIDENCE = 0.4  # Less sensitive
CONFIDENCE_THRESHOLD = 0.65      # More forgiving
INVALID_GESTURE_THRESHOLD = 0.60  # Lower threshold
```

**Adjust Cooldown Speed:**

**Faster Response:**
```python
ACTION_COOLDOWNS = {
    'VOLUME_UP': 0.3,     # Changed from 0.4
    'VOLUME_DOWN': 0.3,
    'SKIP_RIGHT': 0.2,    # Changed from 0.3
    'SKIP_LEFT': 0.2,
    # ... keep others same
}
```

**Prevent Accidental Triggers:**
```python
ACTION_COOLDOWNS = {
    'PLAY': 2.0,          # Changed from 1.5
    'PAUSE': 2.0,
    'STOP': 5.0,          # Changed from 3.0
    # ... keep others same
}
```

**Adjust Help Menu Duration:**

**More Reading Time:**
```python
HELP_SHOW_DURATION = 7.0      # Changed from 5.0
HELP_RESUME_DURATION = 3.0    # Changed from 2.0
```

**Faster Dismissal:**
```python
HELP_SHOW_DURATION = 3.0      # Changed from 5.0
HELP_RESUME_DURATION = 1.0    # Changed from 2.0
```

### Step 24: Create Startup Script

**Create convenience script:**

```bash
cat > ~/start_gesture_v2.sh << 'EOF'
#!/bin/bash

echo "=================================================="
echo "  MPV Gesture Control v2.0 - Startup Script"
echo "=================================================="

# Navigate to project directory
cd ~/hands_on_gesture || { echo "Error: Project directory not found"; exit 1; }

# Enable maximum performance
echo "Enabling MAXN performance mode..."
sudo nvpmodel -m 0
sudo jetson_clocks

# Verify performance mode
MODE=$(sudo nvpmodel -q | grep "NV Power Mode")
echo "Current mode: $MODE"

# Start gesture control
echo ""
echo "Starting gesture control v2.0..."
echo "Press 'q' in camera window to quit"
echo "=================================================="
python3 version_2.py

EOF

chmod +x ~/start_gesture_v2.sh
```

**Use it:**
```bash
~/start_gesture_v2.sh
```

### Step 25: Optional - Auto-Start on Boot

**Create systemd service (optional):**

```bash
sudo nano /etc/systemd/system/gesture-control.service

# Add this content:
[Unit]
Description=MPV Gesture Control v2.0
After=network.target

[Service]
Type=simple
User=nano
WorkingDirectory=/home/nano/hands_on_gesture
ExecStartPre=/usr/bin/sudo /usr/sbin/nvpmodel -m 0
ExecStartPre=/usr/bin/sudo /usr/bin/jetson_clocks
ExecStart=/usr/bin/python3 /home/nano/hands_on_gesture/version_2.py
Restart=on-failure

[Install]
WantedBy=multi-user.target

# Save and exit (Ctrl+X, Y, Enter)

# Enable service
sudo systemctl enable gesture-control.service

# Start service
sudo systemctl start gesture-control.service

# Check status
sudo systemctl status gesture-control.service
```

---

## Troubleshooting

### Issue: TensorFlow Import Error

**Error:**
```
ImportError: No module named 'tensorflow'
```

**Solution:**
```bash
# Verify JetPack version
cat /etc/nv_tegra_release
# Should show: R32.6.1 (JetPack 4.6)

# Download correct wheel
cd ~/
wget https://developer.download.nvidia.com/compute/redist/jp/v46/tensorflow/tensorflow-2.5.0+nv21.8-cp36-cp36m-linux_aarch64.whl

# Reinstall
sudo pip3 install --force-reinstall tensorflow-2.5.0+nv21.8-cp36-cp36m-linux_aarch64.whl

# Verify
python3 -c "import tensorflow as tf; print(tf.__version__)"
```

### Issue: MediaPipe Import Error

**Error:**
```
AttributeError: module 'mediapipe' has no attribute 'solutions'
```

**Cause:** Conflicting ~/mediapipe folder

**Solution:**
```bash
# Rename conflicting folder
mv ~/mediapipe ~/mediapipe-source

# Reinstall MediaPipe
cd ~/mediapipe-bin
pip3 install --force-reinstall \
    v0.8.5/v0.8.5/numpy119x/py36/mediapipe-0.8.5_cuda102-cp36-cp36m-linux_aarch64.whl

# Verify
python3 << 'EOF'
import mediapipe as mp
print("MediaPipe location:", mp.__file__)
print("Has solutions:", hasattr(mp, 'solutions'))
EOF
# Should show path NOT in ~/mediapipe
# Should show: Has solutions: True
```

### Issue: Camera Not Found

**Error:**
```
Error: Cannot open camera /dev/video0
```

**Solution:**
```bash
# List all video devices
ls -l /dev/video*

# Test each camera
for i in 0 1 2 3 4; do
    python3 -c "import cv2; cap = cv2.VideoCapture($i); \
    print('Camera $i:', 'FOUND' if cap.isOpened() else 'NOT FOUND'); \
    cap.release()"
done

# Update CAMERA_INDEX in version_2.py
# Example: If camera is at /dev/video1
nano version_2.py
# Change line: CAMERA_INDEX = 1
```

### Issue: MPV Socket Error

**Error:**
```
Cannot connect to /tmp/mpvsocket
MPV controller not ready
```

**Solution:**
```bash
# Check if MPV is running
ps aux | grep mpv

# If not running, start it
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf test.mp4

# Verify socket exists
ls -l /tmp/mpvsocket
# Should show: srw-rw-rw-

# If socket exists but still error, restart both:
pkill mpv
pkill python3
mpv --input-ipc-server=/tmp/mpvsocket test.mp4 &
cd ~/hands_on_gesture && python3 version_2.py
```

### Issue: Model File Not Found

**Error:**
```
FileNotFoundError: gesture_model_v2.tflite
```

**Solution:**
```bash
# Check file exists
ls -lh ~/hands_on_gesture/models/gesture_model_v2.tflite

# If missing, redownload or copy from source

# Check path in config
grep "MODEL_PATH" ~/hands_on_gesture/version_2.py
# Should match actual file location

# Verify file is not corrupt
file ~/hands_on_gesture/models/gesture_model_v2.tflite
# Should show: data

# Check size
du -h ~/hands_on_gesture/models/gesture_model_v2.tflite
# Should be >5 MB
```

### Issue: Low FPS During Testing

**Problem:**
```
FPS showing <15
System sluggish
```

**Solution:**
```bash
# 1. Enable performance mode
sudo nvpmodel -m 0
sudo jetson_clocks

# 2. Verify mode
sudo nvpmodel -q

# 3. Check temperature
cat /sys/devices/virtual/thermal/thermal_zone0/temp
# Divide by 1000 = temp in °C
# Should be <70°C

# 4. Close background apps
pkill chrome
pkill firefox
pkill code

# 5. If still low, reboot
sudo reboot

# Then retry
cd ~/hands_on_gesture
sudo nvpmodel -m 0
sudo jetson_clocks
python3 version_2.py
```

### Issue: Help Menu Not Appearing

**Problem:**
```
Making invalid gestures
But help never shows
```

**Solution:**
```bash
# 1. Check threshold in code
grep "INVALID_GESTURE_THRESHOLD" ~/hands_on_gesture/version_2.py
# Should be: 0.65

# 2. Check console for confidence values
# Look for lines like:
# [INVALID] Confidence: 58% | Count: 1

# 3. If confidence always >65%, adjust threshold
nano ~/hands_on_gesture/version_2.py
# Change: INVALID_GESTURE_THRESHOLD = 0.70  # Higher

# 4. Save and restart
python3 version_2.py
```

### Issue: System Crashes on Startup

**Problem:**
```
Program starts but crashes immediately
```

**Solution:**
```bash
# Run with verbose error output
cd ~/hands_on_gesture
python3 version_2.py 2>&1 | tee startup_error.log

# Check error log
cat startup_error.log

# Common fixes:

# If memory error:
sudo reboot
cd ~/hands_on_gesture && python3 version_2.py

# If camera error:
# Check camera is connected
lsusb | grep -i camera

# If model loading error:
ls -lh models/
# Verify files exist and are correct size
```

---

## Final Verification Checklist

### Complete This Before Considering Setup Done:

```
✅ HARDWARE:
   ☐ VVDN-JN-NN board powers on (green LED)
   ☐ MicroSD card installed correctly
   ☐ Camera connected and detected
   ☐ Display/monitor connected

✅ SOFTWARE:
   ☐ JetPack 4.6 boots successfully
   ☐ Python 3.6+ installed
   ☐ TensorFlow 2.5+ working
   ☐ MediaPipe 0.8+ working
   ☐ OpenCV installed
   ☐ MPV installed

✅ PROJECT:
   ☐ Files in ~/hands_on_gesture/ directory
   ☐ Model files in ~/hands_on_gesture/models/
   ☐ version_2.py executable
   ☐ Configuration reviewed

✅ PERFORMANCE:
   ☐ MAXN performance mode enabled
   ☐ System starts without errors
   ☐ Camera window opens
   ☐ FPS >20
   ☐ Latency <150ms

✅ FUNCTIONALITY:
   ☐ Hand detection works
   ☐ All 8 gestures recognized
   ☐ Invalid gesture help appears
   ☐ Help auto-dismisses
   ☐ MPV responds to commands
   ☐ Cooldown system works
   ☐ Final report displays
```

---

## Quick Reference

### Daily Startup Commands

```bash
# Terminal 1: MPV
mpv --input-ipc-server=/tmp/mpvsocket your_video.mp4

# Terminal 2: Gesture Control
cd ~/hands_on_gesture
sudo nvpmodel -m 0
sudo jetson_clocks
python3 version_2.py
```

### Useful Commands

```bash
# Check system stats
tegrastats

# Check temperature
cat /sys/devices/virtual/thermal/thermal_zone0/temp

# Monitor processes
htop

# Kill everything
pkill python3
pkill mpv

# Restart system
~/start_gesture_v2.sh
```

---

## Next Steps

### Setup Complete! 

**Congratulations! Your system is ready.**

**Next:** Read **USER_GUIDE_V2.md** for:
- Complete gesture guide
- Invalid gesture detection details
- Help menu usage
- Tips for best results
- Troubleshooting

**Start Using:**
```bash
# Start MPV
mpv --input-ipc-server=/tmp/mpvsocket video.mp4

# Start gesture control
cd ~/hands_on_gesture
python3 version_2.py

# Make gestures!
```

---

**Version:** 2.0  
**Date:** February 19, 2026  
**Status:** Complete ✅  
**Feature:** Invalid Gesture Detection with Interactive Help System  

**Support:** See USER_GUIDE_V2.md for usage instructions
