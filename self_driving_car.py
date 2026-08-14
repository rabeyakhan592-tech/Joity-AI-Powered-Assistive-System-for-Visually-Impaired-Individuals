import time
import cv2
import numpy as np
from gpiozero import Motor, PWMOutputDevice
from picamera2 import Picamera2
from ultralytics import YOLO

# 1. Hardware & Model Initialization

# Motor driver setup
right_motor = Motor(forward=5, backward=23)
left_motor = Motor(forward=24, backward=27)

right_speed = PWMOutputDevice(13)
left_speed = PWMOutputDevice(12)

# Camera configuration
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (720, 560)}))
picam2.start()
picam2.set_controls({"FrameRate": 30})

# YOLOv8 Object Detection Setup (Class 11 = Stop Sign)
model = YOLO("yolov8n.pt") 
STOP_SIGN_CLASS = 11

# 2. Computer Vision Parameters & Helpers

# Perspective warping anchors
SRC_POINTS = np.float32([[5, 480], [760, 480], [55, 250], [685, 250]])
DST_POINTS = np.float32([[100, 240], [280, 240], [100, 0], [280, 0]])
TRANSFORM_MATRIX = cv2.getPerspectiveTransform(SRC_POINTS, DST_POINTS)

def perspective_transform(frame):
    """Warps the camera frame to a bird's-eye perspective view."""
    return cv2.warpPerspective(frame, TRANSFORM_MATRIX, (400, 240))

def process_frame(frame):
    """Filters images using color isolation and Canny edge extraction."""
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    frame_thresh = cv2.inRange(frame_gray, 235, 255)
    frame_edge = cv2.Canny(frame_thresh, 400, 600, apertureSize=3)
    
    frame_final = cv2.bitwise_or(frame_thresh, frame_edge)
    return cv2.cvtColor(frame_final, cv2.COLOR_GRAY2RGB)

def compute_histogram(frame_final):
    """Efficiently sums the region of interest columns using NumPy vectors."""
    roi = frame_final[140:240, :, 0]  # Take only one color channel
    return np.sum(roi, axis=0) / 255

def compute_lane_end_metric(frame_final):
    """Checks the aggregate brightness across the frame to spot a dead end."""
    return np.sum(frame_final[:, :, 0]) / 255

def detect_lanes(histogram_lane):
    """Identifies the peak column locations for both active lanes."""
    left_lane_pos = np.argmax(histogram_lane[:150])
    right_lane_pos = np.argmax(histogram_lane[250:]) + 250
    return left_lane_pos, right_lane_pos

def estimate_distance(bbox_width_px, focal_length_px=1280, known_width_cm=6):
    """Translates bounding box pixel width into a real-world centimeter distance."""
    if bbox_width_px <= 0:
        return None
    return (known_width_cm * focal_length_px) / bbox_width_px

# 3. Dynamic Motor Controls

def move_forward(speed=0.25):
    left_motor.forward()
    right_motor.forward()
    left_speed.value = speed
    right_speed.value = speed

def stop_motors():
    left_motor.stop()
    right_motor.stop()
    left_speed.value = 0
    right_speed.value = 0

def steer_left(severity):
    """Handles multi-tier turning left via severity inputs (1, 2, or 3)."""
    speeds = {1: (0.1, 0.25), 2: (0.15, 0.25), 3: (0.25, 0.25)}
    l_spd, r_spd = speeds.get(severity, (0.25, 0.25))
    
    left_motor.backward()
    right_motor.forward()
    left_speed.value = l_spd
    right_speed.value = r_spd

def steer_right(severity):
    """Handles multi-tier turning right via severity inputs (1, 2, or 3)."""
    speeds = {1: (0.25, 0.1), 2: (0.25, 0.15), 3: (0.25, 0.25)}
    l_spd, r_spd = speeds.get(severity, (0.25, 0.25))
    
    left_motor.forward()
    right_motor.backward()
    left_speed.value = l_spd
    right_speed.value = r_spd

def execute_u_turn():
    left_motor.forward()
    right_motor.backward()
    left_speed.value = 0.2
    right_speed.value = 0.1
    time.sleep(2.0)

# 4. Main Control Routine

try:
    while True:
        frame = picam2.capture_array()
        if frame is None:
            continue

        # Performance fix: Drop alpha channel to build classic 3-channel standard BGR
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        # Draw source warp overlay boundaries onto video feed
        for idx in range(4):
            pt1 = tuple(map(int, SRC_POINTS[idx]))
            pt2 = tuple(map(int, SRC_POINTS[(idx + 1) % 4]))
            cv2.line(frame, pt1, pt2, (255, 0, 0), 2)

        # Vision pipeline executions
        frame_perspective = perspective_transform(frame)
        frame_final = process_frame(frame_perspective)
        
        histogram_lane = compute_histogram(frame_final)
        left_lane_pos, right_lane_pos = detect_lanes(histogram_lane)
        lane_end_metric = compute_lane_end_metric(frame_final)

        # Evaluate positioning layout variables
        if lane_end_metric > 33000:
            execute_u_turn()
            error_value = 0
        elif left_lane_pos > 0 and right_lane_pos > 0:
            lane_center = (right_lane_pos - left_lane_pos) // 2 + left_lane_pos
            error_value = (lane_center - 188) // 4
        else:
            error_value = 0
            
        print(f"Tracking error index: {error_value}")

        # Evaluate target frame using ML inferences
        results = model.predict(frame_bgr, classes=[STOP_SIGN_CLASS], verbose=False)
        annotated_frame = results[0].plot()
        stop_detected = False

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id].lower()
            
            if "stop" in label:
                x1, y1, x2, y2 = map(float, box.xyxy[0])
                distance_cm = estimate_distance(x2 - x1, known_width_cm=6)
                
                if distance_cm and distance_cm <= 50:
                    stop_detected = True
                    stop_motors()
                    
                    # Display safety prompt parameters
                    cv2.putText(annotated_frame, "STOPPED for 5s", (int(x1), int(y1) + 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.imshow("Detection Window", annotated_frame)
                    cv2.waitKey(1)
                    
                    time.sleep(5)
                    move_forward()
                    break

        # Process movement updates if path clears safe metrics
        if not stop_detected:
            if error_value == 0:
                move_forward()
            elif 0 < error_value < 3:
                steer_right(severity=1)
            elif 3 <= error_value < 5:
                steer_right(severity=2)
            elif error_value >= 5:
                steer_right(severity=3)
            elif -3 < error_value < 0:
                steer_left(severity=1)
            elif -5 < error_value <= -3:
                steer_left(severity=2)
            elif error_value <= -5:
                steer_left(severity=3)

        # Render on-screen HUD graphics layouts
        cv2.line(frame_final, (left_lane_pos, 0), (left_lane_pos, 240), (0, 255, 0), 2)
        cv2.line(frame_final, (right_lane_pos, 0), (right_lane_pos, 240), (0, 255, 0), 2)
        cv2.line(frame_final, (188, 0), (188, 240), (255, 0, 0), 2)

        cv2.putText(frame_perspective, "Perspective Transform", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
        cv2.putText(frame_final, f"Tracking Error: {error_value}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        cv2.imshow("Perspective", frame_perspective)
        cv2.imshow("Final", frame_final)
        cv2.imshow("Detection Window", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    stop_motors()
    picam2.stop()
    cv2.destroyAllWindows()
