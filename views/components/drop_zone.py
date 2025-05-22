from PySide6.QtWidgets import QLabel, QFileDialog, QVBoxLayout, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QPixmap
from utils.platform_utils import RESOURCES_PATH

class ImageDropZone(QFrame):
    """Drag and drop zone for images"""
    image_dropped = Signal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dropZoneWidget")
        self.setAcceptDrops(True)
        self.setMinimumHeight(200)
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI components"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setAlignment(Qt.AlignCenter)
        
        # Cloud icon
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        # Create a cloud icon with download arrow
        cloud_pixmap = QPixmap(32, 32)
        cloud_pixmap.fill(Qt.transparent)
        # In a real app, you'd load an actual SVG icon
        self.icon_label.setPixmap(QPixmap(str(RESOURCES_PATH / "icons/cloud-upload.svg")))
        
        # Text label
        self.text_label = QLabel("Drag and drop images\nhere or click to select files")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setWordWrap(True)
        
        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.text_label)
        
    def mousePressEvent(self, event):
        """Handle mouse click to open file dialog"""
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.webp)")
        
        if file_dialog.exec():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                self.image_dropped.emit(file_paths)
            
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                ImageDropZone {
                    background-color: rgba(13, 110, 253, 0.1);
                    border: 2px dashed #0d6efd;
                    border-radius: 10px;
                }
                
                QLabel {
                    background-color: transparent;
                    color: #0d6efd;
                    font-size: 14px;
                }
            """)
            
    def dragLeaveEvent(self, event):
        """Handle drag leave event"""
        event.accept()
        self.setStyleSheet("""
            ImageDropZone {
                background-color: white;
                border: 2px dashed #ddd;
                border-radius: 10px;
            }
            
            QLabel {
                background-color: transparent;
                color: #666;
                font-size: 14px;
            }
        """)
            
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        file_paths = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                file_paths.append(file_path)
                
        if file_paths:
            self.image_dropped.emit(file_paths)
            
        self.setStyleSheet("""
            ImageDropZone {
                background-color: white;
                border: 2px dashed #ddd;
                border-radius: 10px;
            }
            
            QLabel {
                background-color: transparent;
                color: #666;
                font-size: 14px;
            }
        """)
        event.acceptProposedAction()