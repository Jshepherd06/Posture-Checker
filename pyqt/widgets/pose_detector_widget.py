from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt
from core.pose_detector_thread import PoseDetectorThread

class PoseDetectorWidget(QWidget):
    def __init__(self, settings, data_manager, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.data_manager = data_manager 

        # --- UI Layout ---
        layout = QVBoxLayout(self)
        
        self.video_label = QLabel("Starting camera...")
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: black;")
        
        # --- FIX IS HERE ---
        # We set the policy to 'Expanding' so the video resizes with the window
        self.video_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        
        layout.addWidget(self.video_label, 1)

        # Status and warning labels
        self.status_label = QLabel("Status: Awaiting data")
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: red; font-size: 14px;")

        self.calibrate_button = QPushButton("Calibrate Good Posture")
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.warning_label)
        layout.addWidget(self.calibrate_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- Setup Worker Thread ---
        self.worker = PoseDetectorThread(self.settings, self.data_manager)
        
        # --- Connect Signals to Slots ---
        self.worker.frame_ready.connect(self.update_video_frame)
        self.worker.posture_status.connect(self.update_posture_label)
        self.worker.system_warning.connect(self.update_warning_label)
        self.worker.calibration_status.connect(self.update_calibration_status)
        
        self.calibrate_button.clicked.connect(self.worker.start_calibration)
        
        # --- Start the thread ---
        self.worker.start()

    # --- Slot Functions ---
    def update_video_frame(self, cv_image):
        """Converts OpenCV image to QPixmap and displays it."""
        h, w, ch = cv_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(cv_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(
            self.video_label.size(), 
            Qt.AspectRatioMode.KeepAspectRatio, 
            Qt.TransformationMode.SmoothTransformation
        )
        self.video_label.setPixmap(scaled_pixmap)

    def update_posture_label(self, text, color):
        self.status_label.setText(f"Status: {text}")
        self.status_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {color};")

    def update_warning_label(self, text):
        self.warning_label.setText(text)
        
    def update_calibration_status(self, text):
        self.status_label.setText(text)

    def stop_worker_thread(self):
        self.worker.stop()
        self.worker.quit()
        self.worker.wait()