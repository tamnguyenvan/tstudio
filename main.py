import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase

from views.main_window import MainWindow
from utils.platform_utils import RESOURCES_PATH

def main():
    app = QApplication(sys.argv)
    fonts = [
        "SF-Pro Display Regular",
        # "SF Pro Display Medium",
        # "SF Pro Display Semibold",
        # "SF Pro Display Bold",
        # "SF Pro Display Black",
    ]
    for font in fonts:
        QFontDatabase.addApplicationFont(str(RESOURCES_PATH / "fonts/" / (font + ".otf")))
    app.setStyle('Fusion')  # Use Fusion style for consistent look across platforms
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()