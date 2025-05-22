import sys
from PySide6.QtWidgets import QApplication

from views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for consistent look across platforms
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()