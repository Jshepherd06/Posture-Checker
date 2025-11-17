import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainAppWindow  # Import your main window class

if __name__ == "__main__":
    # 1. Create the application instance.
    #    sys.argv allows passing command-line arguments to the app.
    app = QApplication(sys.argv)
    
    # 2. Create an instance of your main window.
    #    The MainAppWindow class (in main_window.py) will
    #    create the AppSettings and all the page widgets.
    window = MainAppWindow()
    
    # 3. Show the main window to the user.
    window.show()
    
    # 4. Start the application's event loop.
    #    This line blocks until the user closes the app.
    #    sys.exit() ensures a clean exit.
    sys.exit(app.exec())