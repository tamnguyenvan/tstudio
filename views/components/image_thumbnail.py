from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from models import ImageModel

class ImageThumbnail(QFrame):
    """Thumbnail widget for displaying images"""
    
    def __init__(self, image_model: ImageModel, parent=None):
        super().__init__(parent)
        self.setObjectName("thumbnailFrame")
        self.image_model = image_model
        self._setup_ui()
        self._load_image()
        
    def _setup_ui(self):
        # Change to horizontal layout
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(0)

        # Image label
        self.image_label = QLabel()
        self.image_label.setObjectName("imageLabel")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedSize(80, 80)

        # Filename label
        self.name_label = QLabel(self.image_model.filename)
        self.name_label.setObjectName("nameLabel")
        self.name_label.setWordWrap(True)

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.name_label)
        self.layout.addStretch()
        self.setLayout(self.layout)
    
    def _load_image(self):
        """Load and display the image"""
        if self.image_model.is_processed and self.image_model.processed_image:
            pixmap = QPixmap.fromImage(self.image_model.processed_image)
        else:
            pixmap = QPixmap(self.image_model.path)
        
        # Scale pixmap while maintaining aspect ratio
        pixmap = pixmap.scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
    
    def update_with_processed_image(self, processed_image: QImage):
        """Update thumbnail with processed image"""
        self.image_model.set_processed_image(processed_image)
        self._load_image()