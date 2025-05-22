from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt

class GalleryHeader(QWidget):
    """Header widget for the gallery"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("galleryHeader")
        # self.setFixedHeight(50)
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI components"""
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Gallery title
        self.title_label = QLabel("Image Gallery")
        self.title_label.setObjectName("galleryTitle")
        self.layout.addWidget(self.title_label)
        
        # Spacer
        self.layout.addStretch()
        
        self.setLayout(self.layout)
    
    def set_title(self, title: str):
        """Set the gallery title"""
        self.title_label.setText(title)