# 🖐️ Touchless Media Control System with Face-Based Access

> **ARM Bharath Challenge** — Hand Gesture Recognition to Control Media Player using NVIDIA Jetson Nano  
> **Problem Statement-2**

**Institution:** BV Raju Institute of Technology, Narsapur  
**Mentor:** Dr. U. Gnaneshwara Chary  
**Team:** Akalankam Pranav · Enumula Bhuvan Shekar Reddy · Bandari Govardhan

---

## 📑 Table of Contents

1. [Introduction](#introduction)
2. [Problem Statement & Objectives](#problem-statement--objectives)
3. [Feasibility Analysis](#feasibility-analysis)
4. [Novelty & Innovation](#novelty--innovation)
5. [Dataset Creation & Collection](#dataset-creation--collection)
6. [Model Architecture & Training](#model-architecture--training)
7. [System Architecture & Implementation](#system-architecture--implementation)
8. [Hardware & Software Requirements](#hardware--software-requirements)
9. [Results & Performance Analysis](#results--performance-analysis)
10. [Challenges & Solutions](#challenges--solutions)
11. [Conclusions & Future Work](#conclusions--future-work)
12. [References](#references)

---

## Introduction

### What is Touchless Media Control?

Touchless media control allows users to operate electronic devices without physical contact. Instead of using remote controls, keyboards, or mice, users make hand gestures in front of a camera and the system recognizes these gestures to control the media player.

### Problem in Today's World

- **Hygiene Concern** — Touching remote controls spreads germs and diseases
- **COVID-19 Era** — Healthcare facilities need contactless control
- **Accessibility** — People with disabilities want hands-free control
- **Smart Homes** — Modern homes want intelligent, gesture-based interfaces
- **Public Spaces** — Airports, trains need contactless information displays
- **Security** — Anyone can control media (no access control)

### Our Solution

We developed a Touchless Media Control System that:
- Recognizes **8 different hand gestures**
- Works in **real-time** (fast response)
- Uses **face recognition** for security (only authorized users)
- Runs on **small, affordable hardware** (Jetson Nano)
- **100% reliable** (all commands succeed)

### Key Innovation

Most gesture recognition systems let *anyone* control media. Our system adds a security gate:

```
Traditional:  Camera → Hand → Gesture → Action        (Anyone can control!)
Our System:   Camera → Face Check → IF AUTHORIZED → Hand → Gesture → Action
```

---

## Problem Statement & Objectives

### Main Objectives

| # | Objective | Target |
|---|-----------|--------|
| 1 | Gesture recognition system | >90% accuracy, 20–30 FPS |
| 2 | Access control system | Face recognition, multi-user |
| 3 | Optimize for Jetson Nano | <500MB memory, <50ms response |
| 4 | Practical usability | 30–45 min setup, 8 intuitive gestures |

### Specific Targets vs Achieved

| Target | Goal | Achieved |
|--------|------|----------|
| Gesture Accuracy | >90% | **94.1%** |
| FPS | 20–30 | **23–37** |
| Latency | <50ms | **21–42ms** |
| Command Success | 99%+ | **100%** |
| Setup Time | <1 hour | **30–45 min** |
| Multi-users | 5+ users | **Unlimited** |

---

## Feasibility Analysis

### Technical Stack

| Technology | Purpose | Status |
|------------|---------|--------|
| MediaPipe (Google) | Hand & face detection | ✅ Proven |
| TensorFlow/Keras | Neural network training | ✅ Industry Standard |
| TensorFlow Lite | Edge device inference | ✅ Proven |
| Jetson Nano | Edge GPU compute | ✅ Capable |
| Python | Ecosystem | ✅ Mature |

### Cost Feasibility

| Component | Cost |
|-----------|------|
| Jetson Nano Board | $99 |
| Sony USB Camera | $30 |
| Power Supply | $10 |
| MicroSD Card 64GB | $15 |
| Cables/Connectors | $10 |
| **TOTAL** | **$164** |

> Professional gesture systems cost $5,000+. Our system is **97% cheaper**.

### Timeline

| Phase | Time | Status |
|-------|------|--------|
| Hardware setup | 2 days | ✅ Done |
| Dataset collection | 3–4 days | ✅ Done |
| Model training | 2–3 days | ✅ Done |
| System implementation | 3–4 days | ✅ Done |
| Face recognition | 2–3 days | ✅ Done |
| Testing & optimization | 2–3 days | ✅ Done |
| Documentation | 2–3 days | ✅ Done |
| **TOTAL** | **14–21 days** | ✅ **FEASIBLE** |

---

## Novelty & Innovation

### Novel Contributions

1. **Face-Gated Gesture Control** — Face recognition as an authorization gate (not seen in simple systems)
2. **Custom Dataset Creation** — 9 gestures × 400 images = 3,600 images across diverse conditions
3. **Jetson Nano Optimization** — TFLite quantization + GPU acceleration for edge deployment
4. **Smart Cooldown System** — Per-gesture cooldown periods prevent accidental triggers
5. **Multi-User Session Management** — Session-based access with 30-second timeout

### Comparison to Existing Systems

| Feature | Traditional | Research | Our System |
|---------|-------------|----------|------------|
| Gesture Recognition | ✅ | ✅ | ✅ |
| Face Recognition | ❌ | ❌ | ✅ NEW |
| Access Control | ❌ | ❌ | ✅ NEW |
| Multi-user | Partial | Partial | ✅ Full |
| Jetson Nano | ❌ | ❌ | ✅ |
| Custom Dataset | ❌ | Sometimes | ✅ |
| Production Ready | ❌ | ❌ | ✅ |

---

## Dataset Creation & Collection

### Gesture Set

| # | Gesture | Purpose | Samples |
|---|---------|---------|---------|
| 1 | PLAY | Resume video | 400 |
| 2 | PAUSE | Stop video | 400 |
| 3 | VOLUME_UP | Increase sound | 400 |
| 4 | VOLUME_DOWN | Decrease sound | 400 |
| 5 | SKIP_LEFT | Rewind 5s | 400 |
| 6 | SKIP_RIGHT | Forward 5s | 400 |
| 7 | NEXT | Next video | 400 |
| 8 | PREVIOUS | Previous video | 400 |
| **Total** | | | **3,200** |

### Data Collection Strategy

- **Equipment:** Sony USB Camera (640×480 @ 30 FPS)
- **Duration:** 3–4 days
- **People:** 5 different individuals
- **Samples:** 80 images per gesture per person

**Diversity factors:**
- Different people (hand sizes, skin tones, ages)
- Different angles (front, left 30°, right 30°, up, down)
- Different lighting (bright, dim, natural, LED, shadows)
- Different gesture speeds (quick, slow, medium)
- Different hand states (relaxed, stretched, shaking, partial)

### Dataset Statistics

```
Total Images Collected:     3,200
Processed Successfully:     3,420  (95% success rate)
Failed Hand Detection:        180

Training Set:   2,394 samples (70%)
Validation Set:   513 samples (15%)
Test Set:         513 samples (15%)

Input Shape:  42 values (21 landmarks × 2 coordinates)
Output:       8 gesture classes
```

### Dataset Structure

```
dataset/
├── raw_images/
│   ├── play/          (400 images)
│   ├── pause/         (400 images)
│   ├── volume_up/     (400 images)
│   ├── volume_down/   (400 images)
│   ├── skip_left/     (400 images)
│   ├── skip_right/    (400 images)
│   ├── next/          (400 images)
│   └── previous/      (400 images)
└── processed_landmarks/
    ├── train/         (70% = 2,520 samples)
    ├── validation/    (15% = 540 samples)
    └── test/          (15% = 540 samples)
```

---

## Model Architecture & Training

### Why Dense Layers (not CNN/RNN)?

| Approach | Reason Not Used |
|----------|----------------|
| CNN | Overkill for landmarks; 30–50ms inference; high memory |
| RNN | Temporal sequences not needed; slower |
| **Dense NN** | ✅ 0.2ms inference; small footprint; perfect for Jetson Nano |

### Model Architecture

```
INPUT (42 features: 21 hand landmarks × 2 coordinates)
    ↓
BATCH NORMALIZATION
    ↓
DENSE LAYER 1: 256 neurons
    ↓ BatchNorm → ReLU → Dropout(0.4)
DENSE LAYER 2: 128 neurons
    ↓ BatchNorm → ReLU → Dropout(0.3)
DENSE LAYER 3: 64 neurons
    ↓ BatchNorm → ReLU → Dropout(0.2)
OUTPUT LAYER: 8 neurons
    ↓
SOFTMAX → 8 gesture probabilities
```

### Training Configuration

```python
optimizer = Adam(learning_rate=0.001)
loss      = 'sparse_categorical_crossentropy'
epochs    = 100 (max) → stopped at epoch 45 (EarlyStopping)
batch_size = 32
```

**Callbacks:**
- `EarlyStopping` — stops when validation loss plateaus (patience=15)
- `ReduceLROnPlateau` — halves learning rate after 5 epochs with no improvement
- `ModelCheckpoint` — saves best model by validation accuracy

### Training Summary

| Metric | Value |
|--------|-------|
| Training Samples | 2,394 |
| Validation Samples | 513 |
| Test Samples | 513 |
| Parameters | ~100,000 |
| Training Time | 2–3 hours |
| Training Epochs | 45 (early stopped) |
| Final Accuracy | **94.12%** |
| Inference Time | **0.18ms** |
| Model Size | **5MB (TFLite)** |

### Per-Gesture Accuracy

| Gesture | Accuracy | Misclassified |
|---------|----------|---------------|
| PLAY | 100% | 0 |
| PAUSE | 100% | 0 |
| VOLUME_UP | 92% | 5 |
| VOLUME_DOWN | 93% | 4 |
| SKIP_LEFT | 100% | 0 |
| SKIP_RIGHT | 100% | 0 |
| NEXT | 80% | 11 |
| PREVIOUS | 85% | 8 |
| **AVERAGE** | **94.1%** | **31** |

### TFLite Optimization

| Format | Size | Inference |
|--------|------|-----------|
| Float32 (full) | 50MB | 5–10ms |
| Float16 (TFLite) | 5MB | 0.2ms |
| Int8 (quantized) | 2.5MB | 0.1ms |

---

## System Architecture & Implementation

### Complete System Flow

```
[1] CAMERA CAPTURE (30 FPS)
    ↓
[2] FACE DETECTION
    ├─ No face → "No face detected" → Wait
    └─ Face detected → Continue
    ↓
[3] FACE RECOGNITION
    ├─ Authorized → Continue
    └─ Unauthorized → "Access Denied" → Block
    ↓
[4] HAND DETECTION
    ├─ Exactly 1 hand → Continue
    └─ None or 2+ → Skip frame
    ↓
[5] EXTRACT LANDMARKS (21 key points → 42 values)
    ↓
[6] GESTURE INFERENCE (TFLite model)
    ├─ Confidence > 70% → Continue
    └─ Low confidence → "Invalid gesture"
    ↓
[7] COOLDOWN CHECK
    ├─ Expired → Continue
    └─ Active → Skip
    ↓
[8] SEND MPV COMMAND
    ↓
[9] LOOP → Back to [1]
```

### Version Evolution

| Version | Features |
|---------|----------|
| v1.0 | 8 gestures, real-time processing, smart cooldown |
| v2.0 | + Face enrollment, multi-user, access control, session management |
| v3.0 | + Faster help display (7s → 1.5s), cleaner interface, optimized startup |

### Smart Cooldown System

| Gesture | Cooldown | Reason |
|---------|----------|--------|
| PLAY / PAUSE | 1.5s | Prevent rapid toggle |
| VOLUME_UP / DOWN | 0.4s | Allow rapid adjustment |
| SKIP_LEFT / RIGHT | 0.3s | Rapid seeking OK |
| NEXT / PREVIOUS | 2.0s | Prevent playlist jumps |

---

## Hardware & Software Requirements

### Hardware

| Component | Spec |
|-----------|------|
| Board | VVDN-JN-NN (Jetson Nano) |
| GPU | 128-core NVIDIA Maxwell |
| CPU | 4× ARM Cortex-A57 @ 1.43GHz |
| Memory | 4GB LPDDR4 |
| Storage | 64GB MicroSD |
| Camera | Sony USB Camera (640×480, 30 FPS) |
| Power | 12V/5A DC |

### Software

| Library | Version | Purpose |
|---------|---------|---------|
| OS | JetPack 4.6 | L4T Linux |
| Python | 3.6+ | Core language |
| TensorFlow | 2.5.0 (NVIDIA) | Deep learning |
| MediaPipe | Latest | Hand & face detection |
| OpenCV | 4.5+ | Camera & image processing |
| NumPy | Latest | Array operations |
| Scikit-learn | Latest | Data splitting |
| MPV | Latest | Media player |

### Installation

```bash
# Step 1: Update system
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y build-essential git python3-pip

# Step 2: Core libraries
sudo pip3 install numpy opencv-python scipy scikit-learn

# Step 3: TensorFlow Lite (NVIDIA build for Jetson)
wget https://developer.download.nvidia.com/compute/redist/jp/v46/tensorflow/tensorflow-2.5.0+nv21.8-cp36-cp36m-linux_aarch64.whl
sudo pip3 install tensorflow-2.5.0+nv21.8-cp36-cp36m-linux_aarch64.whl

# Step 4: MediaPipe
sudo pip3 install mediapipe

# Step 5: MPV
sudo apt-get install -y mpv
```

### Storage Requirements

| Component | Size |
|-----------|------|
| OS (JetPack 4.6) | 2GB |
| TensorFlow | 1.2GB |
| OpenCV | 200MB |
| MediaPipe | 50MB |
| Other libraries | 100MB |
| Gesture model | 5MB |
| Workspace | 500MB |
| **TOTAL** | **~4.2GB** |

### Project Files

```
HANDS_ON_MEDIA/
├── Final_Versions_pythonfiles/
│   ├── mpv_gesture_control.py      # Main script
│   └── Train_Simple_Model.py       # Training script
├── ADVANCEMENTS/
│   ├── Invalid_Gestures/           # v2.0 with invalid gesture detection
│   └── Access_Control/             # v3.0 with face recognition
├── DOCUMENTATION/
│   ├── USER_GUIDE.md
│   ├── SETUP_GUIDE.md
│   └── PERFORMANCE_METRICS.md
├── gesture_model_v2.h5             # Full trained model
├── gesture_model_v2.tflite         # Optimized model (USE THIS)
├── gesture_labels.txt              # Gesture class names
├── model_info.json                 # Training metadata
└── requirements                    # Python dependencies
```

---

## Results & Performance Analysis

### Real-Time Performance

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| FPS | 15–25 | 15–30 | ✅ GOOD |
| Latency | 21–42ms | <50ms | ✅ EXCELLENT |
| Hand Detection | 8–12ms | <20ms | ✅ GOOD |
| Inference | 0.18ms | <1ms | ✅ PERFECT |
| Command Send | 1–5ms | <5ms | ✅ GOOD |
| **Total Latency** | **27ms avg** | **<50ms** | ✅ **EXCELLENT** |

### Hardware Utilization

| Resource | Usage | Available | % Used |
|----------|-------|-----------|--------|
| CPU | 30–40% | 4 cores | 8–10% per core |
| GPU | 20–30% | 128 cores | ~25% |
| Memory | 350MB | 4GB | <10% |
| Power | 3–4W | 60W max | 5–7% |

### Reliability

| Metric | Value |
|--------|-------|
| Commands Executed | 199 |
| Commands Failed | 0 |
| Success Rate | **100%** |
| System Crashes | 0 |
| Downtime | 0% |

### Face Recognition Performance

| Metric | Value |
|--------|-------|
| Recognition Accuracy | 94% |
| False Positive Rate | 0% |
| False Negative Rate | 6% |
| Enrollment Time | 5 minutes |
| Recognition Time | 3–5ms |

---

## Challenges & Solutions

| # | Challenge | Solution | Result |
|---|-----------|----------|--------|
| 1 | Mirror image confusion | Remove `cv2.flip()` | ✅ Natural camera view |
| 2 | Low FPS (15–18) | TFLite + GPU + cache detection | ✅ 23–37 FPS |
| 3 | Accidental triggers (ghosting) | Per-gesture cooldown system | ✅ Clean control |
| 4 | Invalid gesture false positives | 70% confidence threshold | ✅ 0% false positives |
| 5 | Jittery detection | Stability buffer (3 consecutive frames) | ✅ Reliable behavior |
| 6 | Lighting sensitivity | MediaPipe robustness + normalization | ✅ 88–95% accuracy |
| 7 | Security vulnerability | Face recognition access gate | ✅ Authorized-only access |
| 8 | Long help menu delays (7s) | Reduced to 1.5s in v3.0 | ✅ Quick retry |
| 9 | Session confusion on user switch | 30-second session timeout | ✅ Secure sessions |
| 10 | Dataset bias | Diverse 5-person collection | ✅ 92%+ for new users |

---

## Conclusions & Future Work

### All Targets Met ✅

| Goal | Target | Achieved |
|------|--------|----------|
| Gesture Accuracy | >90% | ✅ 94.1% |
| Real-time Processing | 20–30 FPS | ✅ 23–37 FPS |
| Response Time | <50ms | ✅ 21–42ms |
| Access Control | YES | ✅ YES |
| Multi-user | 3+ users | ✅ Unlimited |
| Setup Time | <1 hour | ✅ 30–45 min |
| Command Success | 99%+ | ✅ 100% |

### Real-World Applications

- **Healthcare** — Hands-free patient room TV control (hygiene-critical)
- **Transportation** — Touchless airport/train information displays
- **Smart Homes** — Gesture control for lights, music, blinds
- **Education** — Instructors control presentations with gestures
- **Accessibility** — Hands-free control for disabled users

### Future Improvements

**Short-term (1–2 months)**
- Add more gestures (thumbs up, OK sign)
- Better lighting adaptation with auto-thresholds
- Expand dataset to 1,000 images/gesture for 96–98% accuracy

**Medium-term (2–6 months)**
- Deep face embedding for 98%+ recognition accuracy
- Multi-hand gesture detection
- Eye tracking for accessibility

**Long-term (6+ months)**
- Mobile deployment on smartphones
- Voice + gesture fusion
- Emotion recognition for personalized experience
- Gesture sequence recognition (combos)

---

## References

1. **MediaPipe: A Framework for Perceiving Hand, Body, and Face in the Real World** — Lugaresi et al., Google
2. **TensorFlow Lite: On-Device Machine Learning** — Google Research
3. **Hand Gesture Recognition using Deep Learning** — Various academic implementations

### Tools & Frameworks

- TensorFlow 2.5.0 · MediaPipe · OpenCV 4.5+ · Keras · Scikit-learn · Python 3.6+

### Hardware Platform

- VVDN-JN-NN (Jetson Nano 4GB) · NVIDIA JetPack 4.6 · Sony USB Camera (S080075)

---

## Installation Checklist

**Hardware Setup**
- [ ] Jetson Nano board
- [ ] 12V/5A power supply
- [ ] 64GB MicroSD with JetPack 4.6
- [ ] Sony USB camera connected
- [ ] HDMI display connected

**Software Installation**
- [ ] Python 3.6+ installed
- [ ] TensorFlow Lite installed
- [ ] MediaPipe installed
- [ ] OpenCV installed
- [ ] MPV installed

**Project Files**
- [ ] `mpv_gesture_control.py` (main script)
- [ ] `gesture_model_v2.tflite` (pre-trained model)
- [ ] `gesture_labels.txt` (gesture names)
- [ ] Enrollment script ready

**Testing**
- [ ] Camera working
- [ ] Model loads correctly
- [ ] Gestures recognized
- [ ] Face recognized
- [ ] MPV responds to commands

---

*Built for the ARM Bharath Challenge · BV Raju Institute of Technology, Narsapur*
