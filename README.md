PoseEstimationModule
A high-performance, modular Python library for real-time human pose estimation using the MediaPipe Tasks API. This module is designed for developers and AI students looking to integrate robust pose tracking, joint angle calculation, and exercise repetition counting into their Computer Vision applications.

🚀 Key Features
Modular Class Design: Encapsulated PoseDetector class for "plug-and-play" use in any Python project.

Modern Tasks API: Migrated from legacy MediaPipe solutions to the higher-performance Tasks API (using .task files).

Advanced Rep Counter: Includes a built-in state machine for dual-arm repetition tracking (e.g., bicep curls).

Geometric Inference: Built-in find_angle method using trigonometric mapping to calculate exact joint degrees.

Performance Optimized: Specifically tuned for mid-range/legacy CPUs (tested on Intel Core i7-6600U) utilizing XNNPACK delegates.

Visual Feedback: Integrated logic for dynamic progress bars and percentage mapping using NumPy interpolation.

🛠️ Technical Stack
Language: Python 3.10+

AI Framework: MediaPipe (Vision Tasks)

Image Processing: OpenCV

Math: NumPy (Linear Mapping/Interpolation)

GUI: CustomTkinter (for Dashboard applications)

📂 Project Structure
Plaintext
├── PoseModule.py               # Core detection engine & math methods
├── PoseEstimationModuleTest.py # Main application/test script
├── PhysioAppGUI.py             # CustomTkinter Dashboard with Threading
├── pose_landmarker_lite.task   # MediaPipe optimized model file
└── requirements.txt            # Project dependencies

Note: The 'pose_landmarker_lit.task' file is a light-version API of Google's MediaPipe module. To run this module, you would need to use any of the three '.task' files in your system, as explained in the diagram above. Furthermore, two versions of this API are included in this repository.

⚙️ Installation & Setup
Clone the Repository

Bash
git clone (https://github.com/i-hmzakhan/PoseEstimationModule)
cd PoseEstimationModule
Setup Virtual Environment

Bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
Download the Task Model
Download the pose_landmarker_lite.task file from the Official MediaPipe Site and place it in the root directory.

💻 Quick Start
Basic Detection
Python
import cv2
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.PoseDetector()

while True:
    success, frame = cap.read()
    frame = detector.find_pose(frame, timestamp_ms=int(time.time()*1000))
    lmList = detector.get_positions(frame)
    
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
Bicep Curl Angle Calculation
Python
# Calculate angle for Left Arm (Shoulder: 11, Elbow: 13, Wrist: 15)
angle = detector.find_angle(frame, 11, 13, 15)
reps = detector.rep_counter(angle, side="L")
📊 Roadmap
[ ] Multi-Person Support: Enabling tracking for multiple bodies in a single frame.

[ ] Squat Depth Analysis: Adding hip-to-ankle angle logic.

[ ] Export Functionality: Saving workout data to .csv or .json.
