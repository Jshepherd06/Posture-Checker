from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter # Used for formatting the X-axis
import matplotlib.pyplot as plt

class StatisticsWidget(QWidget):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        
        # Set up Matplotlib Figure and Canvas
        self.figure = Figure(figsize=(10, 5))
        self.canvas = FigureCanvas(self.figure)
        self.axis = self.figure.add_subplot(111)
        
        # Layout
        main_layout = QVBoxLayout(self)
        title_label = QLabel("📊 Session History")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        self.status_label = QLabel("Session Duration: 0m")
        
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.canvas)
        
        self.data_manager.new_ratio_data.connect(self.update_graph)
        self.update_graph()

    def format_time(self, x, pos):
        """Helper to format X-axis labels (Seconds vs Minutes)"""
        if x < 60:
            return f"{int(x)}s"
        else:
            return f"{int(x/60)}m"

    def update_graph(self):
        relative_times, ratios = self.data_manager.get_latest_data()
        
        self.axis.clear()
        
        if relative_times and ratios:
            self.axis.plot(relative_times, ratios, label='Avg Posture (1s)', color='skyblue')
            
            # Use the time formatter defined above
            self.axis.xaxis.set_major_formatter(FuncFormatter(self.format_time))
            
            self.axis.set_title("Posture Ratio Over Time")
            self.axis.set_xlabel("Time (Session Duration)")
            self.axis.set_ylabel("Posture Ratio")
            self.axis.grid(True, linestyle=':', alpha=0.6)
            self.axis.set_ylim(0.4, 1.2)
            self.axis.legend()

            # Update text label
            total_seconds = relative_times[-1]
            if total_seconds > 60:
                self.status_label.setText(f"Session Duration: {total_seconds/60:.1f} minutes")
            else:
                self.status_label.setText(f"Session Duration: {int(total_seconds)} seconds")
        else:
             self.axis.text(0.5, 0.5, "No Data Yet", ha='center', va='center')

        self.canvas.draw()