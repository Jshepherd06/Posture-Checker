from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class HomePageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Welcome header
        title_label = QLabel("Welcome!")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        
        # Title of program
        subtitle_label = QLabel("Posture Checker")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 24px;")

        # Get started button
        self.get_started_button = QPushButton("Get Started")
        self.get_started_button.setFixedSize(200, 50)

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addSpacing(40)
        layout.addWidget(self.get_started_button, alignment=Qt.AlignmentFlag.AlignCenter)