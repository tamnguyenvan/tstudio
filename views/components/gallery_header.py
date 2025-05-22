from PySide6.QtWidgets import (QWidget, QHBoxLayout, QLabel, QToolButton, 
                              QButtonGroup)
from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon
from utils.platform_utils import RESOURCES_PATH

class GalleryHeader(QWidget):
    """Header widget for the gallery with view mode controls"""
    view_mode_changed = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("galleryHeader")
        self.setFixedHeight(50)
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the UI components"""
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Gallery title
        self.title_label = QLabel("Image Gallery")
        self.title_label.setObjectName("galleryTitle")
        self.layout.addWidget(self.title_label)
        
        # Spacer
        self.layout.addStretch()
        
        # View mode buttons
        self._setup_view_buttons()
        
        self.setLayout(self.layout)
    
    def _setup_view_buttons(self):
        """Setup view mode toggle buttons"""
        self.view_buttons_layout = QHBoxLayout()
        self.view_buttons_layout.setSpacing(5)
        
        self.list_view_button = QToolButton()
        self.list_view_button.setCheckable(True)
        self.list_view_button.setToolTip("List View")
        self.list_view_button.setIcon(QIcon(str(RESOURCES_PATH / "icons/list.svg")))
        self.list_view_button.setIconSize(QSize(16, 16))
        
        self.grid_view_button = QToolButton()
        self.grid_view_button.setCheckable(True)
        self.grid_view_button.setChecked(True)
        self.grid_view_button.setToolTip("Grid View")
        self.grid_view_button.setIcon(QIcon(str(RESOURCES_PATH / "icons/grid.svg")))
        self.grid_view_button.setIconSize(QSize(16, 16))
        
        # Button group for exclusive selection
        self.view_button_group = QButtonGroup()
        self.view_button_group.addButton(self.list_view_button, 0)
        self.view_button_group.addButton(self.grid_view_button, 1)
        self.view_button_group.buttonClicked.connect(self._on_view_mode_changed)
        
        self.view_buttons_layout.addWidget(self.list_view_button)
        self.view_buttons_layout.addWidget(self.grid_view_button)
        
        self.layout.addLayout(self.view_buttons_layout)
        
    def _on_view_mode_changed(self, button):
        """Handle view mode change"""
        if button == self.list_view_button:
            self.view_mode_changed.emit(0)
        else:
            self.view_mode_changed.emit(1)
    
    def set_title(self, title: str):
        """Set the gallery title"""
        self.title_label.setText(title)