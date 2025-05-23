from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                              QProgressBar)
from PySide6.QtCore import Signal
from .components import ImageDropZone

class Sidebar(QWidget):
    """Sidebar widget containing controls and drop zone"""
    
    # Signals
    images_dropped = Signal(list)
    process_clicked = Signal()
    clear_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebarWidget")
        self.setMinimumWidth(320)
        self.setMaximumWidth(430)
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        """Setup sidebar UI"""
        # Sidebar layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 0)
        self.layout.setSpacing(30)
        
        # App title
        self.title_label = QLabel("Background Remover")
        self.title_label.setObjectName("titleLabel")
        self.layout.addWidget(self.title_label)
        
        # Drop zone
        self.drop_zone = ImageDropZone()
        self.layout.addWidget(self.drop_zone)
        
        # Process button
        self.process_button = QPushButton("Remove Background")
        self.process_button.setEnabled(False)
        self.layout.addWidget(self.process_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)
        
        # Bottom buttons
        self._setup_bottom_buttons()
        
        # Spacer
        self.layout.addStretch()
        
    def _setup_bottom_buttons(self):
        """Setup bottom control buttons"""
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.setSpacing(30)
        
        # Create clear button with fixed height
        self.clear_button = QPushButton("Clear All")
        self.clear_button.setObjectName("clearButton")
        self.clear_button.setEnabled(False)
        self.clear_button.setFixedHeight(52)  # Match other buttons
        self.clear_button.setVisible(False)  # Initially hidden
        
        self.bottom_layout.addWidget(self.clear_button)

        # Add bottom buttons to sidebar
        self.layout.addLayout(self.bottom_layout)
        
    def _connect_signals(self):
        """Connect internal signals"""
        self.drop_zone.image_dropped.connect(self.images_dropped.emit)
        self.process_button.clicked.connect(self.process_clicked.emit)
        self.clear_button.clicked.connect(self.clear_clicked.emit)
    
    # def update_ui_state(self, state: dict):
    #     """Update UI state based on viewmodel state"""
    #     has_images = state.get('has_images', False)
        
    #     self.process_button.setEnabled(has_images)
    #     self.clear_button.setEnabled(has_images)
    #     self.clear_button.setVisible(has_images)
    
    def set_progress(self, value: int):
        """Set progress bar value"""
        self.progress_bar.setValue(value)
    
    def show_progress(self, show: bool):
        """Show or hide progress bar"""
        self.progress_bar.setVisible(show)
    
    def set_processing_state(self, is_processing: bool):
        """Update UI for processing state"""
        self.process_button.setEnabled(not is_processing)
        self.show_progress(is_processing)
        if is_processing:
            self.set_progress(0)