from PySide6.QtWidgets import (QFrame, QWidget, QHBoxLayout, QLabel, 
                             QPushButton, QToolButton, QStyle)
from PySide6.QtCore import Qt, Signal, QPoint, QTimer, QSize
from PySide6.QtGui import (QPainter, QColor, QIcon, QBrush, QPen,
                          QMouseEvent, QPaintEvent, QEnterEvent)

from utils.platform_utils import RESOURCES_PATH

class TrafficLightButton(QPushButton):
    """Traffic light button (close, minimize, maximize) with macOS styling"""
    
    def __init__(self, button_type, parent=None):
        super().__init__(parent)
        self.button_type = button_type  # 'close', 'minimize', 'maximize'
        self.is_hovered = False
        self.is_pressed = False
        
        # Button properties
        self.setFixedSize(12, 12)
        self.setFocusPolicy(Qt.NoFocus)
        
        # Colors for different states
        self.colors = {
            'close': {
                'normal': QColor(252, 98, 93),
                'hover': QColor(252, 98, 93),
                'pressed': QColor(200, 78, 73)
            },
            'minimize': {
                'normal': QColor(253, 184, 46),
                'hover': QColor(253, 184, 46),
                'pressed': QColor(200, 147, 36)
            },
            'maximize': {
                'normal': QColor(52, 199, 89),
                'hover': QColor(52, 199, 89),
                'pressed': QColor(42, 159, 69)
            }
        }
        
        # Symbol colors
        self.symbol_color = QColor(120, 0, 0, 150)
        
    def enterEvent(self, event: QEnterEvent):
        self.is_hovered = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.is_hovered = False
        self.is_pressed = False
        self.update()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_pressed = True
            self.update()
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.is_pressed = False
        self.update()
        super().mouseReleaseEvent(event)
    
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get button color based on state
        if self.is_pressed:
            color = self.colors[self.button_type]['pressed']
        elif self.is_hovered:
            color = self.colors[self.button_type]['hover']
        else:
            color = self.colors[self.button_type]['normal']
        
        # Draw circle
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(color.darker(110), 0.5))
        painter.drawEllipse(0, 0, 12, 12)
        
        # Draw symbol when hovered
        if self.is_hovered:
            painter.setPen(QPen(self.symbol_color, 1.2))
            center_x, center_y = 6, 6
            
            if self.button_type == 'close':
                # Draw X
                painter.drawLine(center_x - 3, center_y - 3, center_x + 3, center_y + 3)
                painter.drawLine(center_x + 3, center_y - 3, center_x - 3, center_y + 3)
            elif self.button_type == 'minimize':
                # Draw minus
                painter.drawLine(center_x - 3, center_y, center_x + 3, center_y)
            elif self.button_type == 'maximize':
                # Draw arrows or plus
                painter.drawLine(center_x - 2, center_y - 2, center_x + 2, center_y + 2)
                painter.drawLine(center_x + 2, center_y - 2, center_x - 2, center_y + 2)
                painter.drawLine(center_x - 2, center_y, center_x + 2, center_y)
                painter.drawLine(center_x, center_y - 2, center_x, center_y + 2)


