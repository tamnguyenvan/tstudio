from PySide6.QtWidgets import QLabel, QFileDialog
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent

class ImageDropZone(QLabel):
    """Drag and drop zone for images"""
    image_dropped = Signal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dropZoneLabel")
        self.setText("Drag and drop images here\nor click to select files")
        self.setAlignment(Qt.AlignCenter)
        self.setAcceptDrops(True)
        self.setMinimumHeight(160)
        
    def mousePressEvent(self, event):
        """Handle mouse click to open file dialog"""
        self.image_dropped.emit([])  # Empty list signals to open dialog
            
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet(
                "QLabel#dropZoneLabel { "
                "background-color: rgba(13, 110, 253, 50); "
                "border: 2px dashed #0d6efd; "
                "color: #0d6efd; }"
            )
            
    def dragLeaveEvent(self, event):
        """Handle drag leave event"""
        event.accept()
        self.setStyleSheet("")
            
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        file_paths = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                file_paths.append(file_path)
                
        if file_paths:
            self.image_dropped.emit(file_paths)
            
        self.setStyleSheet("")
        event.acceptProposedAction()