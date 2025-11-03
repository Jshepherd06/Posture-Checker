import cv2
import mediapipe as mp
import streamlit as st
import numpy as np
import time
from pathlib import Path
import pygame

class PoseDetector:
    def __init__(self,posture_threshold=0.75):
        # Mediapipe pose setup
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

        # Video capture setup
        self.cap = cv2.VideoCapture(0)
        self.posture_threshold = posture_threshold
        self.FRAME_WINDOW = st.image([])

        # Audio Handling
        self.lastTime = 0
        pygame.mixer.init()
        sound_path = "assests/warning.wav"
        self.warning_sound = pygame.mixer.Sound(sound_path)

        # Calibration
        self.baseline = None

        # For error handling
        # Too dark
        self.dark_warning_placeholder = st.empty()
        self.no_cam_warning_placeholder = st.empty()
        self.too_dark = False
        self.has_warned_dark = False
        self.brightness_threshold = 40
    
    def run(self):
        calibrate = st.button("Calibrate Good Posture")

        if calibrate:
            self.calibrate(duration=3)
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("hello")
                with self.no_cam_warning_placeholder.container():
                    st.warning("⚠️ No camera feed — trying to reconnect...")
                self.reconnect_camera()
                break

            # Check brightness
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)

            if brightness < self.brightness_threshold:
                if not self.has_warned_dark:
                    with self.dark_warning_placeholder.container():
                        st.warning("⚠️ Too dark — please improve lighting!")
                    self.has_warned_dark = True
                self.too_dark = True
            else:
                self.too_dark = False
                self.has_warned_dark = False
                self.dark_warning_placeholder.empty()

            # Convert to RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb)

            # Draw pose landmarks
            self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                posture_ratio = self.read_posture(landmarks)

                self.add_text(frame, posture_ratio)
            self.FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        self.cap.release()
    
    def read_posture(self,landmarks):
        nose = landmarks[0]
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        # use shoulder length to standardize ratio depending on distance
        left_shoulder_x = left_shoulder.x
        right_shoulder_x = right_shoulder.x
        shoulder_Length = left_shoulder_x - right_shoulder_x 
        
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        nose_y = nose.y

        posture_ratio = (shoulder_y - nose_y) / shoulder_Length

        return posture_ratio

    def add_text(self, frame, posture_ratio):
        if self.baseline:
            threshold = self.baseline * 0.85  # 90% of calibrated good posture
        else:
            threshold = self.posture_threshold
        cv2.putText(frame, f"Posture Ratio: {posture_ratio:.4f}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(frame, f"Press ESC to quit", (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        if posture_ratio > threshold:
            cv2.putText(frame, "Good posture", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        else:
            cv2.putText(frame, "Bad posture", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            self.handle_audio_alert(posture_ratio)
    
    def reconnect_camera(self):
        self.cap.release()
        time.sleep(0.5)
        self.cap = cv2.VideoCapture(0)
        
    def handle_audio_alert(self, posture_ratio):
        """Play a sound when posture is bad, but not more than once per 3 seconds."""
        if posture_ratio <= self.posture_threshold:
            if time.time() - self.lastTime > 3:
                self.lastTime = time.time()
                if self.warning_sound:
                    self.warning_sound.play()

    def calibrate(self, duration=3):
        """Collect posture ratios for a few seconds to compute baseline."""
        st.info("Sit upright — calibrating posture...")
        ratios = []
        start = time.time()

        while time.time() - start < duration:
            ret, frame = self.cap.read()
            if not ret:
                continue
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb)

            if results.pose_landmarks:
                ratio = self.read_posture(results.pose_landmarks.landmark)
                ratios.append(ratio)
                self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

            self.FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if ratios:
            self.baseline = np.mean(ratios)
            b = self.baseline * 0.85
            st.success(f"✅ Calibration complete. Baseline posture ratio: {b:.3f}")
        else:
            st.error("⚠️ Calibration failed — no pose detected.")

if __name__ == "__main__":
    detector = PoseDetector()
    detector.run()