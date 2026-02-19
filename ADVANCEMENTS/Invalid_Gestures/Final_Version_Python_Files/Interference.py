#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MPV Gesture Control - VERSION 1.0 (Enhanced)
Smart Per-Gesture Cooldown + Invalid Gesture Detection + No Mirror

Improvements:
- Per-gesture cooldown for better UX
- Invalid gesture detection with help display
- No mirror image (natural camera view)
- Confidence-based adjustments
- Optimized configuration
"""

import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import socket
import json
import time
from collections import deque
import os

# ==================== OPTIMIZED CONFIGURATION ====================
# Model paths
MODEL_PATH = 'gesture_model_v2.tflite'
LABELS_PATH = 'gesture_labels.txt'
MPV_SOCKET = '/tmp/mpvsocket'

# Camera settings
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CAMERA_INDEX = 0

# MediaPipe settings - 0.5 is faster than 0.6 on Jetson Nano
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE  = 0.5

# Gesture recognition
CONFIDENCE_THRESHOLD = 0.70
STABLE_FRAMES = 3

# Invalid gesture threshold
INVALID_GESTURE_THRESHOLD = 0.65  # Below this = invalid gesture

# Smart Per-Gesture Cooldown
ACTION_COOLDOWNS = {
    'PLAY': 1.5,          # Stable - prevent accidental toggles
    'PAUSE': 1.5,         # Stable - prevent accidental toggles
    'VOLUME_UP': 0.4,     # Fast - allow rapid adjustment
    'VOLUME_DOWN': 0.4,   # Fast - allow rapid adjustment
    'SKIP_RIGHT': 0.3,    # Very fast - allow rapid seeking
    'SKIP_LEFT': 0.3,     # Very fast - allow rapid seeking
    'NEXT': 2.0,          # Slow - rare action, prevent mistakes
    'PREVIOUS': 2.0,      # Slow - rare action, prevent mistakes
    'STOP': 3.0           # Very slow - critical action
}

# Gesture help table: (Gesture, Hand Position, Hand Required)
GESTURE_HELP = [
    ('PLAY',        'Index & middle fingers up',   'Either    '),
    ('PAUSE',       'Open palm',                   'Either    '),
    ('VOLUME_UP',   'Index finger up',             'Either    '),
    ('VOLUME_DOWN', 'Index finger down',           'Either    '),
    ('SKIP_RIGHT',  'Thumb up + index,middle -->', 'LEFT hand '),
    ('SKIP_LEFT',   'Thumb up + index,middle <--', 'RIGHT hand'),
    ('NEXT',        'Thumb up + index -->',        'LEFT hand '),
    ('PREVIOUS',    'Thumb up + index <--',        'RIGHT hand'),
]

# Keep for other parts of the code
GESTURE_DESCRIPTIONS = {row[0]: row[1] for row in GESTURE_HELP}

# Help display timing
HELP_SHOW_DURATION   = 5.0   # Show gesture table for 5 seconds
HELP_RESUME_DURATION = 2.0   # Then show "Let's continue" for 2 seconds

# ==================== SMART COOLDOWN MANAGER ====================
class SmartCooldownManager:
    """Intelligent cooldown system with per-gesture timing"""
    
    def __init__(self, base_cooldowns):
        self.base_cooldowns = base_cooldowns
        self.last_execution_times = {}
        self.gesture_counts = {}
        self.total_attempts = {}
        
    def can_execute(self, gesture, confidence):
        """Check if gesture can be executed"""
        current_time = time.time()
        
        # Get base cooldown for this gesture
        base_cooldown = self.base_cooldowns.get(gesture, 1.0)
        
        # Adjust cooldown based on confidence
        if confidence > 0.95:
            cooldown = base_cooldown * 0.9
        elif confidence < 0.80:
            cooldown = base_cooldown * 1.1
        else:
            cooldown = base_cooldown
        
        # Initialize tracking
        if gesture not in self.last_execution_times:
            self.last_execution_times[gesture] = 0
            self.gesture_counts[gesture] = 0
            self.total_attempts[gesture] = 0
        
        self.total_attempts[gesture] += 1
        
        # Check cooldown
        time_since_last = current_time - self.last_execution_times[gesture]
        
        if time_since_last >= cooldown:
            self.last_execution_times[gesture] = current_time
            self.gesture_counts[gesture] += 1
            return True
        
        return False
    
    def get_stats(self):
        """Get execution statistics per gesture"""
        stats = {}
        for gesture in self.gesture_counts:
            executed = self.gesture_counts[gesture]
            attempted = self.total_attempts[gesture]
            stats[gesture] = {
                'executed': executed,
                'attempted': attempted,
                'rate': (executed / attempted * 100) if attempted > 0 else 0
            }
        return stats

# ==================== MPV CONTROLLER ====================
class MPVController:
    """Handle MPV IPC communication"""
    
    def __init__(self, socket_path):
        self.socket_path = socket_path
        self.command_count = 0
        self.failed_commands = 0
        self.command_times = deque(maxlen=100)
        self.commands_by_gesture = {}
        
    def send_command(self, command):
        """Send JSON command to MPV"""
        start_time = time.time()
        
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self.socket_path)
            
            cmd_json = json.dumps(command) + '\n'
            sock.sendall(cmd_json.encode('utf-8'))
            
            sock.settimeout(0.05)
            try:
                response = sock.recv(4096).decode('utf-8')
            except socket.timeout:
                response = None
            
            sock.close()
            
            execution_time = (time.time() - start_time) * 1000
            self.command_times.append(execution_time)
            self.command_count += 1
            
            return True, response, execution_time
            
        except Exception as e:
            self.failed_commands += 1
            return False, str(e), 0
    
    def execute_gesture(self, gesture):
        """Map gesture to MPV command"""
        
        commands_map = {
            'PLAY': {'command': ['set_property', 'pause', False]},
            'PAUSE': {'command': ['set_property', 'pause', True]},
            'VOLUME_UP': {'command': ['add', 'volume', 5]},
            'VOLUME_DOWN': {'command': ['add', 'volume', -5]},
            'NEXT': {'command': ['playlist-next']},
            'PREVIOUS': {'command': ['playlist-prev']},
            'SKIP_RIGHT': {'command': ['seek', 5]},
            'SKIP_LEFT': {'command': ['seek', -5]},
            'STOP': {'command': ['stop']}
        }
        
        descriptions = {
            'PLAY': 'Play', 'PAUSE': 'Pause',
            'VOLUME_UP': 'Vol+5%', 'VOLUME_DOWN': 'Vol-5%',
            'NEXT': 'Next', 'PREVIOUS': 'Prev',
            'SKIP_RIGHT': '+5s', 'SKIP_LEFT': '-5s', 'STOP': 'Stop'
        }
        
        if gesture in commands_map:
            success, response, exec_time = self.send_command(commands_map[gesture])
            
            if gesture not in self.commands_by_gesture:
                self.commands_by_gesture[gesture] = 0
            self.commands_by_gesture[gesture] += 1
            
            return success, descriptions.get(gesture, gesture), exec_time
        
        return False, "Unknown", 0
    
    def get_avg_command_time(self):
        if len(self.command_times) > 0:
            return np.mean(self.command_times)
        return 0.0

# ==================== PERFORMANCE METRICS ====================
class PerformanceMetrics:
    """Track detailed performance metrics"""
    
    def __init__(self, window_size=30):
        self.fps_times = deque(maxlen=window_size)
        self.inference_times = deque(maxlen=window_size)
        self.hand_detection_times = deque(maxlen=window_size)
        self.frame_times = deque(maxlen=window_size)
        self.total_predictions = 0
        self.correct_predictions = 0
        self.invalid_gesture_count = 0
        self.start_time = time.time()
        self.gesture_executions = {}
        
    def update_frame_time(self, duration):
        self.frame_times.append(duration)
        
    def update_fps(self):
        self.fps_times.append(time.time())
        
    def update_inference(self, duration):
        self.inference_times.append(duration)
        
    def update_hand_detection(self, duration):
        self.hand_detection_times.append(duration)
    
    def record_prediction(self):
        self.total_predictions += 1
    
    def record_execution(self, gesture):
        self.correct_predictions += 1
        if gesture not in self.gesture_executions:
            self.gesture_executions[gesture] = 0
        self.gesture_executions[gesture] += 1
    
    def record_invalid_gesture(self):
        self.invalid_gesture_count += 1
        
    def get_fps(self):
        if len(self.fps_times) < 2:
            return 0.0
        time_diff = self.fps_times[-1] - self.fps_times[0]
        return len(self.fps_times) / time_diff if time_diff > 0 else 0.0
    
    def get_avg_inference_ms(self):
        return np.mean(self.inference_times) * 1000 if self.inference_times else 0.0
    
    def get_avg_hand_detection_ms(self):
        return np.mean(self.hand_detection_times) * 1000 if self.hand_detection_times else 0.0
    
    def get_avg_frame_time_ms(self):
        return np.mean(self.frame_times) * 1000 if self.frame_times else 0.0
    
    def get_total_latency_ms(self):
        return self.get_avg_hand_detection_ms() + self.get_avg_inference_ms()
    
    def get_accuracy(self):
        if self.total_predictions == 0:
            return 0.0
        return (self.correct_predictions / self.total_predictions) * 100

# ==================== HELP DISPLAY ====================
def draw_help_overlay(frame, invalid_count, phase):
    """
    Draw help overlay with gesture table.
    phase = 'table'   -> show gesture reference table
    phase = 'resume'  -> show "Let's continue" message
    """
    h, w, _ = frame.shape

    # Semi-transparent dark background
    overlay = frame.copy()
    cv2.rectangle(overlay, (15, 95), (w - 15, h - 15), (15, 15, 15), -1)
    cv2.addWeighted(overlay, 0.87, frame, 0.13, 0, frame)

    if phase == 'resume':
        # ---- "Let's continue" screen ----
        cv2.rectangle(frame, (15, 95), (w - 15, h - 15), (0, 200, 0), 3)
        cy = h // 2 - 30
        cv2.putText(frame, "Great! Let's continue...",
                    (60, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(frame, "Show a valid gesture to control MPV",
                    (40, cy + 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        return

    # ---- Gesture table screen ----
    cv2.rectangle(frame, (15, 95), (w - 15, h - 15), (0, 0, 220), 3)

    # Title
    cv2.putText(frame, "PLEASE USE THESE GESTURES TO CONTROL",
                (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.68, (0, 220, 255), 2)

    # Table header
    hdr_y = 160
    cv2.rectangle(frame, (20, hdr_y - 18), (w - 20, hdr_y + 6), (50, 50, 50), -1)
    cv2.putText(frame, " #  Gesture        Hand Position                 Hand Required",
                (25, hdr_y), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (180, 180, 180), 1)

    # Divider
    cv2.line(frame, (20, hdr_y + 10), (w - 20, hdr_y + 10), (80, 80, 80), 1)

    # Table rows
    row_y = hdr_y + 32
    for i, (gesture, hand_pos, hand_req) in enumerate(GESTURE_HELP):
        # Alternate row shading
        if i % 2 == 0:
            cv2.rectangle(frame, (20, row_y - 16), (w - 20, row_y + 8), (30, 30, 30), -1)

        # Number
        cv2.putText(frame, "{:d}".format(i + 1),
                    (28, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (150, 150, 150), 1)

        # Gesture name  (green)
        cv2.putText(frame, "{:<12}".format(gesture),
                    (50, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (0, 255, 80), 2)

        # Hand position  (white)
        cv2.putText(frame, hand_pos,
                    (190, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (220, 220, 220), 1)

        # Hand required  (yellow for specific hand, grey for either)
        req_color = (0, 220, 255) if 'hand' in hand_req.lower() and 'either' not in hand_req.lower() else (160, 160, 160)
        cv2.putText(frame, hand_req.strip(),
                    (480, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.42, req_color, 1)

        row_y += 28

    # Footer
    cv2.line(frame, (20, row_y + 2), (w - 20, row_y + 2), (80, 80, 80), 1)
    cv2.putText(frame, "Invalid gestures: {}".format(invalid_count),
                (28, row_y + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 100, 0), 1)
    cv2.putText(frame, "Make a valid gesture to continue...",
                (210, row_y + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 0), 2)

# ==================== MAIN APPLICATION ====================
def main():
    print("=" * 70)
    print("MPV GESTURE CONTROL - VERSION 1.0 (Enhanced)")
    print("Smart Cooldown + Invalid Gesture Detection + No Mirror")
    print("=" * 70)
    
    # Check MPV
    print("\n[STEP 1] Checking MPV connection...")
    if not os.path.exists(MPV_SOCKET):
        print("[-] MPV socket not found!")
        print("[!] Start: mpv --input-ipc-server=/tmp/mpvsocket --loop=inf video.mp4")
        return
    
    mpv = MPVController(MPV_SOCKET)
    success, _, _ = mpv.send_command({'command': ['get_property', 'pause']})
    if success:
        print("[+] MPV connected!")
    else:
        print("[!] MPV not responding")
    
    # Load TFLite Model
    print("\n[STEP 2] Loading TFLite model...")
    try:
        interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()
        
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        print("[+] TFLite model loaded!")
    except Exception as e:
        print("[-] Error: {}".format(e))
        return
    
    # Load labels
    print("\n[STEP 3] Loading gesture labels...")
    try:
        with open(LABELS_PATH, 'r') as f:
            GESTURES = [line.strip().upper() for line in f.readlines()]
        print("[+] Loaded {} valid gestures".format(len(GESTURES)))
    except Exception as e:
        print("[-] Error: {}".format(e))
        return
    
    # Initialize SmartCooldownManager
    print("\n[STEP 4] Initializing smart cooldown system...")
    cooldown_manager = SmartCooldownManager(ACTION_COOLDOWNS)
    print("[+] Per-gesture cooldowns configured")
    
    # Initialize MediaPipe - tracking mode is faster than detection mode
    print("\n[STEP 5] Initializing hand detection...")
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
        max_num_hands=1
    )
    print("[+] MediaPipe initialized!")
    
    # Initialize Camera
    print("\n[STEP 6] Opening camera...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[-] Cannot access camera!")
        return

    # IMPORTANT: Do NOT set MJPG on this camera - default codec is faster (25 FPS vs 13 FPS)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)   # keep buffer minimal to avoid stale frames

    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print("[+] Camera ready! (No mirror mode)")
    print("[*] Camera FPS: {:.0f} | Resolution: {}x{}".format(
        actual_fps, FRAME_WIDTH, FRAME_HEIGHT))
    
    print("\n" + "=" * 70)
    print("SYSTEM READY - VERSION 1.0 (Enhanced)")
    print("=" * 70)
    print("\n[FEATURES]")
    print("  - Smart per-gesture cooldown")
    print("  - Invalid gesture detection with help")
    print("  - No mirror image (natural view)")
    print("  - Fast volume/skip controls")
    print("\n[*] Press 'q' to quit")
    print("=" * 70 + "\n")
    
    # Initialize tracking
    metrics = PerformanceMetrics()
    prediction_buffer = deque(maxlen=5)
    confidence_buffer = deque(maxlen=5)
    action_history = deque(maxlen=10)
    
    current_gesture = None
    current_confidence = 0.0
    show_help = False
    help_display_time = 0
    help_phase = 'table'   # 'table' -> show gesture table, 'resume' -> show continue msg
    
    frame_count = 0
    
    try:
        while cap.isOpened():
            frame_start = time.time()
            
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            metrics.update_fps()
            
            # NO MIRROR - Keep original orientation
            # frame = cv2.flip(frame, 1)  # REMOVED!
            
            h, w, _ = frame.shape
            
            # Hand detection
            hand_detect_start = time.time()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            hand_detect_time = time.time() - hand_detect_start
            metrics.update_hand_detection(hand_detect_time)
            
            # Two-phase help display: table -> resume -> off
            if show_help:
                elapsed = time.time() - help_display_time
                if help_phase == 'table' and elapsed > HELP_SHOW_DURATION:
                    help_phase = 'resume'
                    help_display_time = time.time()
                elif help_phase == 'resume' and elapsed > HELP_RESUME_DURATION:
                    show_help = False
                    help_phase = 'table'
            
            # Draw UI Header
            cv2.rectangle(frame, (0, 0), (w, 120), (30, 30, 30), -1)
            cv2.putText(frame, "MPV Control v1.0 - No Mirror", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Performance metrics
            fps = metrics.get_fps()
            latency = metrics.get_total_latency_ms()
            accuracy = metrics.get_accuracy()
            avg_cmd_time = mpv.get_avg_command_time()
            
            met1 = "FPS:{:.1f} Lat:{:.0f}ms Cmd:{:.0f}ms".format(fps, latency, avg_cmd_time)
            cv2.putText(frame, met1, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 2)
            
            met2 = "Hand:{:.0f}ms Inf:{:.0f}ms Acc:{:.0f}% Invalid:{:d}".format(
                metrics.get_avg_hand_detection_ms(),
                metrics.get_avg_inference_ms(),
                accuracy,
                metrics.invalid_gesture_count
            )
            cv2.putText(frame, met2, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
            
            # Process hand
            if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 1:
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # Draw landmarks
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                    mp_drawing.DrawingSpec(color=(255, 100, 0), thickness=1)
                )
                
                # Extract landmarks
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y])
                landmarks = np.array(landmarks, dtype=np.float32).reshape(1, -1)
                
                # TFLite inference
                inference_start = time.time()
                interpreter.set_tensor(input_details[0]['index'], landmarks)
                interpreter.invoke()
                prediction = interpreter.get_tensor(output_details[0]['index'])[0]
                inference_time = time.time() - inference_start
                metrics.update_inference(inference_time)
                
                gesture_idx = np.argmax(prediction)
                confidence = prediction[gesture_idx]
                
                metrics.record_prediction()
                
                # Check if gesture is invalid (low confidence)
                if confidence < INVALID_GESTURE_THRESHOLD:
                    # Invalid gesture detected!
                    if not show_help:
                        metrics.record_invalid_gesture()
                        show_help = True
                        help_phase = 'table'
                        help_display_time = time.time()
                        print("[WARNING] Invalid gesture! Confidence: {:.1f}%".format(confidence * 100))
                    
                    # Clear buffers
                    prediction_buffer.clear()
                    confidence_buffer.clear()
                    current_gesture = None
                else:
                    # Valid gesture
                    prediction_buffer.append(gesture_idx)
                    confidence_buffer.append(confidence)
                    
                    # Stable gesture check
                    if len(prediction_buffer) >= STABLE_FRAMES:
                        unique, counts = np.unique(list(prediction_buffer), return_counts=True)
                        most_common_idx = unique[np.argmax(counts)]
                        most_common_count = np.max(counts)
                        
                        relevant_confidences = [
                            conf for pred, conf in zip(prediction_buffer, confidence_buffer)
                            if pred == most_common_idx
                        ]
                        avg_confidence = np.mean(relevant_confidences)
                        
                        if most_common_count >= STABLE_FRAMES and avg_confidence > CONFIDENCE_THRESHOLD:
                            gesture = GESTURES[most_common_idx]
                            current_gesture = gesture
                            current_confidence = avg_confidence
                            
                            # Execute with SMART COOLDOWN
                            if cooldown_manager.can_execute(gesture, avg_confidence):
                                success, description, exec_time = mpv.execute_gesture(gesture)
                                
                                if success:
                                    action_history.append({
                                        'gesture': gesture,
                                        'time': time.time(),
                                        'conf': avg_confidence,
                                        'exec': exec_time
                                    })
                                    metrics.record_execution(gesture)
                                    
                                    cooldown_used = ACTION_COOLDOWNS.get(gesture, 1.0)
                                    if avg_confidence > 0.95:
                                        cooldown_used *= 0.9
                                    elif avg_confidence < 0.80:
                                        cooldown_used *= 1.1
                                    
                                    print("[ACTION] {:<12} | {:.0f}% | {:.1f}ms | {:.2f}s CD | {}".format(
                                        gesture, avg_confidence * 100, exec_time, cooldown_used, description))
                
                # Display help overlay if invalid gesture
                if show_help:
                    draw_help_overlay(frame, metrics.invalid_gesture_count, help_phase)
                else:
                    # Display current gesture (only if valid)
                    if current_gesture:
                        colors = {
                            'VOLUME_UP': (0, 255, 0), 'VOLUME_DOWN': (0, 165, 255),
                            'PLAY': (255, 100, 0), 'PAUSE': (0, 0, 255),
                            'NEXT': (255, 0, 255), 'PREVIOUS': (255, 255, 0),
                            'STOP': (0, 0, 200), 'SKIP_LEFT': (150, 150, 0),
                            'SKIP_RIGHT': (0, 150, 150)
                        }
                        color = colors.get(current_gesture, (255, 255, 255))
                        
                        box_w = min(int(260 + len(current_gesture) * 8), w - 20)
                        cv2.rectangle(frame, (10, 140), (box_w, 240), color, -1)
                        cv2.rectangle(frame, (10, 140), (box_w, 240), (255, 255, 255), 2)
                        
                        cv2.putText(frame, current_gesture,
                                   (20, 185), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
                        
                        gesture_cd = ACTION_COOLDOWNS.get(current_gesture, 1.0)
                        cv2.putText(frame, "{:.0f}% | CD:{:.1f}s".format(
                            current_confidence * 100, gesture_cd),
                                   (20, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            else:
                prediction_buffer.clear()
                confidence_buffer.clear()
                
                if not show_help:
                    msg = "No hand" if not results.multi_hand_landmarks else "Multiple hands"
                    cv2.putText(frame, msg, (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                else:
                    draw_help_overlay(frame, metrics.invalid_gesture_count, help_phase)
            
            # Action history (only if not showing help)
            if action_history and not show_help:
                hy = h - 140
                cv2.putText(frame, "Recent:", (w - 220, hy), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
                for act in list(action_history)[-5:]:
                    hy += 22
                    cv2.putText(frame, "{} ({:.0f}s)".format(
                        act['gesture'][:8], time.time() - act['time']),
                               (w - 220, hy), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (150, 150, 150), 1)
            
            # MPV status
            st = "MPV: {}/{}".format(mpv.command_count, mpv.failed_commands)
            cv2.putText(frame, st, (w - 150, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
            
            # Display
            cv2.imshow('MPV Gesture Control v1.0', frame)
            
            # Frame time
            frame_time = time.time() - frame_start
            metrics.update_frame_time(frame_time)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n\n[*] Shutting down...")
                break
    
    except KeyboardInterrupt:
        print("\n\n[*] Interrupted...")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()
        
        # Final report
        print("\n" + "=" * 70)
        print("FINAL REPORT - VERSION 1.0 (Enhanced)")
        print("=" * 70)
        
        print("\n[TIMING]")
        print("  FPS: {:.2f}".format(metrics.get_fps()))
        print("  Latency: {:.2f}ms".format(metrics.get_total_latency_ms()))
        print("  Hand: {:.2f}ms | Inference: {:.2f}ms | Cmd: {:.2f}ms".format(
            metrics.get_avg_hand_detection_ms(),
            metrics.get_avg_inference_ms(),
            mpv.get_avg_command_time()
        ))
        
        print("\n[ACCURACY]")
        print("  Prediction Accuracy: {:.2f}%".format(metrics.get_accuracy()))
        print("  Commands Executed: {}".format(metrics.correct_predictions))
        print("  Invalid Gestures: {}".format(metrics.invalid_gesture_count))
        
        print("\n[MPV]")
        print("  Success: {} | Failed: {}".format(mpv.command_count, mpv.failed_commands))
        
        print("\n[COOLDOWN STATS]")
        for gesture in sorted(cooldown_manager.get_stats().keys()):
            stats = cooldown_manager.get_stats()[gesture]
            cd = ACTION_COOLDOWNS.get(gesture, 1.0)
            print("  {:<12} CD:{:.1f}s Exec:{:3d} Rate:{:5.1f}%".format(
                gesture, cd, stats['executed'], stats['rate']
            ))
        
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
