# Touchless Media Control - Setup Guide
## Complete Installation & Configuration

**Last Updated:** February 19, 2026  
**Platform:** VVDN-JN-NN (Jetson Nano) + JetPack 4.6  
**Setup Time:** 30-45 minutes  
**Difficulty:** Beginner-Friendly ✅

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Hardware Setup](#hardware-setup)
3. [OS Installation](#os-installation)
4. [Dependency Installation](#dependency-installation)
5. [Project Setup](#project-setup)
6. [Testing & Verification](#testing--verification)
7. [Configuration](#configuration)
8. [Performance Tuning](#performance-tuning)
9. [Troubleshooting Setup](#troubleshooting-setup)

---

## System Requirements

### Minimum Hardware

```
✅ REQUIRED:
   - VVDN-JN-NN Board (Jetson Nano 4GB SOM + VVDN Carrier)
   - 12V/5A Power Supply (important: use correct voltage)
   - 64GB MicroSD Card (Class 10, V30+ recommended)
   - Sony USB Camera Model S080075
   - USB Keyboard + Mouse (for initial setup)
   - HDMI Display or TV (for output)

⚠️ OPTIONAL (but recommended):
   - Heatsink + Fan (VVDN board has built-in)
   - Ethernet cable (for internet during setup)
   - USB Hub (for multiple peripherals)
```

### Software Requirements

```
✅ OS:
   - VVDN_JN_NN_L4T32.6.1 (JetPack 4.6 + VVDN BSP)
   - Linux kernel 4.9+

✅ Python:
   - Python 3.6 or higher
   - pip3 package manager

✅ Core Libraries:
   - TensorFlow Lite 2.5+
   - MediaPipe 0.8+
   - OpenCV 4.5+
   - NumPy 1.19+

✅ Media Player:
   - MPV (latest version)

✅ Storage:
   - 10GB free space (OS + dependencies)
   - Video files (local storage preferred)
```

### Network

```
🌐 During Setup:
   - Internet required for:
     • Download OS image
     • Install packages
     • Download models & libraries
   - Ethernet cable recommended (faster)
   - USB WiFi adapter works too

🌐 During Operation:
   - NO internet required
   - Completely offline operation
   - Pure gesture control
```

---

## Hardware Setup

### Step 1: Prepare MicroSD Card

**What you need:**
- MicroSD card (64GB minimum, Class 10, V30+)
- Card reader
- Computer with USB port
- Card formatting tool

**What to do:**
```bash
# On your PC/Mac:
# 1. Insert MicroSD into reader
# 2. Identify drive letter (usually /dev/sdb or /dev/sdc)
# 3. Format card (delete all partitions)
# 4. Write OS image (see Step 2)
```

**Tools for formatting:**
- **Windows:** SD Card Formatter (recommended)
- **Mac:** Disk Utility
- **Linux:** gparted or `sudo mkfs.ext4 /dev/sdX`

⚠️ **Warning:** Formatting erases all data! Verify you selected correct drive!

### Step 2: Install JetPack OS

**Download OS Image:**
```bash
# Get VVDN-JN-NN specific image:
# VVDN_JN_NN_L4T32.6.1.tar.gz
# From: VVDN support website or provided USB

# Extract image:
tar -xzf VVDN_JN_NN_L4T32.6.1.tar.gz
```

**Write to MicroSD:**

**Option A: Using Balena Etcher (Recommended)**
```bash
# Download: https://www.balena.io/etcher/
# 1. Open Balena Etcher
# 2. Select image file
# 3. Select MicroSD card
# 4. Click "Flash" (wait 5-10 minutes)
# 5. Remove card when done
```

**Option B: Using dd (Linux/Mac)**
```bash
# Identify card (be very careful!)
diskutil list  # macOS
lsblk          # Linux

# Unmount
diskutil unmountDisk /dev/disk2  # macOS
sudo umount /dev/sdb*             # Linux

# Write image (slow, be patient)
sudo dd if=VVDN_JN_NN_L4T32.6.1.img of=/dev/disk2 bs=4M
# Takes 15-20 minutes

# Verify
diskutil eject /dev/disk2
```

### Step 3: Install MicroSD in VVDN-JN-NN

**What to do:**
```
1. Locate MicroSD slot on VVDN carrier board
2. Insert card (contacts facing inward)
3. Push until it clicks
4. Card should sit flush (not sticking out)
```

**✅ Check installation:**
- Card sits flush in slot
- Contacts visible and clean
- Board powers on with card installed

### Step 4: Power On VVDN-JN-NN

**Power Sequence:**
```
1. Connect 12V/5A power adapter to board
2. Green LED indicates power
3. Blue LED indicates activity
4. Wait 30-60 seconds for first boot
5. System should show Ubuntu login (if HDMI connected)
```

**First Boot (2-3 minutes):**
```
[Boot screen appears]
[Jetson Nano logo]
[Ubuntu logo]
[Login prompt]
```

⚠️ **Do NOT interrupt power during first boot!**

---

## OS Installation

### Step 5: Initial OS Configuration

**Login (First Time):**
```
Username: nano
Password: nano
```

**First-Time Setup:**
```bash
# Update package list
sudo apt-get update

# Upgrade system
sudo apt-get upgrade -y

# Install common tools
sudo apt-get install -y build-essential git wget curl

# This takes 5-10 minutes (be patient)
```

### Step 6: Network Configuration

**Ethernet (Recommended):**
```bash
# Plug in ethernet cable
# System auto-detects
# Check connection:
ifconfig
# Should show: inet 192.168.x.x (or similar)
```

**WiFi (Alternative):**
```bash
# If no ethernet available
sudo nmtui
# Use interface to connect to WiFi network
```

**Test Internet:**
```bash
ping google.com
# If working: CTRL+C to stop
# If failing: Check cable/WiFi settings
```

### Step 7: Enable VVDN Performance Features

```bash

# Lock GPU/CPU clocks to max
sudo jetson_clocks

# Verify MAXN mode
sudo nvpmodel -q
# Should show: Current NV Power Mode: MAXN

# Enable these at boot (optional):
sudo -s
echo "nvpmodel -m 0" >> /etc/rc.local
echo "jetson_clocks" >> /etc/rc.local
exit
```

---

## Dependency Installation

### Step 8: Install Python & Dependencies

**Python Setup:**
```bash
# Check Python version
python3 --version
# Should be 3.6 or higher

# Install pip3
sudo apt-get install -y python3-pip

# Upgrade pip
sudo pip3 install --upgrade pip

# Verify
python3 -m pip --version
# Should be 21.3 or higher
```

**Core Python Libraries:**
```bash
# NumPy (math)
sudo pip3 install numpy

# OpenCV (image processing)
sudo pip3 install opencv-python

# SciPy (scientific computing)
sudo pip3 install scipy

# Takes 5-10 minutes
```

### Step 9: Install TensorFlow Lite

```bash
# NVIDIA provides optimized TFLite wheel for Jetson
# Version: tensorflow-2.5.0 for JetPack 4.6

# Download NVIDIA's TensorFlow wheel
wget https://developer.download.nvidia.com/compute/redist/jp/v46/tensorflow/tensorflow-2.5.0+nv21.8-cp36-cp36m-linux_aarch64.whl

# Install
sudo pip3 install tensorflow-2.5.0+nv21.8-cp36-cp36m-linux_aarch64.whl

# Takes 10-15 minutes (large file)

# Verify
python3 -c "import tensorflow as tf; print(f'TensorFlow {tf.__version__} loaded')"
# Should show: TensorFlow 2.5.0 loaded
```

### Step 10: Install MediaPipe

**IMPORTANT:** MediaPipe requires special installation for Jetson Nano (ARM architecture). Standard `pip install mediapipe` will NOT work!

#### Step 10a: Install Swap File (Required for Installation)

```bash
# Clone swap installer
cd ~
git clone https://github.com/JetsonHacksNano/installSwapfile.git
cd installSwapfile/
./installSwapfile.sh

# This creates 6GB swap file (takes 2-3 minutes)
# Swap is required for MediaPipe installation

# Verify swap is active
swapon --show
# Should show: /mnt/swapfile with 6G size
```

#### Step 10b: Install MediaPipe Dependencies

```bash
# Install required system packages
sudo apt-get update
sudo apt-get install -y libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran

# Install Python dependencies with specific versions
sudo pip3 install -U pip testresources setuptools==49.6.0
sudo apt-get install -y python3-pip

# Install NumPy (specific version required)
sudo pip3 install -U --no-deps numpy==1.19.4 future==0.18.2 mock==3.0.5 keras_preprocessing==1.1.2 keras_applications==1.0.8 gast==0.4.0 protobuf pybind11 cython pkgconfig

# Install h5py (required for MediaPipe)
sudo env H5PY_SETUP_REQUIRES=0 pip3 install -U h5py==3.1.0

# Install OpenCV Python bindings
sudo apt-get install -y python3-opencv

# Takes 5-10 minutes total
```

#### Step 10c: Download and Install MediaPipe

```bash
# Clone MediaPipe pre-built wheels repository
cd ~
git clone https://github.com/PINTO0309/mediapipe-bin
cd mediapipe-bin

# The wheel file is located at:
# ~/mediapipe-bin/v0.8.5/v0.8.5/numpy119x/py36/mediapipe-0.8.5_cuda102-cp36-cp36m-linux_aarch64.whl

# Install the wheel (for Python 3.6)
pip3 install ~/mediapipe-bin/v0.8.5/v0.8.5/numpy119x/py36/mediapipe-0.8.5_cuda102-cp36-cp36m-linux_aarch64.whl

# Should complete successfully
# Takes 2-3 minutes
```

#### Step 10d: Fix Import Conflicts (CRITICAL!)

```bash
# If you have MediaPipe source code cloned, it will block the installation
# Check if ~/mediapipe folder exists
ls -la ~/mediapipe

# If it exists, rename it to avoid conflicts
mv ~/mediapipe ~/mediapipe-source

# Also rename if you have mediapipe-models
if [ -d ~/mediapipe-models ]; then
    # This is fine, keep it for model files
    echo "mediapipe-models exists - this is OK"
fi
```

#### Step 10e: Verify MediaPipe Installation

```bash
# Test import
python3 -c "import mediapipe as mp; print('MediaPipe works')"
# Should show: MediaPipe works

# Check MediaPipe contents
python3 << 'EOF'
import mediapipe as mp
print("MediaPipe module location:", mp.__file__)
contents = dir(mp)
if 'solutions' in contents:
    print("✓ MediaPipe installed correctly!")
else:
    print("✗ MediaPipe installation incomplete")
EOF
# Should show: ✓ MediaPipe installed correctly!

# Test MediaPipe Hands solution
python3 << 'EOF'
import mediapipe as mp
import cv2

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5
)

print("✓ MediaPipe Hands initialized successfully")
hands.close()
print("✓ MediaPipe is fully working!")
EOF
```

**Expected output:**
```
MediaPipe works
MediaPipe module location: /home/nano/.local/lib/python3.6/site-packages/mediapipe/__init__.py
✓ MediaPipe installed correctly!
[Some warnings about .tflite files - these are NORMAL]
✓ MediaPipe Hands initialized successfully
✓ MediaPipe is fully working!
```

#### Troubleshooting MediaPipe Installation

**Issue: "No module named mediapipe" after installation**

```bash
# Check if ~/mediapipe folder exists (this blocks imports!)
ls -la ~/mediapipe

# If exists, rename it
mv ~/mediapipe ~/mediapipe-source

# Try import again
python3 -c "import mediapipe as mp; print('OK')"
```

**Issue: "AttributeError: module 'mediapipe' has no attribute 'solutions'"**

This means Python is importing a folder instead of the package. Fix:

```bash
# Find and rename conflicting folders
mv ~/mediapipe ~/mediapipe-source
mv ~/mediapipe-models ~/mediapipe-models-data  # if exists

# Test again
python3 -c "import mediapipe as mp; print(dir(mp))"
# Should show 'solutions' in the list
```

**Issue: Warnings about missing .tflite model files**

```
W20260212 20:18:03.316799 tflite_model_loader.cc:32] Trying to resolve path manually as GetResourceContents failed: ; Can't find file: mediapipe/modules/palm_detection/palm_detection.tflite
```

These warnings are **NORMAL** and **can be ignored**. MediaPipe will download models automatically when needed. The system works despite these warnings.

### Step 11: Install Additional Libraries

```bash
# Socket (for MPV IPC) - usually built-in
# JSON (for data) - usually built-in
# Collections (for deque) - usually built-in

# Just verify
python3 << 'EOF'
import socket
import json
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
print("✅ All core libraries OK!")
EOF
```

### Step 12: Install MPV Media Player

```bash
# Install MPV
sudo apt-get install -y mpv

# Verify installation
which mpv
mpv --version
# Should show: mpv 0.27.x or higher

# Test MPV works
mpv --version 2>&1 | head -1
```

---

## Project Setup

### Step 13: Create Project Directory

```bash
# Create working directory
mkdir -p ~/hands_on_media
cd ~/hands_on_media

# Create subdirectories
mkdir -p modules scripts data

# Verify structure
ls -la
# Should show: modules/, scripts/, data/ folders

# Create __init__.py for modules (makes it a package)
touch modules/__init__.py
```

### Step 14: Copy Project Files

**Copy these files to ~/hands_on_media/:**

```
hands_on_media
|
└── gesture_model_v2.h5
|
└── gesture_model_v2.tflite
|
└── gesture_labels.txt
|
└── scripts/
    └── mpv_gesture_control.py

```

**Download files:**

```bash
cd ~/hands_on_media
# Option A: From GitHub/provided source
git clone https://[your-repo]/gesture-control
cp gesture-control/scripts/mpv_gesture_control.py   .
cp gesture-control/gesture_model_v2.tflite .
cp gesture-control/gesture_labels.txt .

# Option B: Copy from USB drive
cp /media/usb/mpv_gesture_control.py .
cp /media/usb/gesture_model_v2.tflite .
cp /media/usb/gesture_labels.txt .

# Verify files exist
ls -lh mpv_gesture_control.py gesture_model_v2.tflite gesture_labels.txt
# All should show sizes >1MB
```

### Step 15: Verify Installation

**Test all components load:**

```bash
cd ~/hands_on_media
python3 << 'EOF'
print("Testing imports...")
import cv2
print("✓ OpenCV")
import numpy as np
print("✓ NumPy")
import tensorflow as tf
print("✓ TensorFlow")
import mediapipe as mp
print("✓ MediaPipe")
import socket
print("✓ Socket")
print("\n✅ All imports successful!")
EOF
```

**Test file access:**

```bash
cd ~/hands_on_media
python3 << 'EOF'
import os
files = ['mpv_gesture_control.py', 'gesture_model_v2.tflite', 'gesture_labels.txt']
for f in files:
    if os.path.exists(f):
        size = os.path.getsize(f) / 1024 / 1024  # Convert to MB
        print(f"✓ {f}: {size:.1f}MB")
    else:
        print(f"✗ {f}: NOT FOUND")
EOF
```

---

## Testing & Verification

### Step 16: Test Camera

**Check Camera Detection:**

```bash
# List cameras
ls /dev/video*
# Should show: /dev/video0 (or similar)

# Test camera with Python
python3 << 'EOF'
import cv2
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("✅ Camera OK")
    ret, frame = cap.read()
    print(f"Frame size: {frame.shape}")
    cap.release()
else:
    print("❌ Camera NOT working")
EOF
```

**Physical Test:**
```bash
# Try opening live camera view
python3 << 'EOF'
import cv2
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if ret:
        cv2.imshow('Camera Test', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Failed to read frame")
        break
cap.release()
cv2.destroyAllWindows()
EOF
```

### Step 17: Test Model Loading

```bash
cd ~/hands_on_media
python3 << 'EOF'
import tensorflow as tf

# Load gesture model
MODEL_PATH = 'gesture_model_v2.tflite'
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
print(f"✅ Model loaded: {MODEL_PATH}")

# Load gesture labels
with open('gesture_labels.txt', 'r') as f:
    gestures = [line.strip() for line in f]
print(f"✅ Loaded {len(gestures)} gestures:")
for i, g in enumerate(gestures, 1):
    print(f"   {i}. {g}")
EOF
```

### Step 18: Test MPV Connection

```bash
# Terminal 1: Start MPV
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf ~/Videos/test.mp4

# Terminal 2: Test socket
python3 << 'EOF'
import socket
import json

try:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect('/tmp/mpvsocket')
    
    # Test pause command
    cmd = {'command': ['set_property', 'pause', True]}
    sock.sendall((json.dumps(cmd) + '\n').encode('utf-8'))
    
    print("✅ MPV socket working")
    sock.close()
except Exception as e:
    print(f"❌ MPV socket error: {e}")
EOF
```

### Step 19: Full System Test

```bash
cd ~/hands_on_media

# Terminal 1: Start MPV
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf ~/Videos/test.mp4

# Terminal 2: Run gesture control
python3 mpv_gesture_control.py

# You should see:
# - System initialization messages
# - "SYSTEM READY"
# - Camera window opens
# - Ready to make gestures
```

---

## Configuration

### Step 20: Adjust Settings (Optional)

**Edit mpv_gesture_control.py** to customize:

```bash
nano mpv_gesture_control.py
```

**Configurable Settings:**

```python
# Camera settings (line 35-38)
FRAME_WIDTH = 640          # 640x480 recommended
FRAME_HEIGHT = 480
CAMERA_INDEX = 0           # 0=first camera, 1=second, etc.

# Detection thresholds (line 40-46)
MIN_DETECTION_CONFIDENCE = 0.5   # Lower = more sensitive
CONFIDENCE_THRESHOLD = 0.70      # Gesture confidence needed
INVALID_GESTURE_THRESHOLD = 0.65  # (not used in gesture-only)

# Gesture cooldowns (line 48-58)
ACTION_COOLDOWNS = {
    'PLAY': 1.5,          # Adjust as needed
    'PAUSE': 1.5,
    # ... others
}
```

**Common Adjustments:**

```python
# For better lighting conditions:
MIN_DETECTION_CONFIDENCE = 0.6  # More sensitive

# For poor lighting:
MIN_DETECTION_CONFIDENCE = 0.4  # Less sensitive

# For stricter gesture recognition:
CONFIDENCE_THRESHOLD = 0.80     # More strict

# For looser recognition:
CONFIDENCE_THRESHOLD = 0.60     # More forgiving
```

---

## Performance Tuning

### Step 21: Maximize Performance

**Always run before each session:**

```bash
# Maximum performance mode
sudo nvpmodel -m 0

# Lock clocks to maximum
sudo jetson_clocks

# Verify MAXN mode
sudo nvpmodel -q
# Output: Current NV Power Mode: MAXN
```

**Monitor Performance:**

```bash
# Check temperature (should be <60°C)
cat /sys/devices/virtual/thermal/thermal_zone0/temp
# Divide by 1000 to get Celsius

# Check CPU frequency
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
# Should be 1479000+ (1.4+ GHz)

# Check if thermal throttling active
tegrastats
# Look for: Tfreq (thermal throttle frequency)
```

### Step 22: Startup Script (Optional)

**Create startup script for convenience:**

```bash
cat > ~/startup_gesture.sh << 'EOF'
#!/bin/bash
cd ~/hands_on_media
sudo nvpmodel -m 0
sudo jetson_clocks
echo "Performance mode enabled (MAXN)"
echo "Run gesture control: python3 mpv_gesture_control.py"
EOF

chmod +x ~/startup_gesture.sh
```

**Use it:**
```bash
~/startup_gesture.sh
```

---

## Troubleshooting Setup

### Issue: TensorFlow Installation Fails

**Error:**
```
ERROR: No module named 'tensorflow'
```

**Solution:**
```bash
# Verify JetPack version
cat /etc/nv_tegra_release
# Should show: JetPack 4.6

# Download correct NVIDIA wheel for JetPack 4.6
wget https://developer.download.nvidia.com/compute/redist/jp/v46/tensorflow/tensorflow-2.5.0+nv21.8-cp36-cp36m-linux_aarch64.whl

# Install
sudo pip3 install tensorflow-2.5.0+nv21.8-cp36-cp36m-linux_aarch64.whl

# Test
python3 -c "import tensorflow as tf; print(tf.__version__)"
```

### Issue: MediaPipe Installation Hangs

**Symptom:**
```
Installation appears stuck or very slow
```

**Solution:**
```bash
# Increase timeout
pip3 install --default-timeout=1000 mediapipe

# BETTER: Use pre-built wheel for Jetson Nano
cd ~
git clone https://github.com/PINTO0309/mediapipe-bin
pip3 install ~/mediapipe-bin/v0.8.5/v0.8.5/numpy119x/py36/mediapipe-0.8.5_cuda102-cp36-cp36m-linux_aarch64.whl
```

### Issue: MediaPipe Import Error "No attribute 'solutions'"

**Error:**
```
AttributeError: module 'mediapipe' has no attribute 'solutions'
```

**Cause:** Python is importing ~/mediapipe folder instead of the installed package

**Solution:**
```bash
# Rename conflicting folder
mv ~/mediapipe ~/mediapipe-source

# Verify fix
python3 << 'EOF'
import mediapipe as mp
print("MediaPipe location:", mp.__file__)
if 'solutions' in dir(mp):
    print("✓ Fixed! MediaPipe working")
else:
    print("✗ Still broken")
EOF
```

### Issue: MediaPipe .tflite Warnings

**Warning:**
```
W20260212 20:18:03.316799 tflite_model_loader.cc:32] 
Trying to resolve path manually as GetResourceContents failed: 
Can't find file: mediapipe/modules/palm_detection/palm_detection.tflite
```

**This is NORMAL and can be ignored!**
- MediaPipe downloads models automatically when needed
- Warnings appear during initialization
- System works perfectly despite warnings
- DO NOT try to manually download .tflite files

### Issue: Camera Not Detected

**Error:**
```
No camera found at /dev/video0
```

**Solution:**
```bash
# Check USB connections
lsusb
# Should show Sony camera

# Try different camera index
python3 << 'EOF'
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"✓ Camera found at /dev/video{i}")
        cap.release()
    else:
        print(f"✗ No camera at /dev/video{i}")
EOF

# Update CAMERA_INDEX in mpv_gesture_control.py if needed
```

### Issue: MPV Socket Error

**Error:**
```
Could not connect to /tmp/mpvsocket
```

**Solution:**
```bash
# Ensure MPV running with socket
ps aux | grep mpv
# Should show mpv process

# Kill and restart MPV
pkill mpv
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf video.mp4 &

# Verify socket created
ls -l /tmp/mpvsocket
# Should show: srw-rw-rw-
```

### Issue: Low FPS (<15)

**Cause:**
```
Performance mode not enabled
Background apps running
```

**Solution:**
```bash
# Enable MAXN mode
sudo nvpmodel -m 0
sudo jetson_clocks

# Close unnecessary apps
pkill chrome
pkill firefox

# Check temperature
cat /sys/devices/virtual/thermal/thermal_zone0/temp
# If >70°C, reduce workload
```

### Issue: Model Loading Error

**Error:**
```
Could not open gesture_model_v2.tflite
```

**Solution:**
```bash
# Verify file exists
ls -lh gesture_model_v2.tflite
# Should be >5MB

# Verify file is readable
file gesture_model_v2.tflite
# Should show: data

# Verify working directory
pwd
# Should be ~/hands_on_media

# Run from correct directory
cd ~/hands_on_media
python3 mpv_gesture_control.py
```

---

## Verification Checklist

Before considering setup complete, verify:

```
☐ VVDN-JN-NN board powers on (green LED)
☐ JetPack 4.6 installed and boots
☐ Python 3.6+ installed
☐ TensorFlow 2.5+ working
☐ MediaPipe installed
☐ OpenCV installed
☐ Camera detected and working
☐ Gesture model loads
☐ Gesture labels load (9 gestures)
☐ MPV installed
☐ MPV socket working
☐ MAXN performance mode enabled
☐ System runs without errors
☐ Camera window opens
☐ Gestures are recognized
☐ MPV responds to commands
```

---

## Quick Reference

### Before Each Session

```bash
cd ~/hands_on_media
sudo nvpmodel -m 0
sudo jetson_clocks
python3 mpv_gesture_control.py
```

### Emergency Troubleshooting

```bash
# If system hangs
# Kill all
pkill python3
pkill mpv

# Restart
cd ~/hands_on_media
python3 mpv_gesture_control.py
```

### Useful Commands

```bash
# Check system stats
tegrastats

# Check thermal info
cat /sys/devices/virtual/thermal/thermal_zone0/temp

# Monitor disk space
df -h

# Check processes
ps aux | grep python3

# Network test
ping google.com
```

---

## Support & Next Steps

### Setup Complete! ✅

You're ready to use touchless gesture control!

**Next:** Read [USER_GUIDE.md](USER_GUIDE.md)

### Getting Help

If issues persist:

1. **Check [USER_GUIDE.md](USER_GUIDE.md) Troubleshooting**
2. **Review this Setup Guide's Troubleshooting section**
3. **Provide error output from terminal**
4. **Run diagnostic:**

```bash
python3 << 'EOF'
import os
import sys
print("System Info:")
print(f"Python: {sys.version}")
print(f"Working dir: {os.getcwd()}")
print(f"Files: {os.listdir('.')}")

try:
    import tensorflow as tf
    print(f"✓ TensorFlow {tf.__version__}")
except: print("✗ TensorFlow")

try:
    import mediapipe as mp
    print(f"✓ MediaPipe")
except: print("✗ MediaPipe")

try:
    import cv2
    print(f"✓ OpenCV {cv2.__version__}")
except: print("✗ OpenCV")
EOF
```

---

**Date:** February 19, 2026  
**Status:** Complete ✅  


