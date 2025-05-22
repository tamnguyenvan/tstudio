from PySide6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QGridLayout)
from PySide6.QtCore import Qt
from typing import Dict, List
from models import ImageModel
from .components import ImageThumbnail

class BaseGalleryView(QWidget):
    """Base class for gallery views"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thumbnails: Dict[str, ImageThumbnail] = {}
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup base UI - to be overridden"""
        pass
    
    def _macos_scrollbar_style(self) -> str:
        return """
        QScrollBar:vertical {
            background: transparent;
            width: 8px;
            margin: 0px 2px 0px 2px;
        }

        QScrollBar::handle:vertical {
            background: rgba(0, 0, 0, 60%);
            min-height: 20px;
            border-radius: 4px;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0;
            background: none;
        }

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;
        }

        QScrollBar:horizontal {
            background: transparent;
            height: 8px;
            margin: 2px 0px 2px 0px;
        }

        QScrollBar::handle:horizontal {
            background: rgba(0, 0, 0, 60%);
            min-width: 20px;
            border-radius: 4px;
        }

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            width: 0;
            background: none;
        }

        QScrollBar::add-page:horizontal,
        QScrollBar::sub-page:horizontal {
            background: none;
        }
        """

    def add_images(self, image_models: list[ImageModel]):
        """Add multiple images to the view"""
        for model in image_models:
            self.add_image(model)
    
    def add_image(self, image_model: ImageModel):
        """Add a single image to the view - to be overridden"""
        pass
        
    def update_image(self, path: str, processed_image):
        """Update an image with processed version"""
        if path in self.thumbnails:
            self.thumbnails[path].update_with_processed_image(processed_image)
            
    def clear(self):
        """Clear all images"""
        for thumbnail in self.thumbnails.values():
            thumbnail.deleteLater()
        self.thumbnails.clear()

class ListView(BaseGalleryView):
    """List view for displaying images vertically"""
    
    def _setup_ui(self):
        """Setup list view UI"""
        self.layout = QVBoxLayout()
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.container_widget = QWidget()
        self.container_layout = QVBoxLayout(self.container_widget)
        self.container_layout.setSpacing(8)
        self.container_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.container_widget)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
        self.scroll_area.setStyleSheet(self._macos_scrollbar_style())
        
    def add_image(self, image_model: str | ImageModel):
        """Add image to list view"""
        if isinstance(image_model, str):
            image_model = ImageModel(image_model)
        thumbnail = ImageThumbnail(image_model)
        self.container_layout.addWidget(thumbnail)
        self.thumbnails[image_model.path] = thumbnail

class GridView(BaseGalleryView):
    """Grid view for displaying images in a grid"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.row = 0
        self.col = 0
        self.columns = 3
        
    def _setup_ui(self):
        """Setup grid view UI"""
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.container_widget = QWidget()
        self.grid_layout = QGridLayout(self.container_widget)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setAlignment(Qt.AlignTop)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.container_widget)
        
        self.layout.addWidget(self.scroll_area)
        self.setLayout(self.layout)
        self.scroll_area.setStyleSheet(self._macos_scrollbar_style())
        
    def add_image(self, image_model: str | ImageModel):
        """Add image to grid view"""
        if isinstance(image_model, str):
            image_model = ImageModel(image_model)
        thumbnail = ImageThumbnail(image_model)
        self.grid_layout.addWidget(thumbnail, self.row, self.col)
        self.thumbnails[image_model.path] = thumbnail
        
        # Update row and column
        self.col += 1
        if self.col >= self.columns:
            self.col = 0
            self.row += 1
            
    def clear(self):
        """Clear all images and reset grid position"""
        super().clear()
        self.row = 0
        self.col = 0