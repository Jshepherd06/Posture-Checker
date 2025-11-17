import cv2
import mediapipe as mp
import numpy as np
import time
import pygame
from PyQt6.QtCore import QThread, pyqtSignal

# Import your settings class or pass settings dictionary
# from app_settings import AppSettings 

class PoseDetectorThread(QThread):
    # --- Define Signals ---
    # Signal to send the video frame (np.ndarray)
    frame_ready = pyqtSignal(np.ndarray)
    # Signal to send status updates (text, color)
    posture_status = pyqtSignal(str, str)
    # Signal to send warnings (e.g., "Too dark")
    system_warning = pyqtSignal(str)
    # Signal for calibration status
    calibration_status = pyqtSignal(str)

    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.running = True
        self.calibrating = False

        # --- PoseDetector logic (moved from __init__) ---
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = None
        
        self.lastTime = 0
        pygame.mixer.init()
        try:
            self.warning_sound = pygame.mixer.Sound("assets/warning.wav")
        except FileNotFoundError:
            self.warning_sound = None
            print("Warning: could not load sound file.")

        self.baseline = None
        self.brightness_threshold = 40

    def run(self):
        """This is the main loop of the thread."""
        self.cap = cv2.VideoCapture(0)
        
        while self.running:
            if not self.cap.isOpened():
                self.system_warning.emit("No camera feed — trying to reconnect...")
                self.reconnect_camera()
                time.sleep(1)
                continue

            ret, frame = self.cap.read()
            if not ret:
                continue

            # --- Handle Calibration ---
            if self.calibrating:
                self.run_calibration() # A new function to handle the calibration loop
                self.calibrating = False # Stop calibrating after it's done
                continue # Skip rest of loop for this one frame

            # --- Brightness Check ---
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if np.mean(gray) < self.brightness_threshold:
                self.system_warning.emit("Too dark — please improve lighting!")
            else:
                self.system_warning.emit("") # Clear warning

            # --- Pose Processing ---
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb)
            self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            
            if results.pose_landmarks:
                posture_ratio = self.read_posture(results.pose_landmarks.landmark)
                self.add_text_and_check(frame, posture_ratio)
            
            # --- Emit the processed frame ---
            self.frame_ready.emit(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
        self.cap.release()
        print("Pose detector thread stopped.")

    def start_calibration(self):
        """Called from the GUI to trigger calibration."""
        self.calibrating = True

    def run_calibration(self):
        """Collect posture ratios for a few seconds to compute baseline."""
        self.calibration_status.emit("Sit upright — calibrating posture...")
        ratios = []
        start = time.time()
        duration = self.settings.get("calibration_duration")

        while time.time() - start < duration:
            ret, frame = self.cap.read()
            if not ret: continue
            
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb)
            if results.pose_landmarks:
                ratio = self.read_posture(results.pose_landmarks.landmark)
                ratios.append(ratio)
            
            # Emit frame during calibration
            self.frame_ready.emit(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            time.sleep(0.03) # ~30fps

        if ratios:
            self.baseline = np.mean(ratios)
            b = self.baseline * self.settings.get("posture_strictness")
            self.calibration_status.emit(f"Calibration complete. Baseline: {b:.3f}")
        else:
            self.calibration_status.emit("Calibration failed — no pose detected.")

    def add_text_and_check(self, frame, posture_ratio):
        """Replaces add_text, also emits signals."""
        if self.baseline:
            threshold = self.baseline * self.settings.get("posture_strictness")
        else:
            threshold = self.settings.get("posture_threshold")
        
        cv2.putText(frame, f"Posture Ratio: {posture_ratio:.4f}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        
        if posture_ratio > threshold:
            cv2.putText(frame, "Good posture", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            self.posture_status.emit("Good Posture", "green")
        else:
            cv2.putText(frame, "Bad posture", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            self.posture_status.emit("Bad Posture", "red")
            self.handle_audio_alert(posture_ratio, threshold) # Pass threshold

    def handle_audio_alert(self, posture_ratio, threshold):
        """Play a sound when posture is bad."""
        if (posture_ratio <= threshold) and self.settings.get("sound_enabled"):
            if time.time() - self.lastTime > self.settings.get("warning_wait"):
                self.lastTime = time.time()
                if self.warning_sound:
                    self.warning_sound.play()

    def read_posture(self, landmarks):
        nose = landmarks[0]
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        left_shoulder_x = left_shoulder.x
        right_shoulder_x = right_shoulder.x
        shoulder_Length = abs(left_shoulder_x - right_shoulder_x)
        if shoulder_Length < 0.1: # Avoid division by zero if shoulders not visible
             return 0
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        nose_y = nose.y
        posture_ratio = (shoulder_y - nose_y) / shoulder_Length
        return posture_ratio

    def reconnect_camera(self):
        if self.cap:
            self.cap.release()
        time.sleep(0.5)
        self.cap = cv2.VideoCapture(0)

    def stop(self):
        """Tells the loop to exit."""
        self.running = False