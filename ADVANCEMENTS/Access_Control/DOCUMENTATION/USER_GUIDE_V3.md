# Face-Based Access Control - User Guide
## Quick & Simple

**Version:** 2.0 with Face Recognition  
**Date:** February 19, 2026  

---

## Quick Start (5 Minutes)

### Terminal 1: Start MPV
```bash
mpv --input-ipc-server=/tmp/mpvsocket --loop=inf "video.mp4"
```

### Terminal 2: Start System
```bash
cd ~/improve
sudo nvpmodel -m 0
sudo jetson_clocks
python3 version_2.py
```

**Camera window opens → Make gestures!**

---

## How It Works

### Step 1: Enroll Your Face (One Time)
```bash
python3 scripts/enroll_user.py
# Enter your name: john
# Look at camera, press SPACE 5 times (different angles)
# Done! You're registered
```

### Step 2: Use The System
- Your face appears → Green box = Authorized ✅
- Your gestures work → Video responds
- Unknown face → Red box = Blocked ❌
- Their gestures don't work

### Step 3: Make Gestures (8 Options)

| Gesture | Hand | How | Action |
|---------|------|-----|--------|
| PLAY | Either | 2 fingers up ✌️ | Play |
| PAUSE | Either | Open palm ✋ | Pause |
| VOLUME_UP | Either | Index up ☝️ | Vol+5% |
| VOLUME_DOWN | Either | Index down 👇 | Vol-5% |
| SKIP_RIGHT | LEFT | Thumb + 2→ | +5s |
| SKIP_LEFT | RIGHT | Thumb + 2← | -5s |
| NEXT | LEFT | Thumb + 1→ | Next |
| PREVIOUS | RIGHT | Thumb + 1← | Prev |

---

## Face Recognition Features

### Authorized User (You)
```
 Face detected
 System recognizes: "Welcome john!"
 Gestures WORK
 Commands execute
```

### Unauthorized User (Someone Else)
```
 Face detected but NOT recognized
 System shows: "Unknown user - Access denied"
 Gestures DON'T WORK
 No commands execute
```

### Session Management
- Authorized for 30 seconds of no-face
- Leave → Session expires
- Return → Re-authenticate instantly
- Clean, secure access

---

## Tips for Success

### Face Recognition
-  Good lighting in front of face
-  Face fully visible in camera
-  Different angles during enrollment (5 photos)
-  Don't wear sunglasses
-  Don't cover face

### Gestures
-  Extend fingers fully
-  Hold 0.5+ seconds
-  Face palm toward camera
-  Good lighting for hand
-  Quick jerky movements
-  Hand out of frame

---

## Common Issues

### Issue: Not Recognized
**Solution:**
- Better lighting
- Face fully visible
- Re-enroll with new photos

### Issue: Gestures Not Working
**Check:**
- Is green box showing? (Authorized)
- Is red box showing? (Not authorized)
- If red → Have authorized person try

### Issue: Can't Enroll
```bash
# Check camera works
python3 -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

# Try enrollment again
python3 scripts/enroll_user.py
```

---

## Enroll Multiple Users

```bash
# Enroll alice
python3 scripts/enroll_user.py
# Name: alice

# Enroll bob
python3 scripts/enroll_user.py
# Name: bob

# Check who's enrolled
python3 -c "from modules.face_recognition import FaceRecognizer; print(FaceRecognizer().list_users())"
# Output: ['john', 'alice', 'bob']
```

---

## Security Features

✅ **Only authorized users can control**
✅ **Face database encrypted**
✅ **Session timeout (30s) prevents hijacking**
✅ **Audit trail (who used what, when)**
✅ **Easy to block users (delete from database)**

---

## Quit System

**In camera window:** Press `Q`

---

## Summary

✅ Enroll once (5 photos)
✅ System recognizes your face
✅ Only you can control media
✅ Others are blocked
✅ 8 easy hand gestures
✅ Real-time response

**That's it! Enjoy touchless, secure control!** 🎉

