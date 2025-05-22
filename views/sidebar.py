from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, 
                              QProgressBar, QHBoxLayout)
from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon
from .components import ImageDropZone
from utils.platform_utils import RESOURCES_PATH

class Sidebar(QWidget):
    """Sidebar widget containing controls and drop zone"""
    
    # Signals
    images_dropped = Signal(list)
    process_clicked = Signal()
    clear_clicked = Signal()
    save_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebarWidget")
        self.setMinimumWidth(280)
        self.setMaximumWidth(320)
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self):
        """Setup sidebar UI"""
        # Sidebar layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        # App title
        self.title_label = QLabel("Background Remover")
        self.title_label.setObjectName("titleLabel")
        self.layout.addWidget(self.title_label)
        
        # Drop zone
        self.drop_zone = ImageDropZone()
        self.layout.addWidget(self.drop_zone)
        
        # Process button
        self.process_button = QPushButton("Remove Background")
        self.process_button.setText("Remove Background")
        self.process_button.setStyleSheet("text-align: center; vertical-align: middle;")
        self.process_button.setEnabled(False)
        self.layout.addWidget(self.process_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)
        
        # Spacer
        self.layout.addStretch()
        
        # Bottom buttons
        self._setup_bottom_buttons()
        
    def _setup_bottom_buttons(self):
        """Setup bottom control buttons"""
        self.bottom_layout = QVBoxLayout()
        self.bottom_layout.setSpacing(10)
        
        self.clear_button = QPushButton("Clear All")
        # self.clear_button.setIcon(QIcon(str(RESOURCES_PATH / "icons/clear.svg")))
        # self.clear_button.setIconSize(QSize(16, 16))
        self.clear_button.setStyleSheet("text-align: center; vertical-align: middle;")
        self.clear_button.setObjectName("clearButton")
        self.clear_button.setEnabled(False)
        
        self.save_button = QPushButton("Save All")
        # self.save_button.setIcon(QIcon(str(RESOURCES_PATH / "icons/save.svg")))
        # self.save_button.setIconSize(QSize(16, 16))
        self.save_button.setStyleSheet("text-align: center; vertical-align: middle;")
        self.save_button.setObjectName("saveButton")
        self.save_button.setEnabled(False)
        
        self.bottom_layout.addWidget(self.clear_button)
        self.bottom_layout.addWidget(self.save_button)
        
        # Add bottom buttons to sidebar
        self.layout.addLayout(self.bottom_layout)
        
    def _connect_signals(self):
        """Connect internal signals"""
        self.drop_zone.image_dropped.connect(self.images_dropped.emit)
        self.process_button.clicked.connect(self.process_clicked.emit)
        self.clear_button.clicked.connect(self.clear_clicked.emit)
        self.save_button.clicked.connect(self.save_clicked.emit)
    
    def update_ui_state(self, state: dict):
        """Update UI state based on viewmodel state"""
        has_images = state.get('has_images', False)
        has_processed = state.get('has_processed', False)
        
        self.process_button.setEnabled(has_images)
        self.clear_button.setEnabled(has_images)
        self.save_button.setEnabled(has_processed)
    
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