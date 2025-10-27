import cv2
import mediapipe as mp
import streamlit as st

class PoseDetector:
    def __init__(self,posture_threshold=0.75):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils

        self.cap = cv2.VideoCapture(0)
        self.posture_threshold = posture_threshold
        self.FRAME_WINDOW = st.image([])
    
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

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
        cv2.putText(frame, f"Posture Ratio: {posture_ratio:.4f}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        cv2.putText(frame, f"Press ESC to quit", (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        if posture_ratio > 0.75:
            cv2.putText(frame, "Good posture", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        else:
            cv2.putText(frame, "Bad posture", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

if __name__ == "__main__":
    detector = PoseDetector()
    detector.run()