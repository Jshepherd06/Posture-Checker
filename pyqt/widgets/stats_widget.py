from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter 
import matplotlib.pyplot as plt

# NOTE: MainAppWindow must be updated to pass self.settings to this class:
# self.stats_page = StatisticsWidget(self.settings, self.data_manager) 
class StatisticsWidget(QWidget):
    def __init__(self, settings, data_manager, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.data_manager = data_manager
        
        # Set up Matplotlib Figure and Canvas
        self.figure = Figure(figsize=(10, 5))
        self.canvas = FigureCanvas(self.figure)
        self.axis = self.figure.add_subplot(111)
        
        # Layout
        main_layout = QVBoxLayout(self)
        title_label = QLabel("Session History")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        # Labels for the new statistics
        self.status_label = QLabel("Session Duration: 0s")
        self.percent_label = QLabel("Time Good Posture: 0.0%")
        self.streak_label = QLabel("Longest Good Streak: 0s")
        self.threshold_label = QLabel("Active Threshold: N/A")

        main_layout.addWidget(title_label)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.percent_label)
        main_layout.addWidget(self.streak_label)
        main_layout.addWidget(self.threshold_label)
        main_layout.addWidget(self.canvas)
        
        self.data_manager.new_ratio_data.connect(self.update_graph)
        self.update_graph()

    def format_time(self, x, pos):
        """Helper to format X-axis labels (Seconds vs Minutes)"""
        if x < 60:
            return f"{int(x)}s"
        else:
            return f"{int(x/60)}m"

    def format_duration(self, seconds):
        """Converts total seconds into Hh Mmin Ss format."""
        if seconds < 60:
            return f"{int(seconds)}s"
        minutes = int(seconds / 60)
        seconds = int(seconds % 60)
        if minutes < 60:
            return f"{minutes}m {seconds}s"
        
        hours = int(minutes / 60)
        minutes = int(minutes % 60)
        return f"{hours}h {minutes}m {seconds}s"


    def update_graph(self):
        relative_times, ratios = self.data_manager.get_latest_data()
        
        # NEW: Get the calculated statistics
        total_s, percent_good, longest_streak_s, threshold = self.data_manager.calculate_posture_stats() 
        
        self.axis.clear()
        
        # Update text labels
        self.status_label.setText(f"Session Duration: {self.format_duration(total_s)}")
        self.percent_label.setText(f"Time Good Posture: {percent_good:.1f}%")
        self.streak_label.setText(f"Longest Good Streak: {self.format_duration(longest_streak_s)}")
        self.threshold_label.setText(f"Active Threshold: {threshold:.3f}")

        if relative_times and ratios:
            self.axis.plot(relative_times, ratios, label='Avg Posture (1s)', color='skyblue')
            
            # Plot the threshold line
            self.axis.axhline(threshold, color='red', linestyle='--', label=f'Threshold ({threshold:.3f})')
            
            self.axis.xaxis.set_major_formatter(FuncFormatter(self.format_time))
            
            self.axis.set_title("Posture Ratio Over Time")
            self.axis.set_xlabel("Time (Session Duration)")
            self.axis.set_ylabel("Posture Ratio")
            self.axis.grid(True, linestyle=':', alpha=0.6)
            self.axis.set_ylim(0.4, 1.2)
            self.axis.legend()
        else:
             self.axis.text(0.5, 0.5, "No Data Yet", ha='center', va='center')

        self.canvas.draw()