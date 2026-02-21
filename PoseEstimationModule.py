import cv2
import mediapipe as mp
import time
import math
import numpy as np 
from mediapipe.tasks import python
from mediapipe.tasks.python import vision



class PoseDetector:
    def __init__(self, model_path='.venv/pose_landmarker_lite.task'):
        self.model_path = model_path
        
        # --- MediaPipe Tasks Initialization ---
        BaseOptions = mp.tasks.BaseOptions
        PoseLandmarker = mp.tasks.vision.PoseLandmarker
        PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=self.model_path),
            running_mode=VisionRunningMode.VIDEO
        )

        self.detector = PoseLandmarker.create_from_options(options)
        
        # --- Persistent Fitness Variables ---
        self.count = 0
        self.dir = 0  # 0 for moving Up (contraction), 1 for moving Down (extension)
        
        self.POSE_CONNECTIONS = [
            (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5), (5, 6), (6, 8),
            (9, 10), (11, 12), (11, 13), (13, 15), (12, 14), (14, 16),
            (15, 17), (15, 19), (15, 21), (17, 19), (16, 18), (16, 20), (16, 22), (18, 20),
            (11, 23), (12, 24), (23, 24), (23, 25), (24, 26), (25, 27), (26, 28),
            (27, 29), (28, 30), (27, 31), (28, 32), (29, 31), (30, 32)
        ]

    def find_pose(self, frame, timestamp_ms, draw=True):
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        self.results = self.detector.detect_for_video(mp_image, timestamp_ms)

        if self.results.pose_landmarks and draw:
            for landmark_list in self.results.pose_landmarks:
                for connection in self.POSE_CONNECTIONS:
                    start_lm = landmark_list[connection[0]]
                    end_lm = landmark_list[connection[1]]
                    if start_lm.visibility > 0.5 and end_lm.visibility > 0.5:
                        start_point = (int(start_lm.x * w), int(start_lm.y * h))
                        end_point = (int(end_lm.x * w), int(end_lm.y * h))
                        cv2.line(frame, start_point, end_point, (0, 255, 0), 2)

                for lm in landmark_list:
                    if lm.visibility > 0.5:
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return frame

    def get_positions(self, frame):
        self.lmList = []
        if self.results.pose_landmarks:
            h, w, _ = frame.shape
            for id, lm in enumerate(self.results.pose_landmarks[0]):
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy, lm.visibility])
        return self.lmList

    def find_angle(self, frame, p1, p2, p3, draw=True):
        """Calculates angle between three points (e.g., 11, 13, 15 for left arm)."""
        x1, y1 = self.lmList[p1][1:3]
        x2, y2 = self.lmList[p2][1:3]
        x3, y3 = self.lmList[p3][1:3]

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - 
                             math.atan2(y1 - y2, x1 - x2))
        if angle < 0: angle += 360
        if angle > 180: angle = 360 - angle

        if draw:
            cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(frame, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(frame, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, str(int(angle)), (x2 - 50, y2 + 50), 
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle

    def rep_counter(self, angle, up_thresh=160, down_thresh=30):
        """Logic to increment count when a full range of motion is detected."""
        if angle >= up_thresh:
            if self.dir == 0:
                self.count += 0.5
                self.dir = 1
        if angle <= down_thresh:
            if self.dir == 1:
                self.count += 0.5
                self.dir = 0
        return int(self.count)
    
    

    # Inside the PoseDetector class:
    def get_progress_stats(self, angle, up_thresh=160, down_thresh=30):
        """
        Returns the percentage of the rep and the pixel height for a bar.
        """
        # 1. Map angle to 0-100 percentage
        per = np.interp(angle, (down_thresh, up_thresh), (100, 0))
        
        # 2. Map angle to bar height (650 is bottom, 100 is top of bar)
        bar = np.interp(angle, (down_thresh, up_thresh), (100, 650))
        
        return per, bar

    def close(self):
        self.detector.close()