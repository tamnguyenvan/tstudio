STYLESHEET = """
/* Main Window Styles */
QMainWindow {
    background-color: transparent;
}

QWidget#mainWidget {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
}

/* Title Bar Styles */
QWidget#customTitleBar {
    background-color: transparent;
    border-bottom: 1px solid #e0e0e0;
}

QLabel#titlebarLabel {
    color: #333;
    font-size: 24px;
    font-weight: 500;
}

QToolButton#exportButton {
    border: none;
    background: transparent;
    border-radius: 4px;
}

/* Sidebar Styles */
QWidget#sidebarWidget {
    background-color: white;
    border-right: none; /* Removed border as we'll use the splitter handle */
}

/* Title Styles */
QLabel#titleLabel {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 34px;
    font-weight: 600;
    padding: 0px 0px;
    color: #333;
    qproperty-alignment: AlignLeft;
}

/* Gallery Title Styles */
QLabel#galleryTitle {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 34px;
    font-weight: 600;
    padding: 0px 0px;
    color: #333;
    qproperty-alignment: AlignLeft;
}

/* Button Styles - Bigger as requested */
QPushButton {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: #0d6efd;
    color: white;
    border-radius: 8px;
    padding: 14px 14px;
    font-weight: 500;
    font-size: 30px;
    text-align: center;
    border: none;
}

QPushButton:hover {
    background-color: #0b5ed7;
}

QPushButton:pressed {
    background-color: #0a58ca;
}

QPushButton:disabled {
    background-color: #6c757d;
    color: #adb5bd;
}

QPushButton#clearButton {
    background-color: #ff3b30;
    color: white;
}

QPushButton#clearButton:hover {
    background-color: #e0352b;
}

QPushButton#clearButton:pressed {
    background-color: #c82333;
}

QPushButton#saveButton {
    background-color: #28a745;
    color: white;
}

QPushButton#saveButton:hover {
    background-color: #218838;
}

QPushButton#saveButton:pressed {
    background-color: #1e7e34;
}

QPushButton#clearButton:disabled, QPushButton#saveButton:disabled {
    background-color: #6c757d;
    color: #adb5bd;
}

/* Splitter Styles */
QSplitter::handle {
    background-color: #e0e0e0;
    width: 2px;
}

QSplitter::handle:hover {
    background-color: #0d6efd;
}

/* Drop Zone Styles */
QWidget#dropZoneWidget {
    background-color: #F8F9F9;
    border: 2px dashed #ddd;
    border-radius: 10px;
    min-height: 200px;
}

QWidget#dropZoneWidget:hover {
    border: 2px dashed #aaa;
    background-color: #f9f9f9;
}

QWidget#dropZoneWidget QLabel {
    background-color: transparent;
    color: #666;
    font-size: 24px;
}

QWidget#dropZoneWidget[dragActive="true"] {
    background-color: rgba(13, 110, 253, 0.1);
    border: 2px dashed #0d6efd;
}

QWidget#dropZoneWidget[dragActive="true"] QLabel {
    color: #0d6efd;
}

/* Cloud Icon Style */
QLabel#cloudIconLabel {
    background-color: #e0e0e0;
    border-radius: 16px;
    min-width: 32px;
    min-height: 32px;
}

/* Scroll Area Styles */
QScrollArea {
    border: none;
    background-color: white;
}

QWidget#listViewContainer {
    background-color: white;
}

/* Scrollbar Styles */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0px 2px 0px 2px;
}

QScrollBar::handle:vertical {
    background: rgba(0, 0, 0, 60%);
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
    background: none;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: none;
}

QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    margin: 2px 0px 2px 0px;
}

QScrollBar::handle:horizontal {
    background: rgba(0, 0, 0, 60%);
    min-width: 20px;
    border-radius: 4px;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
    background: none;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
}

/* Gallery Header Styles */
QWidget#galleryHeader {
    background-color: transparent;
    padding: 10px 15px;
    border-bottom: 1px solid #e0e0e0;
}

/* Gallery Empty state Styles */
QLabel#emptyStateLabel {
    background-color: transparent;
    color: #666;
    font-size: 16px;
    text-align: center;
}

/* Image Thumbnail Styles - Horizontal layout */
QFrame#thumbnailFrame {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 8px;
    margin: 4px;
}

QFrame#thumbnailFrame QLabel#imageLabel {
    border: none;
    background-color: transparent;
    min-width: 80px;
    max-width: 80px;
    min-height: 80px;
    max-height: 80px;
}

QFrame#thumbnailFrame QLabel#nameLabel {
    font-size: 16px;
    color: #333;
    font-weight: 500;
    border: none;
    padding-left: 10px;
}

/* Progress Bar Styles */
QProgressBar {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    border: 2px solid #e0e0e0;
    border-radius: 5px;
    text-align: center;
    font-weight: 500;
}

QProgressBar::chunk {
    background-color: #0d6efd;
    border-radius: 3px;
}

/* Dark Mode Styles */
.dark QWidget#mainWidget {
    background-color: #2d2d2d;
}

.dark QWidget#sidebarWidget {
    background-color: #2d2d2d;
}

.dark QSplitter::handle {
    background-color: #444;
}

.dark QSplitter::handle:hover {
    background-color: #0d6efd;
}

.dark QScrollArea, .dark QWidget#listViewContainer {
    background-color: #2d2d2d;
}

.dark QWidget#dropZoneWidget {
    border: 2px dashed #555;
    background-color: #333;
}

.dark QWidget#dropZoneWidget:hover {
    border: 2px dashed #777;
    background-color: #383838;
}

.dark QWidget#dropZoneWidget QLabel {
    color: #aaa;
}

.dark QWidget#dropZoneWidget[dragActive="true"] {
    background-color: rgba(13, 110, 253, 0.2);
    border: 2px dashed #0d6efd;
}

.dark QWidget#dropZoneWidget[dragActive="true"] QLabel {
    color: #0d6efd;
}

.dark QLabel#cloudIconLabel {
    background-color: #555;
}

.dark QLabel#titleLabel, .dark QLabel#galleryTitle {
    color: #eee;
}

.dark QFrame#thumbnailFrame {
    background-color: #333;
    border: 1px solid #444;
}

.dark QFrame#thumbnailFrame QLabel#nameLabel {
    color: #eee;
}

.dark QProgressBar {
    border: 2px solid #555;
    color: #eee;
}

.dark QProgressBar::chunk {
    background-color: #0d6efd;
}
"""