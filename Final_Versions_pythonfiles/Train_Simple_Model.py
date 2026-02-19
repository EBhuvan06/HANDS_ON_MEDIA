#!/usr/bin/env python3
"""
Train gesture recognition model optimized for Jetson Nano
"""

import numpy as np
import cv2
import mediapipe as mp
import os
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import json

print(f"TensorFlow version: {tf.__version__}")
print(f"GPU Available: {tf.config.list_physical_devices('GPU')}")

# Configuration
GESTURES = ['VOLUME_UP', 'VOLUME_DOWN', 'PLAY', 'PAUSE', 'NEXT', 'PREVIOUS', 
            'STOP', 'SKIP_LEFT', 'SKIP_RIGHT']
RAW_IMAGES_DIR = 'dataset/raw_images'
MODEL_DIR = 'models'
MODEL_NAME = 'gesture_model_v2.h5'
TFLITE_NAME = 'gesture_model_v2.tflite'

os.makedirs(MODEL_DIR, exist_ok=True)

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)

def extract_hand_landmarks(image_path):
    """Extract hand landmarks from image"""
    image = cv2.imread(image_path)
    if image is None:
        return None
    
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)
    
    if not results.multi_hand_landmarks:
        return None
    
    hand_landmarks = results.multi_hand_landmarks[0]
    landmarks = []
    for lm in hand_landmarks.landmark:
        landmarks.extend([lm.x, lm.y])
    
    return np.array(landmarks)

def load_dataset():
    """Load and process dataset"""
    X = []
    y = []
    
    print("\n📦 Loading dataset...")
    print("-" * 60)
    
    for gesture_idx, gesture in enumerate(GESTURES):
        gesture_dir = os.path.join(RAW_IMAGES_DIR, gesture.lower())
        
        if not os.path.exists(gesture_dir):
            print(f"⚠️  {gesture}: Directory not found")
            continue
        
        image_files = [f for f in os.listdir(gesture_dir) if f.endswith('.jpg')]
        successful = 0
        failed = 0
        
        for img_file in image_files:
            img_path = os.path.join(gesture_dir, img_file)
            landmarks = extract_hand_landmarks(img_path)
            
            if landmarks is not None:
                X.append(landmarks)
                y.append(gesture_idx)
                successful += 1
            else:
                failed += 1
        
        print(f"{'✅' if successful > 0 else '❌'} {gesture:15} : {successful:4} samples ({failed} failed)")
    
    print("-" * 60)
    
    if len(X) == 0:
        raise ValueError("No valid samples found!")
    
    X = np.array(X)
    y = np.array(y)
    
    # Shuffle data
    X, y = shuffle(X, y, random_state=42)
    
    print(f"Total samples: {len(X)}")
    print(f"Feature shape: {X.shape}")
    print(f"Classes: {len(GESTURES)}\n")
    
    return X, y

def create_model(input_shape, num_classes):
    """Create optimized model for Jetson Nano"""
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        
        # Batch normalization for stability
        layers.BatchNormalization(),
        
        # First dense block
        layers.Dense(256, kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.4),
        
        # Second dense block
        layers.Dense(128, kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.3),
        
        # Third dense block
        layers.Dense(64, kernel_regularizer=regularizers.l2(0.001)),
        layers.BatchNormalization(),
        layers.Activation('relu'),
        layers.Dropout(0.2),
        
        # Output layer
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def train_model(X_train, y_train, X_val, y_val, num_classes):
    """Train the model"""
    
    print("🏗️  Building model...")
    model = create_model((X_train.shape[1],), num_classes)
    
    # Compile with proper optimizer
    optimizer = keras.optimizers.Adam(learning_rate=0.001)
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    model.summary()
    
    # Callbacks
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        ),
        ModelCheckpoint(
            os.path.join(MODEL_DIR, 'best_model.h5'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    print("\n🚀 Training model...")
    print("=" * 60)
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=100,
        batch_size=32,
        callbacks=callbacks,
        verbose=1
    )
    
    return model, history

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    print("\n📊 Evaluating model...")
    print("=" * 60)
    
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {test_acc*100:.2f}%")
    print(f"Test Loss: {test_loss:.4f}")
    
    # Per-class accuracy
    predictions = model.predict(X_test, verbose=0)
    pred_classes = np.argmax(predictions, axis=1)
    
    print("\nPer-Class Accuracy:")
    print("-" * 40)
    for i, gesture in enumerate(GESTURES):
        mask = y_test == i
        if np.sum(mask) > 0:
            class_acc = np.mean(pred_classes[mask] == y_test[mask])
            print(f"{gesture:15} : {class_acc*100:.2f}%")
    
    return test_acc

def convert_to_tflite(model):
    """Convert model to TFLite for Jetson Nano"""
    print("\n🔄 Converting to TFLite...")
    
    # Convert with optimization
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    # For Jetson Nano, we can use float16 for better performance
    converter.target_spec.supported_types = [tf.float16]
    
    tflite_model = converter.convert()
    
    # Save TFLite model
    tflite_path = os.path.join(MODEL_DIR, TFLITE_NAME)
    with open(tflite_path, 'wb') as f:
        f.write(tflite_model)
    
    print(f"✅ TFLite model saved: {tflite_path}")
    print(f"   Size: {len(tflite_model) / 1024:.2f} KB")
    
    return tflite_path

def save_gesture_labels():
    """Save gesture labels"""
    labels_path = os.path.join(MODEL_DIR, 'gesture_labels.txt')
    with open(labels_path, 'w') as f:
        for gesture in GESTURES:
            f.write(f"{gesture}\n")
    print(f"✅ Labels saved: {labels_path}")

def main():
    print("\n" + "=" * 60)
    print("🎯 GESTURE RECOGNITION MODEL TRAINING")
    print("=" * 60)
    
    # Load dataset
    X, y = load_dataset()
    
    # Split dataset: 70% train, 15% validation, 15% test
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Test samples: {len(X_test)}\n")
    
    # Train model
    model, history = train_model(X_train, y_train, X_val, y_val, len(GESTURES))
    
    # Evaluate
    test_acc = evaluate_model(model, X_test, y_test)
    
    # Save .h5 model
    h5_path = os.path.join(MODEL_DIR, MODEL_NAME)
    model.save(h5_path)
    print(f"\n✅ H5 model saved: {h5_path}")
    
    # Convert to TFLite
    tflite_path = convert_to_tflite(model)
    
    # Save labels
    save_gesture_labels()
    
    # Save training info
    info = {
        'gestures': GESTURES,
        'test_accuracy': float(test_acc),
        'total_samples': int(len(X)),
        'input_shape': [int(x) for x in X.shape[1:]],
        'num_classes': len(GESTURES)
    }
    
    info_path = os.path.join(MODEL_DIR, 'model_info.json')
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ TRAINING COMPLETE!")
    print("=" * 60)
    print(f"📁 Models directory: {MODEL_DIR}/")
    print(f"   - {MODEL_NAME} (H5 format)")
    print(f"   - {TFLITE_NAME} (TFLite format for Jetson)")
    print(f"   - gesture_labels.txt")
    print(f"   - model_info.json")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
    hands.close()
