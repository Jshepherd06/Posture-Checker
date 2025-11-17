import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainAppWindow

if __name__ == "__main__":
    # Create the application instance.
    # sys.argv allows passing command-line arguments to the app.
    app = QApplication(sys.argv)
    
    # Create an instance of your main window.
    window = MainAppWindow()
    
    # Show the main window to the user.
    window.show()
    
    # Start the application's event loop.
    # sys.exit() ensures a clean exit.
    sys.exit(app.exec())