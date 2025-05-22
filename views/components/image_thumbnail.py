from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor
from models import ImageModel

class ImageThumbnail(QFrame):
    """Thumbnail widget for displaying images with chess board background"""
    
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
        
        # Image label with chess board background
        self.image_label = ChessBoardLabel()
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


class ChessBoardLabel(QLabel):
    """QLabel with chess board background pattern"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.square_size = 10  # square size of chess board
        
    def paintEvent(self, event):
        """Override paint event to draw chess board background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw chess board background
        self._draw_chess_board(painter)
        
        # Call paintEvent of QLabel to draw pixmap
        super().paintEvent(event)
    
    def _draw_chess_board(self, painter):
        """Draw chess board pattern"""
        width = self.width()
        height = self.height()
        
        # Colors for chess board
        light_color = QColor(255, 255, 255, 100)  # White transparent
        dark_color = QColor(128, 128, 128, 100)   # Gray transparent
        
        # Draw each square
        for row in range(0, height, self.square_size):
            for col in range(0, width, self.square_size):
                # Determine color based on position (chess board pattern)
                is_light = (row // self.square_size + col // self.square_size) % 2 == 0
                color = light_color if is_light else dark_color
                
                # Draw square
                painter.fillRect(col, row, self.square_size, self.square_size, color)
    
    def set_square_size(self, size):
        """Set the size of chess board squares"""
        self.square_size = size
        self.update()  # Trigger repaint