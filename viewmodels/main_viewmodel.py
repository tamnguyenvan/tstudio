from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog
from typing import List, Dict
import os
from models import ImageModel, BackgroundRemovalModel

class MainViewModel(QObject):
    """ViewModel for the main application logic"""
    
    # Signals
    images_added = Signal(list)  # List of ImageModel
    images_cleared = Signal()
    processing_started = Signal()
    processing_finished = Signal()
    progress_updated = Signal(int)
    image_processed = Signal(str, object)  # path, QImage
    error_occurred = Signal(str, str)  # path, error message
    ui_state_changed = Signal(dict)  # UI state dictionary
    
    def __init__(self):
        super().__init__()
        self.image_models: Dict[str, ImageModel] = {}
        self.bg_removal_model = BackgroundRemovalModel()
        
    def add_images_from_paths(self, paths: List[str]):
        """Add images from file paths"""
        new_models = []
        for path in paths:
            if path not in self.image_models and self._is_valid_image(path):
                model = ImageModel(path)
                self.image_models[path] = model
                new_models.append(model)
        
        if new_models:
            self.images_added.emit(new_models)
            self._update_ui_state()
    
    def select_images_dialog(self, parent=None):
        """Open file dialog to select images"""
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(
            parent, "Select Images", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        
        if file_paths:
            self.add_images_from_paths(file_paths)
    
    def process_images(self):
        """Start processing all images"""
        if not self.image_models:
            return
        
        self.processing_started.emit()
        
        # Create worker and connect signals
        worker = self.bg_removal_model.process_images(list(self.image_models.values()))
        worker.progress.connect(self.progress_updated.emit)
        worker.image_processed.connect(self._on_image_processed)
        worker.all_finished.connect(self._on_processing_finished)
        worker.error_occurred.connect(self.error_occurred.emit)
        worker.start()
    
    def clear_images(self):
        """Clear all images"""
        self.bg_removal_model.stop_processing()
        self.image_models.clear()
        self.images_cleared.emit()
        self._update_ui_state()
    
    def save_images(self, parent=None):
        """Save all processed images"""
        processed_models = [model for model in self.image_models.values() if model.is_processed]
        
        if not processed_models:
            return False
        
        save_dir = QFileDialog.getExistingDirectory(
            parent, "Select Save Directory", "", QFileDialog.ShowDirsOnly
        )
        
        if not save_dir:
            return False
        
        for model in processed_models:
            save_path = os.path.join(save_dir, model.get_save_filename())
            model.processed_image.save(save_path, "PNG")
        
        return True
    
    def get_image_count(self) -> int:
        """Get total number of images"""
        return len(self.image_models)
    
    def get_processed_count(self) -> int:
        """Get number of processed images"""
        return sum(1 for model in self.image_models.values() if model.is_processed)
    
    def _on_image_processed(self, path: str, processed_image):
        """Handle when an image is processed"""
        if path in self.image_models:
            self.image_models[path].set_processed_image(processed_image)
            self.image_processed.emit(path, processed_image)
    
    def _on_processing_finished(self):
        """Handle when all processing is finished"""
        self.processing_finished.emit()
        self._update_ui_state()
    
    def _update_ui_state(self):
        """Update UI state based on current data"""
        has_images = len(self.image_models) > 0
        has_processed = self.get_processed_count() > 0
        
        state = {
            'has_images': has_images,
            'has_processed': has_processed,
            'image_count': len(self.image_models),
            'processed_count': self.get_processed_count()
        }
        
        self.ui_state_changed.emit(state)
    
    def _is_valid_image(self, path: str) -> bool:
        """Check if file is a valid image"""
        return path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp'))