class MacOSTitleBar(QFrame):
    """Custom macOS-style title bar with traffic lights and export button"""
    
    # Signals
    closeClicked = Signal()
    minimizeClicked = Signal()
    maximizeClicked = Signal()
    exportClicked = Signal()
    doubleClicked = Signal()
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("customTitleBar")
        self.title = title
        self.parent_window = parent
        
        # Mouse tracking for window dragging
        self.dragging = False
        self.drag_start_position = QPoint()
        
        # Setup UI
        self.setFixedHeight(40)
        self.setMouseTracking(True)
        self._setup_ui()
        
        # Double click timer
        self.double_click_timer = QTimer()
        self.double_click_timer.setSingleShot(True)
        self.double_click_timer.timeout.connect(self._single_click_action)
        self.click_count = 0
    
    def _setup_ui(self):
        """Setup the UI components with improved centering"""
        # Main layout với căn chỉnh theo trục Y
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(16, 0, 16, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignVCenter)  # Căn giữa theo trục Y
        
        # Left side - Traffic lights với fixed width để đảm bảo symmetry
        self.traffic_lights_container = QWidget()
        self.traffic_lights_container.setFixedWidth(120)  # Fixed width cho symmetry
        self.traffic_lights_layout = QHBoxLayout(self.traffic_lights_container)
        self.traffic_lights_layout.setContentsMargins(0, 0, 0, 0)
        self.traffic_lights_layout.setSpacing(8)
        self.traffic_lights_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # Create traffic light buttons
        self.close_button = TrafficLightButton('close')
        self.minimize_button = TrafficLightButton('minimize')
        self.maximize_button = TrafficLightButton('maximize')
        
        # Connect signals
        self.close_button.clicked.connect(self.closeClicked.emit)
        self.minimize_button.clicked.connect(self.minimizeClicked.emit)
        self.maximize_button.clicked.connect(self.maximizeClicked.emit)
        
        self.traffic_lights_layout.addWidget(self.close_button)
        self.traffic_lights_layout.addWidget(self.minimize_button)
        self.traffic_lights_layout.addWidget(self.maximize_button)
        self.traffic_lights_layout.addStretch()
        
        # Center - Title với absolute centering
        self.title_container = QWidget()
        self.title_layout = QHBoxLayout(self.title_container)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setAlignment(Qt.AlignCenter)
        
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("titlebarLabel")  # Sửa object name để match với CSS
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.title_layout.addWidget(self.title_label)
        
        # Right side - Export button với fixed width để match left side
        self.export_container = QWidget()
        self.export_container.setFixedWidth(120)  # Same width as traffic lights
        self.export_layout = QHBoxLayout(self.export_container)
        self.export_layout.setContentsMargins(0, 0, 0, 0)
        self.export_layout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.export_button = QToolButton()
        self.export_button.setObjectName("exportButton")
        self.export_button.setToolTip("Export")
        self.export_button.setIcon(QIcon(str(RESOURCES_PATH / "icons/save.svg")))
        self.export_button.setIconSize(QSize(24, 24))
        self.export_button.setCursor(Qt.PointingHandCursor)
        self.export_button.setFixedSize(40, 32)
        self.export_button.clicked.connect(self.exportClicked.emit)
        
        self.export_layout.addWidget(self.export_button)
        
        # Add to main layout - đảm bảo title luôn ở giữa
        self.layout.addWidget(self.traffic_lights_container)
        self.layout.addWidget(self.title_container, 1)  # Stretch factor = 1
        self.layout.addWidget(self.export_container)
        
        self.setLayout(self.layout)
    
    def set_title(self, title: str):
        """Set the title text"""
        self.title = title
        self.title_label.setText(title)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for dragging"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.globalPosition().toPoint()
            
            # Handle double click
            self.click_count += 1
            if self.click_count == 1:
                self.double_click_timer.start(300)  # 300ms for double click
            elif self.click_count == 2:
                self.double_click_timer.stop()
                self.click_count = 0
                self.doubleClicked.emit()
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move for window dragging"""
        if self.dragging and self.parent_window:
            # Calculate new position
            delta = event.globalPosition().toPoint() - self.drag_start_position
            new_pos = self.parent_window.pos() + delta
            
            # Move window
            self.parent_window.move(new_pos)
            self.drag_start_position = event.globalPosition().toPoint()
        
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
        
        super().mouseReleaseEvent(event)
    
    def _single_click_action(self):
        """Handle single click action"""
        self.click_count = 0
        # Add any single click behavior here if needed
    
    def set_window_state(self, is_maximized: bool):
        """Update the maximize button based on window state"""
        # You can change the maximize button appearance based on window state
        pass