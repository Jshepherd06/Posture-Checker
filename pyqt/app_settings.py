from PyQt6.QtCore import QSettings

class AppSettings:
    """
    A wrapper for QSettings to manage persistent application settings.
    This replaces the Streamlit session_state.
    """
    def __init__(self):
        # define organization application name.
        # this tells QSettings where to save the settings on the users OS.
        self.settings = QSettings("PostureAppCompany", "PostureApp")
        
        # default values
        self.defaults = {
            "posture_threshold": 0.75,
            "posture_strictness": 0.85,
            "warning_wait": 3,
            "calibration_duration": 3,
            "sound_enabled": True,
        }
        
        # Ensure all default settings are populated on first launch
        self._initialize_defaults()

    def _initialize_defaults(self):
        """
        Writes any default values that are not already in the settings file.
        """
        for key, value in self.defaults.items():
            if not self.settings.contains(key):
                self.settings.setValue(key, value)

    def get(self, key):
        """
        Gets a setting value.
        It will automatically convert types (e.g., "true" to True).
        """
        # Get the value, falling back to the default if it doesn't exist
        default_value = self.defaults.get(key)
        
        # QSettings.value() can automatically handle type conversion
        if isinstance(default_value, bool):
            return self.settings.value(key, default_value, type=bool)
        if isinstance(default_value, int):
            return self.settings.value(key, default_value, type=int)
        if isinstance(default_value, float):
            return self.settings.value(key, default_value, type=float)
            
        return self.settings.value(key, default_value)

    def set(self, key, value):
        """
        Saves a setting value persistently.
        """
        if key in self.defaults:
            self.settings.setValue(key, value)
        else:
            print(f"Warning: Attempted to set unknown setting '{key}'")