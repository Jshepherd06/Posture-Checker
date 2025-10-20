import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    # Draw pose landmarks
    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        nose = landmarks[0]
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
        nose_y = nose.y

        posture_ratio = shoulder_y - nose_y

        cv2.putText(frame, f"Posture Ratio: {posture_ratio:.4f}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        if posture_ratio > 0.24:
            cv2.putText(frame, "Good posture", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        else:
            cv2.putText(frame, "Bad posture!", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    cv2.imshow('Posture Checker', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()