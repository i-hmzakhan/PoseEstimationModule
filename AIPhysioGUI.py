import tkinter as tk
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading
import PoseEstimationModule as pm # Your updated module
import time


# Video Paths for Testing:
# 1. Webcam: 
video_path = 0
# 2. External Camera: 
# video_path = 1
# 3. Video File: 
#video_path = r'path_to_your_video.mp4'  

class PhysioAppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kinetic-OS | AI Physio Trainer")
        self.geometry("1100x600")
        
        # --- Initialize AI Engine ---
        self.detector = pm.PoseDetector()
        self.cap = cv2.VideoCapture(video_path)  # Change to 0 for webcam, 1 for external camera, or provide video path
        # Set properties for 720p (Width=3, Height=4)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 384)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)
        self.running = True

        # --- Layout Configuration ---
        self.grid_columnconfigure(1, weight=15)
        self.grid_rowconfigure(0, weight=5)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="KINETIC-OS", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_start = ctk.CTkButton(self.sidebar, text="Reset Reps", command=self.reset_counter)
        self.btn_start.grid(row=1, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))

        # --- Main Video Area ---
        self.video_label = tk.Label(self, bg="black")
        self.video_label.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # --- Stats Overlay (Bottom) ---
        self.stats_frame = ctk.CTkFrame(self, height=100)
        self.stats_frame.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="ew")
        
        self.rep_label = ctk.CTkLabel(self.stats_frame, text="REPS: 0", font=ctk.CTkFont(size=40, weight="bold"))
        self.rep_label.pack(side="left", padx=50)

        self.fps_label = ctk.CTkLabel(self.stats_frame, text="FPS: 0", font=ctk.CTkFont(size=15))
        self.fps_label.pack(side="right", padx=20)

        # Start the video thread
        self.thread = threading.Thread(target=self.video_loop, daemon=True)
        self.thread.start()

    def video_loop(self):
        pTime = 0
        while self.running:
            success, frame = self.cap.read()
            if success:
                # 1. Run AI Logic
                timestamp_ms = int(self.cap.get(cv2.CAP_PROP_POS_MSEC))
                frame = self.detector.find_pose(frame, timestamp_ms)
                lmList = self.detector.get_positions(frame)

                if len(lmList) != 0:
                    angle = self.detector.find_angle(frame, 11, 13, 15)
                    per, bar = self.detector.get_progress_stats(angle)
                    reps = self.detector.rep_counter(angle)
                    
                    # Update GUI Labels
                    self.rep_label.configure(text=f"REPS: {int(reps)}")
                
                # 2. Performance Tracking
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                self.fps_label.configure(text=f"FPS: {int(fps)}")

                # 3. Convert frame for Tkinter
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (1080*2, 1080))
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

    def reset_counter(self):
        self.detector.count = 0
        self.rep_label.configure(text="REPS: 0")

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def on_closing(self):
        self.running = False
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = PhysioAppGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()