import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QListWidget, QWidget, 
    QHBoxLayout, QListWidgetItem
)

# Import your new page widgets
from widgets.homepage_widget import HomePageWidget
from widgets.pose_detector_widget import PoseDetectorWidget
from widgets.settings_widget import SettingsWidget
from widgets.stats_widget import StatisticsWidget
from app_settings import AppSettings # A new class to manage QSettings

class MainAppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Posture Checker")
        self.setGeometry(100, 100, 1200, 800)

        # Load/create settings
        self.settings = AppSettings()

        # Main layout
        central_widget = QWidget()
        self.main_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # --- Navigation ---
        self.nav_list = QListWidget()
        self.nav_list.setFixedWidth(150)
        self.main_layout.addWidget(self.nav_list)

        # --- Page Stack ---
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        # --- Create and Add Pages ---
        # Pass the settings object to the widgets that need it
        self.home_page = HomePageWidget()
        self.pose_page = PoseDetectorWidget(self.settings) 
        self.settings_page = SettingsWidget(self.settings)
        self.stats_page = StatisticsWidget()

        self.stacked_widget.addWidget(self.home_page)    # Index 0
        self.stacked_widget.addWidget(self.pose_page)     # Index 1
        self.stacked_widget.addWidget(self.settings_page) # Index 2
        self.stacked_widget.addWidget(self.stats_page)   # Index 3

        # Add items to navigation list
        self.nav_list.addItem("Home")
        self.nav_list.addItem("Pose Detector")
        self.nav_list.addItem("Settings")
        self.nav_list.addItem("Statistics")

        # --- Connect Navigation ---
        self.nav_list.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

        # --- Connect "Get Started" button from home page ---
        self.home_page.get_started_button.clicked.connect(self.go_to_pose_detector)

        # Select first page
        self.nav_list.setCurrentRow(0)

    def go_to_pose_detector(self):
        self.nav_list.setCurrentRow(1) # This will trigger the signal to change page

    def closeEvent(self, event):
        self.pose_page.stop_worker_thread()
        event.accept()


# In main.py
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainAppWindow()
    window.show()
    sys.exit(app.exec())