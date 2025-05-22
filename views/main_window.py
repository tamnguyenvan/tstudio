import os

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QSplitter, QApplication, QFileDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette

from .sidebar import Sidebar
from .gallery_views import ListView
from .components.gallery_header import GalleryHeader
from .components.mac_vibrancy_widget import MacVibrancyWidget
from .components.custom_titlebar import MacOSTitleBar
from models import BackgroundRemovalWorker
from utils.platform_utils import IS_MACOS, HAS_NSVIEW
from resources.styles import STYLESHEET

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Batch Image Background Remover")
        self.setMinimumSize(1000, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Initialize UI
        self._init_ui()

        # Initialize state
        self.image_paths = []
        self.processed_images = {}
        self.worker_thread = None 
        self.is_maximized = False
        
        # Connect signals
        self._connect_signals()
        
        # Apply theme
        self._apply_theme()

        self.move(460, 240)
    
    def _init_ui(self):
        """Initialize the UI components"""
        # Create central widget
        self.central_widget = QWidget()
        self.central_widget.setObjectName("mainWidget")
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Content layout
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Apply vibrancy effect for macOS
        if HAS_NSVIEW:
            self.vibrancy_effect = MacVibrancyWidget(self)
            self.content_layout.addWidget(self.vibrancy_effect)
            
            # Container for main content
            self.content_widget = QWidget(self.vibrancy_effect)
            self.inner_content_layout = QHBoxLayout(self.content_widget)
            self.inner_content_layout.setContentsMargins(0, 0, 0, 0)
            self.content_widget.setLayout(self.inner_content_layout)
        else:
            # For non-macOS systems
            self.inner_content_layout = self.content_layout
        
        # Create splitter for sidebar and main area
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setHandleWidth(1)  # Make the splitter handle visible but thin
        self.inner_content_layout.addWidget(self.splitter)
        
        # Create sidebar
        self.sidebar = Sidebar()
        
        # Create main content area
        self.main_content = QWidget()
        self.main_content.setObjectName("mainContent")
        self.main_content_layout = QVBoxLayout(self.main_content)
        self.main_content_layout.setContentsMargins(40, 40, 40, 40)
        self.main_content_layout.setSpacing(30)
        
        # Gallery header
        self.gallery_header = GalleryHeader()
        self.main_content_layout.addWidget(self.gallery_header)
        
        # Create list view
        self.list_view = ListView()
        self.main_content_layout.addWidget(self.list_view)
        
        # Add widgets to splitter
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.main_content)
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        
        # Set splitter proportions - 40% sidebar, 60% main content
        total_width = self.width()
        self.splitter.setSizes([int(total_width * 0.43), int(total_width * 0.57)])
        
        # Add title bar
        self.title_bar = MacOSTitleBar("TStudio", self)
        self.main_layout.addWidget(self.title_bar)

        self.main_layout.addLayout(self.content_layout)
        
        # Window flags for macOS style window
        if IS_MACOS:
            self.setAttribute(Qt.WA_TranslucentBackground)
    
    def _connect_signals(self):
        """Connect signals between components"""
        # Connect sidebar signals
        self.sidebar.images_dropped.connect(self.add_images)
        self.sidebar.process_clicked.connect(self.process_images)
        self.sidebar.clear_clicked.connect(self.clear_images)

        # Connect title bar signals
        self.title_bar.closeClicked.connect(self.close)
        self.title_bar.minimizeClicked.connect(self.showMinimized)
        self.title_bar.maximizeClicked.connect(self.toggle_maximize)
        self.title_bar.doubleClicked.connect(self.toggle_maximize)
        self.title_bar.saveClicked.connect(self.save_images)
    
    def _apply_theme(self):
        """Apply theme based on system settings"""
        palette = QApplication.palette()
        background_color = palette.color(QPalette.Window)
        brightness = (background_color.red() * 299 + 
                     background_color.green() * 587 + 
                     background_color.blue() * 114) / 1000
        
        is_dark = brightness < 128
        
        if is_dark:
            self.setStyleSheet(STYLESHEET)
            self.central_widget.setProperty("class", "dark")
            if HAS_NSVIEW:
                self.vibrancy_effect.set_dark_mode(True)
        else:
            self.setStyleSheet(STYLESHEET)
            self.central_widget.setProperty("class", "")
            if HAS_NSVIEW:
                self.vibrancy_effect.set_dark_mode(False)
        
        # Force style update
        self.central_widget.style().unpolish(self.central_widget)
        self.central_widget.style().polish(self.central_widget)
        self.central_widget.update()
    
    def add_images(self, paths):
        for path in paths:
            if path not in self.image_paths:
                self.image_paths.append(path)
                self.list_view.add_image(path)
                
        self.sidebar.process_button.setEnabled(len(self.image_paths) > 0)
        self.sidebar.clear_button.setVisible(len(self.image_paths) > 0)
        self.sidebar.clear_button.setEnabled(len(self.image_paths) > 0)
        
        # Update gallery title
        count = len(self.image_paths)
        self.gallery_header.set_title(f"Image Gallery ({count} {'image' if count == 1 else 'images'})")
        
    def process_images(self):
        if not self.image_paths:
            return
            
        # Disable UI during processing
        self.sidebar.process_button.setEnabled(False)
        self.sidebar.progress_bar.setValue(0)
        self.sidebar.progress_bar.setVisible(True)
        
        # Create and start worker thread
        self.worker_thread = BackgroundRemovalWorker(self.image_paths)
        self.worker_thread.progress.connect(self.update_progress)
        self.worker_thread.image_processed.connect(self.update_image)
        self.worker_thread.all_finished.connect(self.processing_finished)
        self.worker_thread.start()
        
    def update_progress(self, value):
        self.sidebar.progress_bar.setValue(value)
        
    def update_image(self, image_path, processed_image):
        self.processed_images[image_path] = processed_image
        self.list_view.update_image(image_path, processed_image)
        
    def processing_finished(self):
        self.sidebar.progress_bar.setVisible(False)
        self.sidebar.process_button.setEnabled(True)
        self.title_bar.save_button.setVisible(len(self.processed_images) > 0)
        self.title_bar.save_button.setEnabled(len(self.processed_images) > 0)
        
    def clear_images(self):
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.worker_thread.wait()
            
        self.image_paths.clear()
        self.processed_images.clear()
        self.list_view.clear()
        
        self.sidebar.process_button.setEnabled(False)
        self.sidebar.clear_button.setVisible(False)
        self.title_bar.save_button.setVisible(False)
        self.sidebar.clear_button.setEnabled(False)
        self.sidebar.progress_bar.setVisible(False)
        
        # Reset gallery title
        self.gallery_header.set_title("Image Gallery")
        
    def save_images(self):
        if not self.processed_images:
            return
            
        save_dir = QFileDialog.getExistingDirectory(
            self, "Select Save Directory", "", QFileDialog.ShowDirsOnly
        )
        
        if not save_dir:
            return
            
        for image_path, processed_image in self.processed_images.items():
            filename = os.path.basename(image_path)
            name, _ = os.path.splitext(filename)
            save_path = os.path.join(save_dir, f"{name}_nobg.png")
            
            # Save the image
            processed_image.save(save_path, "PNG")
        
    def closeEvent(self, event):
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.worker_thread.wait()
        event.accept()
        
    def resizeEvent(self, event):
        """Handle resize event to maintain the 40/60 split"""
        super().resizeEvent(event)
        total_width = self.splitter.width()
        self.splitter.setSizes([int(total_width * 0.4), int(total_width * 0.6)])

    def toggle_maximize(self):
        """Toggle between maximized and normal window state"""
        if self.is_maximized:
            self.showNormal()
            self.is_maximized = False
        else:
            self.showMaximized()
            self.is_maximized = True
        
        self.title_bar.set_window_state(self.is_maximized)
    