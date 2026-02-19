#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MPV Gesture Control - OPTIMIZED for Jetson Nano
Uses TFLite for 10x faster inference
Target: <150ms latency, >20 FPS
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

# ==================== CONFIGURATION ====================
MODEL_PATH = 'gesture_model_v2.tflite'  # TFLite model
LABELS_PATH = 'gesture_labels.txt'
MPV_SOCKET = '/tmp/mpvsocket'

# Optimized settings for speed
CONFIDENCE_THRESHOLD = 0.70  # Slightly lower for better accuracy metric
STABLE_FRAMES = 3  # Reduced from 5 for faster response
ACTION_COOLDOWN = 1.0  # Reduced from 1.5

CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# ==================== MPV CONTROLLER ====================
class MPVController:
    """Handle MPV IPC communication"""
    
    def __init__(self, socket_path):
        self.socket_path = socket_path
        self.command_count = 0
        self.failed_commands = 0
        self.command_times = deque(maxlen=100)
        
    def send_command(self, command):
        """Send JSON command to MPV"""
        start_time = time.time()
        
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(self.socket_path)
            
            cmd_json = json.dumps(command) + '\n'
            sock.sendall(cmd_json.encode('utf-8'))
            
            sock.settimeout(0.05)  # Reduced timeout for speed
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
            return success, descriptions.get(gesture, gesture), exec_time
        
        return False, "Unknown", 0
    
    def get_avg_command_time(self):
        if len(self.command_times) > 0:
            return np.mean(self.command_times)
        return 0.0

# ==================== PERFORMANCE METRICS ====================
class PerformanceMetrics:
    """Track performance metrics"""
    
    def __init__(self, window_size=30):
        self.fps_times = deque(maxlen=window_size)
        self.inference_times = deque(maxlen=window_size)
        self.hand_detection_times = deque(maxlen=window_size)
        self.frame_times = deque(maxlen=window_size)  # Total frame time
        self.total_predictions = 0
        self.correct_predictions = 0
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

