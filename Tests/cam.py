import cv2

cap = cv2.VideoCapture(0)  # 0 = default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('your face', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # press ESC to quit
        break

cap.release()
cv2.destroyAllWindows()