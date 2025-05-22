from PySide6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QLabel, QSizePolicy)
from PySide6.QtCore import Qt
from typing import Dict, Optional
from models import ImageModel
from .components import ImageThumbnail

class ListView(QWidget):
    """List view for displaying images vertically"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thumbnails: Dict[str, ImageThumbnail] = {}
        self.empty_label: Optional[QLabel] = None
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup list view UI"""
        self.layout = QVBoxLayout()
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create empty state label
        self.empty_label = QLabel("No images added yet\nDrop images to get started")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setObjectName("emptyStateLabel")
        self.empty_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.empty_label.setMinimumSize(200, 200)  # Set a minimum size to ensure visibility
        self.empty_label.setWordWrap(True)
        self.empty_label.setVisible(True)
        
        self.container_widget = QWidget()
        self.container_widget.setObjectName("listViewContainer")
        self.container_layout = QVBoxLayout(self.container_widget)
        self.container_layout.setSpacing(8)
        self.container_layout.setAlignment(Qt.AlignTop)
        
        # Add empty label to container
        self.container_layout.addWidget(self.empty_label)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.container_widget)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
        
    def add_image(self, image_model: str | ImageModel):
        """Add image to list view"""
        if isinstance(image_model, str):
            image_model = ImageModel(image_model)
        thumbnail = ImageThumbnail(image_model)
        self.container_layout.addWidget(thumbnail)
        self.thumbnails[image_model.path] = thumbnail
        
        # Hide empty state if this is the first image
        if len(self.thumbnails) == 1 and self.empty_label:
            self.empty_label.setVisible(False)
            
    def update_image(self, path: str, processed_image):
        """Update an image with processed version"""
        if path in self.thumbnails:
            self.thumbnails[path].update_with_processed_image(processed_image)
            
    def clear(self):
        """Clear all images"""
        for thumbnail in self.thumbnails.values():
            thumbnail.deleteLater()
        self.thumbnails.clear()
        # Show empty state when all images are cleared
        if self.empty_label:
            self.empty_label.setVisible(True)