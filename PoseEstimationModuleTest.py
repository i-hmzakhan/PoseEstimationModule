import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow/MediaPipe logging
import cv2
import time
import PoseEstimationModule as pm # Ensure this matches your filename

# 1. Setup Camera
video_path = r'E:\Sem-03\Computer Vision\PoseEstimationProject\5.mp4'  # Change to 0 for webcam, 1 for external camera, or provide video path
cap = cv2.VideoCapture(video_path)  # Change to 0 for webcam, 1 for external camera, or provide video path
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
if not cap.isOpened():
    print(f"ERROR: Could not open video file at {video_path}")
    # Print current working directory to help you debug the path
    print(f"Current Working Directory: {os.getcwd()}") 
else:
    print("Video file opened successfully!")
detector = pm.PoseDetector()
pTime = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    # 2. AI Detection
    timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
    frame = detector.find_pose(frame, timestamp_ms)
    lmList = detector.get_positions(frame)

    # 3. Logic Layer (Only runs if a person is detected)
    if len(lmList) != 0:
        # Calculate Angle (Left Arm: Shoulder 11, Elbow 13, Wrist 15)
        angle = detector.find_angle(frame, 11, 13, 15)
        
        # Get Progress Bar Data
        per, bar = detector.get_progress_stats(angle)
        
        # Count Repetitions
        reps = detector.rep_counter(angle)

        # --- DRAW PROGRESS BAR ---
        # 1. The Background Outline (Gray)
        cv2.rectangle(frame, (580, 100), (620, 400), (128, 128, 128), 3)
        # 2. The Filling Bar (Green)
        cv2.rectangle(frame, (580, int(bar/1.5)), (620, 400), (0, 255, 0), cv2.FILLED)
        # 3. Percentage Text
        cv2.putText(frame, f'{int(per)}%', (560, 80), 
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        # --- DRAW REP COUNTER BOX ---
        cv2.rectangle(frame, (0, 380), (150, 500), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, str(int(reps)), (45, 480), 
                    cv2.FONT_HERSHEY_PLAIN, 8, (255, 0, 0), 10)

    # 4. Final UI Scaling & Display
    # Note: We resize at the end so our UI coordinates stay consistent
    frame = cv2.resize(frame, (720, 500))
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(frame, f'FPS: {int(fps)}', (10, 50), 
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)
    
    cv2.imshow("Kinetic-OS Physio", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

detector.close()
cap.release()
cv2.destroyAllWindows()