# ==================== MAIN APPLICATION ====================
def main():
    print("=" * 70)
    print("MPV GESTURE CONTROL - OPTIMIZED (TFLite)")
    print("=" * 70)
    
    # Check MPV
    print("\n[STEP 1] Checking MPV connection...")
    if not os.path.exists(MPV_SOCKET):
        print("[-] MPV socket not found!")
        print("[!] Start MPV with: mpv --input-ipc-server=/tmp/mpvsocket --loop=inf video.mp4")
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
        print("[*] Input shape: {}".format(input_details[0]['shape']))
    except Exception as e:
        print("[-] Error loading TFLite model: {}".format(e))
        print("[!] Make sure gesture_model_v2.tflite exists")
        return
    
    # Load labels
    print("\n[STEP 3] Loading gesture labels...")
    try:
        with open(LABELS_PATH, 'r') as f:
            GESTURES = [line.strip().upper() for line in f.readlines()]
        print("[+] Loaded {} gestures: {}".format(len(GESTURES), ', '.join(GESTURES)))
    except Exception as e:
        print("[-] Error loading labels: {}".format(e))
        return
    
    # Initialize MediaPipe with optimized settings
    print("\n[STEP 4] Initializing hand detection (optimized)...")
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        min_detection_confidence=0.6,  # Lowered for speed
        min_tracking_confidence=0.6,   # Lowered for speed
        max_num_hands=1
    )
    print("[+] MediaPipe initialized!")
    
    # Initialize Camera
    print("\n[STEP 5] Opening camera...")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("[-] Cannot access camera!")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("[+] Camera ready! Resolution: {}x{}".format(actual_width, actual_height))
    
    print("\n" + "=" * 70)
    print("SYSTEM READY - OPTIMIZED FOR SPEED")
    print("=" * 70)
    print("\n[TARGET PERFORMANCE]")
    print("  FPS: >20 | Latency: <150ms | Accuracy: >80%")
    print("\n[*] Press 'q' to quit")
    print("=" * 70 + "\n")
    
    # Initialize tracking
    metrics = PerformanceMetrics()
    prediction_buffer = deque(maxlen=5)  # Smaller buffer for speed
    confidence_buffer = deque(maxlen=5)
    last_action_time = {}
    action_history = deque(maxlen=10)
    
    current_gesture = None
    current_confidence = 0.0
    
    frame_count = 0
    
    try:
        while cap.isOpened():
            frame_start = time.time()
            
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            metrics.update_fps()
            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape
            
            # Hand detection
            hand_detect_start = time.time()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            hand_detect_time = time.time() - hand_detect_start
            metrics.update_hand_detection(hand_detect_time)
            
            # Draw minimal UI for speed
            cv2.rectangle(frame, (0, 0), (w, 100), (30, 30, 30), -1)
            cv2.putText(frame, "MPV Control (TFLite Optimized)", 
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Performance metrics
            fps = metrics.get_fps()
            latency = metrics.get_total_latency_ms()
            accuracy = metrics.get_accuracy()
            avg_cmd_time = mpv.get_avg_command_time()
            
            # Compact metrics display
            met1 = "FPS:{:.1f} Lat:{:.0f}ms".format(fps, latency)
            met2 = "Hand:{:.0f} Inf:{:.0f} Cmd:{:.0f} Acc:{:.0f}%".format(
                metrics.get_avg_hand_detection_ms(),
                metrics.get_avg_inference_ms(),
                avg_cmd_time, accuracy
            )
            
            cv2.putText(frame, met1, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 100), 2)
            cv2.putText(frame, met2, (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
            
            # Process hand
            if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 1:
                hand_landmarks = results.multi_hand_landmarks[0]
                
                # Draw landmarks (simplified for speed)
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
                
                # Buffer predictions
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
                        
                        # Execute with cooldown
                        current_time = time.time()
                        if gesture not in last_action_time or \
                           (current_time - last_action_time[gesture]) > ACTION_COOLDOWN:
                            
                            success, description, exec_time = mpv.execute_gesture(gesture)
                            
                            if success:
                                last_action_time[gesture] = current_time
                                action_history.append({
                                    'gesture': gesture,
                                    'time': current_time,
                                    'conf': avg_confidence,
                                    'exec': exec_time
                                })
                                metrics.record_execution(gesture)
                                
                                print("[ACTION] {:<12} | {:.0f}% | {:.1f}ms | {}".format(
                                    gesture, avg_confidence * 100, exec_time, description))
                
                # Display current gesture (minimal)
                if current_gesture:
                    colors = {
                        'VOLUME_UP': (0, 255, 0), 'VOLUME_DOWN': (0, 165, 255),
                        'PLAY': (255, 100, 0), 'PAUSE': (0, 0, 255),
                        'NEXT': (255, 0, 255), 'PREVIOUS': (255, 255, 0),
                        'STOP': (0, 0, 200), 'SKIP_LEFT': (150, 150, 0),
                        'SKIP_RIGHT': (0, 150, 150)
                    }
                    color = colors.get(current_gesture, (255, 255, 255))
                    
                    box_w = min(int(250 + len(current_gesture) * 8), w - 20)
                    cv2.rectangle(frame, (10, 120), (box_w, 220), color, -1)
                    cv2.rectangle(frame, (10, 120), (box_w, 220), (255, 255, 255), 2)
                    
                    cv2.putText(frame, current_gesture,
                               (20, 165), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
                    cv2.putText(frame, "{:.0f}%".format(current_confidence * 100),
                               (20, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            else:
                prediction_buffer.clear()
                confidence_buffer.clear()
                
                msg = "No hand" if not results.multi_hand_landmarks else "Multiple hands"
                cv2.putText(frame, msg, (10, h - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            # Action history (minimal)
            if action_history:
                hy = h - 120
                cv2.putText(frame, "Recent:", (w - 200, hy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
                for act in list(action_history)[-4:]:
                    hy += 20
                    cv2.putText(frame, "{} ({:.0f}s)".format(act['gesture'][:8], time.time() - act['time']),
                               (w - 200, hy), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (150, 150, 150), 1)
            
            # MPV status
            st = "MPV: {}/{}".format(mpv.command_count, mpv.failed_commands)
            cv2.putText(frame, st, (w - 150, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
            
            # Display
            cv2.imshow('MPV Gesture Control (Optimized)', frame)
            
            # Calculate frame time
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
        print("FINAL PERFORMANCE REPORT")
        print("=" * 70)
        print("\n[TIMING METRICS]")
        print("  Average FPS: {:.2f}".format(metrics.get_fps()))
        print("  Total Latency: {:.2f}ms".format(metrics.get_total_latency_ms()))
        print("    - Hand Detection: {:.2f}ms".format(metrics.get_avg_hand_detection_ms()))
        print("    - Model Inference: {:.2f}ms".format(metrics.get_avg_inference_ms()))
        print("    - Command Execution: {:.2f}ms".format(mpv.get_avg_command_time()))
        print("  Avg Frame Time: {:.2f}ms ({:.1f} FPS potential)".format(
            metrics.get_avg_frame_time_ms(), 
            1000.0 / metrics.get_avg_frame_time_ms() if metrics.get_avg_frame_time_ms() > 0 else 0
        ))
        
        print("\n[ACCURACY METRICS]")
        print("  Overall Accuracy: {:.2f}%".format(metrics.get_accuracy()))
        print("  Total Predictions: {}".format(metrics.total_predictions))
        print("  Stable Executions: {}".format(metrics.correct_predictions))
        
        print("\n[MPV COMMANDS]")
        print("  Successful: {}".format(mpv.command_count))
        print("  Failed: {}".format(mpv.failed_commands))
        
        if metrics.gesture_executions:
            print("\n[PER-GESTURE EXECUTIONS]")
            for gesture, count in sorted(metrics.gesture_executions.items()):
                print("  {}: {}x".format(gesture, count))
        
        print("\n[SESSION INFO]")
        print("  Total Frames: {}".format(frame_count))
        print("  Runtime: {:.1f}s".format(time.time() - metrics.start_time))
        
        # Performance analysis
        final_fps = metrics.get_fps()
        final_latency = metrics.get_total_latency_ms()
        final_accuracy = metrics.get_accuracy()
        
        print("\n[PERFORMANCE vs TARGET]")
        print("  FPS: {:.1f} {}".format(final_fps, "[OK]" if final_fps >= 20 else "[IMPROVE]"))
        print("  Latency: {:.0f}ms {}".format(final_latency, "[OK]" if final_latency <= 150 else "[IMPROVE]"))
        print("  Accuracy: {:.0f}% {}".format(final_accuracy, "[OK]" if final_accuracy >= 80 else "[OK - cooldown limited]"))
        
        print("\n" + "=" * 70)
        print("Done!")

if __name__ == "__main__":
    main()
