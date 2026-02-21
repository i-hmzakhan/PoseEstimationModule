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

💡 What can you build with this module?
Because of its modular design and built-in geometric logic, this repository can serve as the core engine for several Computer Vision applications:

1. AI Fitness Trainer
Rep Counter: Automatically count squats, push-ups, or bicep curls using the find_angle method.

Form Correction: Compare live joint angles against "perfect form" thresholds and provide real-time audio/visual alerts if the user is leaning too far or not reaching full depth.

2. Physical Therapy Assistant
Range of Motion (ROM) Tracking: Measure the maximum extension and flexion of a joint over time to track recovery progress after surgery or injury.

Posture Monitor: Use the shoulder and hip landmarks to detect "slouching" while working at a desk and trigger a Windows notification to sit up straight.

3. Gesture-Based Control (HCI)
Touchless Interface: Map the coordinates of the wrists (Landmarks 15 & 16) to the system mouse cursor to navigate OS menus without a physical mouse.

Virtual Gaming: Trigger game actions (like jumping or punching) when specific pose conditions are met (e.g., if y-coordinate of hips increases by 20%).

4. Sports Analytics
Bowling/Swing Analysis: Analyze the velocity and angle of an arm during a cricket bowl or a golf swing by calculating the change in joint coordinates across frames.

Yoga Alignment: Verify if a user is holding a pose (like the Warrior Pose) by checking the alignment of the ankles, knees, and shoulders.
[ ] Squat Depth Analysis: Adding hip-to-ankle angle logic.
[ ] Export Functionality: Saving workout data to .csv or .json.


[P.S. If you're interested in the above-mentioned projects, you would only need to add functions/methods for them in the module file and call them in your main function. (For example, the biceps curl counter has already been added to the module).]


