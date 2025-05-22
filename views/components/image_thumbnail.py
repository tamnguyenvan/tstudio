from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage, QColor
from models import ImageModel

class ImageThumbnail(QFrame):
    """Thumbnail widget for displaying images"""
    
    def __init__(self, image_model: ImageModel, parent=None):
        super().__init__(parent)
        self.image_model = image_model
        self._setup_ui()
        self._load_image()
        
    def _setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f8f8;
                border: 1px solid #ddd;
                border-radius: 12px;
            }
        """)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(10)

        # Image label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(150, 150)
        self.image_label.setMaximumSize(200, 200)
        self.image_label.setStyleSheet("""
            QLabel {
                border: none;
                border-radius: 8px;
                background-color: #ffffff;
            }
        """)

        # Filename label
        self.name_label = QLabel(self.image_model.filename)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #555;
                font-weight: 500;
                border: none;
            }
        """)

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.name_label)
        self.setLayout(self.layout)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 45)) 
        self.setGraphicsEffect(shadow)
    
    def _load_image(self):
        """Load and display the image"""
        if self.image_model.is_processed and self.image_model.processed_image:
            pixmap = QPixmap.fromImage(self.image_model.processed_image)
        else:
            pixmap = QPixmap(self.image_model.path)
        
        # Scale pixmap while maintaining aspect ratio
        pixmap = pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
    
    def update_with_processed_image(self, processed_image: QImage):
        """Update thumbnail with processed image"""
        self.image_model.set_processed_image(processed_image)
        self._load_image()