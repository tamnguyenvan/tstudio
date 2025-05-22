import io

from PySide6.QtCore import QObject, Signal, QThread
from PySide6.QtGui import QImage
import rembg
from PIL import Image
from .image_model import ImageModel

class BackgroundRemovalWorker(QThread):
    """Worker thread for background removal processing"""
    progress = Signal(int)
    image_processed = Signal(str, QImage)  # image_path, processed_image
    all_finished = Signal()
    error_occurred = Signal(str, str)  # image_path, error_message
    
    def __init__(self, image_models: list[ImageModel] | list[str]):
        super().__init__()
        if isinstance(image_models, list) and isinstance(image_models[0], str):
            image_models = [ImageModel(path) for path in image_models]
        self.image_models = image_models
        self.running = True
        
    def run(self):
        total = len(self.image_models)
        for i, image_model in enumerate(self.image_models):
            if not self.running:
                break
                
            try:
                # Load image
                input_image = Image.open(image_model.path)
                
                # Remove background
                output = rembg.remove(input_image)
                
                # Convert to QImage
                byte_array = io.BytesIO()
                output.save(byte_array, format='PNG')
                byte_array = byte_array.getvalue()
                
                q_image = QImage.fromData(byte_array)
                
                # Emit signal with processed image
                self.image_processed.emit(image_model.path, q_image)
                
                # Update progress
                self.progress.emit(int((i + 1) / total * 100))
                
            except Exception as e:
                self.error_occurred.emit(image_model.path, str(e))
                
        self.all_finished.emit()
        
    def stop(self):
        self.running = False

# class BackgroundRemovalModel(QObject):
#     """Model for handling background removal operations"""
    
#     def __init__(self):
#         super().__init__()
#         self.worker = BackgroundRemovalWorker([])
    
#     def process_images(self, image_models: list[ImageModel] | list[str]) -> BackgroundRemovalWorker:
#         """Start processing images and return the worker thread"""
#         if isinstance(image_models, list) and isinstance(image_models[0], str):
#             image_models = [ImageModel(path) for path in image_models]
        
#         if self.worker and self.worker.isRunning():
#             self.worker.stop()
#             self.worker.wait()
        
#         self.worker = BackgroundRemovalWorker(image_models)
#         return self.worker
    
#     def stop_processing(self):
#         """Stop the current processing"""
#         if self.worker and self.worker.isRunning():
#             self.worker.stop()
#             self.worker.wait()