import cv2
import mediapipe as mp
import streamlit as st
import numpy as np
import time
from pathlib import Path
import pygame

class PoseDetector:
    def __init__(self,settings):
        # Mediapipe pose setup
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

        # Video capture setup
        self.cap = cv2.VideoCapture(0)
        self.posture_threshold = settings["posture_threshold"]
        self.FRAME_WINDOW = st.image([])

        # Audio Handling
        self.lastTime = 0 # for determining whether to play warning again
        self.warning_wait = settings["warning_wait"] # wait time before next warning
        pygame.mixer.init()
        sound_path = "assests/warning.wav"
        self.warning_sound = pygame.mixer.Sound(sound_path)
        self.sound_enabled = settings["sound_enabled"]

        # Calibration
        self.baseline = None
        self.calibration_duration = settings["calibration_duration"]
        self.posture_strictness = settings["posture_strictness"] # percent of ideal posture before failure

        # For error handling
        # Too dark
        self.dark_warning_placeholder = st.empty()
        self.no_cam_warning_placeholder = st.empty()
        self.too_dark = False
        self.has_warned_dark = False
        self.brightness_threshold = 40
    
    
    # Loop that runs camera
    def run(self):
        # calibration button
        calibrate = st.button("Calibrate Good Posture")

        if calibrate:
            self.calibrate(self.calibration_duration)
        
        while True:
            ret, frame = self.cap.read() # read a fram from camera
            if not ret: # if failed to read frame, try to reconnect
                with self.no_cam_warning_placeholder.container():
                    st.warning("⚠️ No camera feed — trying to reconnect...")
                self.reconnect_camera()
                break

            # Check brightness
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(gray)

            # if camera is too dark, throw warning
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

                # posture analysis and add text
                posture_ratio = self.read_posture(landmarks)
                self.add_text(frame, posture_ratio)
            self.FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        self.cap.release()
    
    # returns posture ratio from mediapipe landmarks.
    def read_posture(self,landmarks):
        nose = landmarks[0]
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        # use shoulder length to standardize ratio depending on distance
        left_shoulder_x = left_shoulder.x
        right_shoulder_x = right_shoulder.x
        shoulder_Length = left_shoulder_x - right_shoulder_x 
        
        # use difference in shoulder and nose height for posture analysis
        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        nose_y = nose.y

        posture_ratio = (shoulder_y - nose_y) / shoulder_Length

        return posture_ratio

    # adds text onto the camera feed, also handles warning audio
    def add_text(self, frame, posture_ratio):
        if self.baseline:
            threshold = self.baseline * self.posture_strictness
        else:
            threshold = self.posture_threshold
        cv2.putText(frame, f"Posture Ratio: {posture_ratio:.4f}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(frame, f"Press ESC to quit", (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        if posture_ratio > threshold:
            cv2.putText(frame, "Good posture", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        else:
            cv2.putText(frame, "Bad posture", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            self.handle_audio_alert(posture_ratio)
    
    # tries to reconnect camera in case of failure
    def reconnect_camera(self):
        self.cap.release()
        time.sleep(0.5)
        self.cap = cv2.VideoCapture(0)
        
    # plays audio if posture_ratio below threshold
    def handle_audio_alert(self, posture_ratio):
        """Play a sound when posture is bad, but not more than once per 3 seconds."""
        if (posture_ratio <= self.posture_threshold) and self.sound_enabled:
            if time.time() - self.lastTime > self.warning_wait:
                self.lastTime = time.time()
                if self.warning_sound:
                    self.warning_sound.play()

    # calibration for personalized posture ratio
    def calibrate(self, duration=3):
        """Collect posture ratios for a few seconds to compute baseline."""
        st.info("Sit upright — calibrating posture...")
        ratios = []
        start = time.time()

        # read frames during calibration period, store posture ratios into an array
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
            b = self.baseline * self.posture_strictness
            st.success(f"✅ Calibration complete. Baseline posture ratio: {b:.3f}")
        else:
            st.error("⚠️ Calibration failed — no pose detected.")

if __name__ == "__main__":
    st.set_page_config(page_title="Posture Detector", layout="wide")
    detector = PoseDetector(settings=st.session_state.pose_settings)
    detector.run()