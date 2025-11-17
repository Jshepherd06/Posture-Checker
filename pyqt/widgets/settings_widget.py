from PyQt6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QFormLayout, 
    QSlider, 
    QCheckBox, 
    QLabel, 
    QGroupBox
)
from PyQt6.QtCore import Qt

class SettingsWidget(QWidget):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        
        # Main layout for the entire page
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Title
        title_label = QLabel(" Posture Detector Settings")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title_label)
        main_layout.addSpacing(20)
        
        # --- Group 1: Posture Sensitivity (No Calibration) ---
        no_calib_group = QGroupBox(" Posture Sensitivity Without Calibration")
        no_calib_layout = QFormLayout(no_calib_group)

        #  Posture Threshold (0.5 to 1.0)
        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setRange(50, 100)
        # Convert stored float (e.g., 0.75) to integer slider value (75)
        initial_threshold = int(self.settings.get("posture_threshold") * 100)
        self.threshold_slider.setValue(initial_threshold)
        self.threshold_slider.valueChanged.connect(self.on_threshold_changed)
        no_calib_layout.addRow("Good/Bad Posture Threshold (x/100):", self.threshold_slider)

        main_layout.addWidget(no_calib_group)
        
        # --- Group 2: Calibration Settings ---
        calib_group = QGroupBox("📐 Calibration & Strictness")
        calib_layout = QFormLayout(calib_group)

        #  Posture Strictness (0.5 to 1.0) - Already implemented in prior steps
        self.strictness_slider = QSlider(Qt.Orientation.Horizontal)
        self.strictness_slider.setRange(50, 100)
        initial_strictness = int(self.settings.get("posture_strictness") * 100)
        self.strictness_slider.setValue(initial_strictness)
        self.strictness_slider.valueChanged.connect(self.on_strictness_changed)
        calib_layout.addRow("Strictness (% of baseline, x/100):", self.strictness_slider)

        #  Calibration Duration (1 to 10 seconds)
        self.duration_slider = QSlider(Qt.Orientation.Horizontal)
        self.duration_slider.setRange(1, 10)
        self.duration_slider.setValue(self.settings.get("calibration_duration"))
        self.duration_slider.valueChanged.connect(self.on_duration_changed)
        calib_layout.addRow("Calibration Duration (seconds):", self.duration_slider)

        main_layout.addWidget(calib_group)
        
        # --- Group 3: Audio & Alerts ---
        audio_group = QGroupBox(" Audio & Alerts")
        audio_layout = QFormLayout(audio_group)

        #  Warning Cooldown (1 to 10 seconds)
        self.wait_slider = QSlider(Qt.Orientation.Horizontal)
        self.wait_slider.setRange(1, 10)
        self.wait_slider.setValue(self.settings.get("warning_wait"))
        self.wait_slider.valueChanged.connect(self.on_wait_changed)
        audio_layout.addRow("Cooldown between warnings (seconds):", self.wait_slider)
        
        #  Sound Enabled (Toggle/CheckBox)
        self.sound_toggle = QCheckBox("Enable warning sound")
        self.sound_toggle.setChecked(self.settings.get("sound_enabled"))
        self.sound_toggle.toggled.connect(self.on_sound_toggled)
        audio_layout.addWidget(self.sound_toggle)

        main_layout.addWidget(audio_group)
        main_layout.addStretch(1) # Push everything to the top

    # Functions to handle widget changes -------
    
    def on_threshold_changed(self, value):
        # Converts integer (50-100) to float (0.5-1.0) and saves
        self.settings.set("posture_threshold", value / 100.0)
        
    def on_strictness_changed(self, value):
        # Converts integer (50-100) to float (0.5-1.0) and saves
        self.settings.set("posture_strictness", value / 100.0)

    def on_duration_changed(self, value):
        # Saves integer value (1-10) directly
        self.settings.set("calibration_duration", value)

    def on_wait_changed(self, value):
        # Saves integer value (1-10) directly
        self.settings.set("warning_wait", value)

    def on_sound_toggled(self, checked):
        # Saves boolean value (True/False) directly
        self.settings.set("sound_enabled", checked)