from PySide6.QtCore import QObject, Signal
from typing import List
from models import ImageModel

class GalleryViewModel(QObject):
    """ViewModel for gallery display logic"""
    
    # Signals
    view_mode_changed = Signal(int)  # 0 = list, 1 = grid
    title_updated = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._view_mode = 1  # Default to grid view
        self._image_models: List[ImageModel] = []
    
    def set_view_mode(self, mode: int):
        """Set the view mode (0=list, 1=grid)"""
        if mode != self._view_mode:
            self._view_mode = mode
            self.view_mode_changed.emit(mode)
    
    def get_view_mode(self) -> int:
        """Get current view mode"""
        return self._view_mode
    
    def update_images(self, image_models: List[ImageModel]):
        """Update the list of image models"""
        self._image_models = image_models
        self._update_title()
    
    def clear_images(self):
        """Clear all images"""
        self._image_models.clear()
        self._update_title()
    
    def _update_title(self):
        """Update the gallery title based on image count"""
        count = len(self._image_models)
        if count == 0:
            title = "Image Gallery"
        else:
            title = f"Image Gallery ({count} {'image' if count == 1 else 'images'})"
        
        self.title_updated.emit(title)