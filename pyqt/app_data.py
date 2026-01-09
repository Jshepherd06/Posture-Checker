from PyQt6.QtCore import QObject, pyqtSignal
import time
import numpy as np

class AppDataManager(QObject):
    """
    Manages the posture data log by averaging frames into 1-second chunks,
    and calculates ongoing session statistics.
    """
    # Signal to notify the statistics page that new data is available
    new_ratio_data = pyqtSignal()

    def __init__(self, settings, parent=None): 
        super().__init__(parent)
        self.settings = settings
        
        # This will hold the long-term history (1 point per second)
        # Format: (timestamp, average_ratio)
        self.posture_log = []
        
        # This acts as a temporary buffer to calculate the 1-second average
        self.second_buffer = []
        self.last_save_time = time.time()

        # Capacity: ~10 hours of 1-second data points
        self.MAX_LOG_SIZE = 36000 

    def add_ratio(self, ratio):
        """
        Called by the thread every frame (~30 times/sec).
        Buffers data and saves an average 1-second chunk to the log.
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
        Retrieves the entire session history for plotting.
        """
        if not self.posture_log:
            return [], []
            
        timestamps, ratios = zip(*self.posture_log)
        
        # Convert timestamps to relative time (seconds since start)
        start_time = timestamps[0]
        relative_times = [(t - start_time) for t in timestamps]
        
        return relative_times, list(ratios)

    def calculate_posture_stats(self):
        """
        Calculates the total duration, percentage of good posture time, and 
        the longest streak of good posture (above threshold).
        Returns: (total_duration_s, percent_good, longest_streak_s, active_threshold)
        """
        if not self.posture_log:
            return 0.0, 0.0, 0.0, 0.0 

        # 1. Determine the active threshold (Calibration takes precedence)
        baseline = self.settings.get("baseline")
        strictness = self.settings.get("posture_strictness")
        default_threshold = self.settings.get("posture_threshold")
        
        if baseline > 0:
            active_threshold = baseline * strictness
        else:
            active_threshold = default_threshold
        
        timestamps, ratios = zip(*self.posture_log)
        
        total_duration_s = timestamps[-1] - timestamps[0]
        if total_duration_s == 0:
             return 0.0, 0.0, 0.0, active_threshold

        # 2. Calculate time above threshold (good posture) and longest streak
        good_posture_time_s = 0.0
        longest_streak_s = 0.0
        current_streak_s = 0.0
        
        # Iterate through the 1-second averaged data points
        for i in range(len(self.posture_log)):
            ratio = self.posture_log[i][1] # Get the ratio
            time_interval_s = 1.0 
            
            is_good = ratio > active_threshold
            
            if is_good:
                good_posture_time_s += time_interval_s
                current_streak_s += time_interval_s
            else:
                # Streak is broken, save if it's the longest
                if current_streak_s > longest_streak_s:
                    longest_streak_s = current_streak_s
                current_streak_s = 0.0

        # Check the final streak when the loop ends
        if current_streak_s > longest_streak_s:
            longest_streak_s = current_streak_s

        percent_good = (good_posture_time_s / total_duration_s) * 100
        
        return total_duration_s, percent_good, longest_streak_s, active_threshold