from PyQt6.QtCore import QObject, pyqtSignal
import time

class AppDataManager(QObject):
    """
    Manages the posture data log and emits signals when new data is added.
    """
    # Signal to notify the statistics page that new data is available
    new_ratio_data = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Store data as a list of (timestamp, posture_ratio)
        self.posture_log = []
        # Store the current window of data for the graph
        self.last_60_seconds = [] 

        # We will keep a limit on how much data to store to prevent memory issues
        self.MAX_LOG_SIZE = 1800 # ~30 minutes at 1 update per second

    def add_ratio(self, ratio):
        """
        Called by the PoseDetectorThread to record a new data point.
        """
        current_time = time.time()
        new_point = (current_time, ratio)
        
        # 1. Add to the full log
        self.posture_log.append(new_point)
        
        # 2. Trim the log if it exceeds the max size
        if len(self.posture_log) > self.MAX_LOG_SIZE:
            self.posture_log.pop(0)

        # 3. Update the rolling 60-second window
        one_minute_ago = current_time - 60
        self.last_60_seconds = [p for p in self.posture_log if p[0] >= one_minute_ago]
        
        # 4. Emit signal to update the statistics page
        self.new_ratio_data.emit()

    def get_latest_data(self):
        """
        Called by StatisticsWidget to fetch the data for the graph.
        Returns two lists: timestamps (x-axis) and ratios (y-axis)
        """
        if not self.last_60_seconds:
            return [], []
            
        timestamps, ratios = zip(*self.last_60_seconds)
        
        # Convert timestamps to relative seconds for better plotting
        start_time = timestamps[0]
        relative_times = [(t - start_time) for t in timestamps]
        
        return relative_times, list(ratios)