import os
import sys
import platform
from pathlib import Path
from typing import Dict, List, Optional

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                              QSplitter, QStackedWidget, QApplication, QFileDialog)
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QIcon, QPalette, QFont

from .sidebar import Sidebar
from .gallery_views import ListView, GridView
from .components.gallery_header import GalleryHeader
from models import BackgroundRemovalWorker
from utils.platform_utils import IS_MACOS, IS_WINDOWS, IS_LINUX, HAS_NSVIEW
from resources.styles import STYLESHEET

class MacVibrancyWidget(QMacCocoaViewContainer if HAS_NSVIEW else QWidget):
    """MacOS specific vibrancy effect widget"""
    
    def __init__(self, parent=None):
        super().__init__(0, parent)
        
        if HAS_NSVIEW:
            # Create NSVisualEffectView
            self.effect_view = NSVisualEffectView.alloc().initWithFrame_((0, 0), (100, 100))
            self.effect_view.setMaterial_(NSVisualEffectMaterial.underWindowBackground)
            self.effect_view.setBlendingMode_(NSVisualEffectBlendingMode.behindWindow)
            self.effect_view.setState_(1)  # Active state
            self.effect_view.setAutoresizingMask_(18)  # width + height
            
            # Set the NSView
            self.setCocoaView(self.effect_view)
        else:
            # Fallback for non-macOS systems
            self.setStyleSheet("background-color: rgba(240, 240, 240, 230);")
    
    def set_dark_mode(self, is_dark):
        """Toggle dark/light mode for macOS"""
        if HAS_NSVIEW:
            appearance = NSAppearance.appearanceNamed_("NSAppearanceNameDarkAqua" if is_dark 
                                                     else "NSAppearanceNameAqua")
            self.effect_view.setAppearance_(appearance)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Batch Image Background Remover")
        self.setMinimumSize(1000, 700)
        
        # Initialize UI
        self._init_ui()

        # Initialize state
        self.image_paths = []
        self.processed_images = {}
        self.worker_thread = None 
        
        # Connect signals
        self._connect_signals()
        
        # Apply theme
        self._apply_theme()
    
    def _init_ui(self):
        """Initialize the UI components"""
        # Create central widget
        self.central_widget = QWidget()
        self.central_widget.setObjectName("mainWidget")
        self.setCentralWidget(self.central_widget)
        
        # Main layout
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Apply vibrancy effect for macOS
        if HAS_NSVIEW:
            self.vibrancy_effect = MacVibrancyWidget(self)
            self.vibrancy_effect.setContentsMargins(0, 0, 0, 0)
            self.main_layout.addWidget(self.vibrancy_effect)
            
            # Container for main content
            self.content_widget = QWidget(self.vibrancy_effect)
            self.content_layout = QHBoxLayout(self.content_widget)
            self.content_layout.setContentsMargins(15, 15, 15, 15)
            self.content_widget.setLayout(self.content_layout)
        else:
            # For non-macOS systems
            self.content_layout = self.main_layout
            self.content_layout.setContentsMargins(15, 15, 15, 15)
        
        # Create splitter for sidebar and main area
        self.splitter = QSplitter(Qt.Horizontal)
        self.content_layout.addWidget(self.splitter)
        
        # Create sidebar
        self.sidebar = Sidebar()
        
        # Create main content area
        self.main_content = QWidget()
        self.main_content_layout = QVBoxLayout(self.main_content)
        self.main_content_layout.setContentsMargins(0, 0, 0, 0)
        self.main_content_layout.setSpacing(0)
        
        # Gallery header with view mode controls
        self.gallery_header = GalleryHeader()
        self.main_content_layout.addWidget(self.gallery_header)
        
        # Create stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.list_view = ListView()
        self.grid_view = GridView()
        
        self.stacked_widget.addWidget(self.list_view)
        self.stacked_widget.addWidget(self.grid_view)
        self.stacked_widget.setCurrentIndex(1)  # Default to grid view
        
        self.main_content_layout.addWidget(self.stacked_widget)
        
        # Add widgets to splitter
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.main_content)
        self.splitter.setCollapsible(0, False)
        self.splitter.setCollapsible(1, False)
        
        # Set splitter proportions
        self.splitter.setSizes([300, 700])
        
        # Window flags for macOS style window
        if IS_MACOS:
            self.setAttribute(Qt.WA_TranslucentBackground)
            # Get statusbar height and menu bar height
            frame_geo = self.frameGeometry()
            content_geo = self.geometry()
            title_bar_height = frame_geo.height() - content_geo.height()
            self.content_layout.setContentsMargins(15, 15 + title_bar_height, 15, 15)
    
    def _connect_signals(self):
        """Connect signals between components"""
        # Connect sidebar signals
        self.sidebar.images_dropped.connect(self.add_images)
        self.sidebar.process_clicked.connect(self.process_images)
        self.sidebar.clear_clicked.connect(self.clear_images)
        self.sidebar.save_clicked.connect(self.save_images)
        
        # Connect gallery header signals
        self.gallery_header.view_mode_changed.connect(self.change_view_mode)
    
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
                self.grid_view.add_image(path)
                self.list_view.add_image(path)
                
        self.sidebar.process_button.setEnabled(len(self.image_paths) > 0)
        self.sidebar.clear_button.setEnabled(len(self.image_paths) > 0)
        
        # Update gallery title
        count = len(self.image_paths)
        self.gallery_header.title_label.setText(f"Image Gallery ({count} {'image' if count == 1 else 'images'})")
        
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
        self.grid_view.update_image(image_path, processed_image)
        self.list_view.update_image(image_path, processed_image)
        
    def processing_finished(self):
        self.sidebar.progress_bar.setVisible(False)
        self.sidebar.process_button.setEnabled(True)
        self.sidebar.save_button.setEnabled(len(self.processed_images) > 0)
        
    def clear_images(self):
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.worker_thread.wait()
            
        self.image_paths.clear()
        self.processed_images.clear()
        self.grid_view.clear()
        self.list_view.clear()
        
        self.sidebar.process_button.setEnabled(False)
        self.sidebar.clear_button.setEnabled(False)
        self.sidebar.save_button.setEnabled(False)
        self.sidebar.progress_bar.setVisible(False)
        
        # Reset gallery title
        self.gallery_header.title_label.setText("Image Gallery")
        
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
            
    def change_view_mode(self, mode):
        self.stacked_widget.setCurrentIndex(mode)
        
    def closeEvent(self, event):
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            self.worker_thread.wait()
        event.accept()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for consistent look across platforms
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())