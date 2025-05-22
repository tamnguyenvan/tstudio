from dataclasses import dataclass
from typing import Optional
from PySide6.QtGui import QImage
import uuid
import os

@dataclass
class ImageModel:
    """Model representing an image with its metadata"""
    path: str
    filename: str
    id: str
    processed_image: Optional[QImage] = None
    is_processed: bool = False
    
    def __init__(self, path: str):
        self.path = path
        self.filename = os.path.basename(path)
        self.id = str(uuid.uuid4())
        self.processed_image = None
        self.is_processed = False
    
    def set_processed_image(self, image: QImage):
        """Set the processed image and mark as processed"""
        self.processed_image = image
        self.is_processed = True
    
    def get_save_filename(self) -> str:
        """Get the filename for saving processed image"""
        name, _ = os.path.splitext(self.filename)
        return f"{name}_nobg.png"