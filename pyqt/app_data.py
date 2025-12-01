from PyQt6.QtCore import QObject, pyqtSignal
import time
import numpy as np

class AppDataManager(QObject):
    # Signal to notify the statistics page that new data is available
    new_ratio_data = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # This will hold the long-term history (1 point per second)
        # Format: (timestamp, average_ratio)
        self.posture_log = []
        
        # This acts as a temporary buffer to calculate the 1-second average
        self.second_buffer = []
        self.last_save_time = time.time()

        # Capacity: 10 hours * 60 mins * 60 secs = 36,000 points
        self.MAX_LOG_SIZE = 36000 

    def add_ratio(self, ratio):
        """
        Called by the thread every frame (~30 times/sec).
        We buffer these and average them into 1-second chunks.
        """
        current_time = time.time()
        self.second_buffer.append(ratio)

        # If 1 second has passed since the last save...
        if current_time - self.last_save_time >= 1.0:
            if self.second_buffer:
                # Calculate average of the last second
                avg_ratio = np.mean(self.second_buffer)
                
                # Save to long-term log
                self.posture_log.append((current_time, avg_ratio))
                
                # Reset buffer and timer
                self.second_buffer = []
                self.last_save_time = current_time
                
                # Trim log if too big
                if len(self.posture_log) > self.MAX_LOG_SIZE:
                    self.posture_log.pop(0)

                # Emit signal to update graph (now only happens once per second!)
                self.new_ratio_data.emit()

    def get_latest_data(self):
        """
        Returns the entire session history.
        """
        if not self.posture_log:
            return [], []
            
        timestamps, ratios = zip(*self.posture_log)
        
        # Convert timestamps to relative time (seconds since start)
        start_time = timestamps[0]
        relative_times = [(t - start_time) for t in timestamps]
        
        return relative_times, list(ratios)