# Raspberry Pi Taka Note Detector
import cv2
import time
import os
import subprocess
from picamera2 import Picamera2

# Configuration 
CASCADE_FILES = {
    "10": "/home/pi/cascades/10_taka.xml",
    "50": "/home/pi/cascades/50_taka.xml",
    "100": "/home/pi/cascades/100_taka.xml",
    "500": "/home/pi/cascades/500_taka.xml"
}

SCALE_FACTOR = 1.2
MIN_NEIGHBORS = 4
MIN_SIZE = (60, 30)
DETECTION_COOLDOWN = 1.5  
OUTDIR = "/home/pi/detections"
os.makedirs(OUTDIR, exist_ok=True)

# Load cascades
cascades = {}
for label, path in CASCADE_FILES.items():
    if not os.path.exists(path):
        print(f"Cascade file not found: {path}")
        continue
    c = cv2.CascadeClassifier(path)
    if c.empty():
        print(f"Failed to load cascade: {path}")
        continue
    cascades[label] = c

if not cascades:
    raise RuntimeError("No valid cascades loaded!")

# Initialize camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "BGR888"})
picam2.configure(config)
picam2.start()
print("Using Picamera2 for live detection (normal colors).")
print("Press 'q' to quit.")

last_detection_time = 0

def speak(text: str):
    """Speak text via espeak (lightweight TTS)."""
    try:
        subprocess.Popen(["espeak", text])
    except FileNotFoundError:
        pass

# Main 
while True:
    # Capture directly in BGR — no need for color conversion
    frame = picam2.capture_array()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    detected_labels = []
    for label, cascade in cascades.items():
        found = cascade.detectMultiScale(
            gray,
            scaleFactor=SCALE_FACTOR,
            minNeighbors=MIN_NEIGHBORS,
            minSize=MIN_SIZE
        )

        for (x, y, w, h) in found:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} Taka", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            detected_labels.append(label)

    # If any note detected, announce & save image
    now = time.time()
    if detected_labels and (now - last_detection_time) > DETECTION_COOLDOWN:
        last_detection_time = now
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        fname = os.path.join(OUTDIR, f"det_{timestamp}.jpg")
        cv2.imwrite(fname, frame)
        notes = ", ".join(sorted(set(detected_labels)))
        print(f"[{timestamp}] Detected: {notes} taka → saved {fname}")
        speak(f"Detected {notes} taka")

    # Display window
    cv2.imshow("Multi Taka Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
print("Detection stopped.")
