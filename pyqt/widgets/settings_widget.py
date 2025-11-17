from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QSlider, QCheckBox, QLabel
from PyQt6.QtCore import Qt
# from app_settings import AppSettings # This would be passed in __init__

class SettingsWidget(QWidget):
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        layout = QFormLayout(self)
        
        # Equivalent of st.slider
        self.strictness_slider = QSlider(Qt.Orientation.Horizontal)
        self.strictness_slider.setRange(50, 100) # 0.5 -> 1.0 (as percent)
        self.strictness_slider.setValue(int(self.settings.get("posture_strictness") * 100))
        
        # Connect the slider's 'valueChanged' signal to a function
        self.strictness_slider.valueChanged.connect(self.on_strictness_changed)
        layout.addRow("Posture Strictness (%):", self.strictness_slider)

        # Equivalent of st.toggle
        self.sound_toggle = QCheckBox("Enable warning sound")
        self.sound_toggle.setChecked(self.settings.get("sound_enabled"))
        self.sound_toggle.toggled.connect(self.on_sound_toggled)
        layout.addRow(self.sound_toggle)
        # ... add other settings ...

    def on_strictness_changed(self, value):
        # value is an int (50-100), save it as a float (0.5-1.0)
        self.settings.set("posture_strictness", value / 100.0)

    def on_sound_toggled(self, checked):
        self.settings.set("sound_enabled", checked)