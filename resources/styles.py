STYLESHEET = """
QMainWindow {
    background-color: transparent;
}

QWidget#mainWidget {
    background-color: #f5f5f5;
    border-radius: 10px;
}

QWidget#sidebarWidget {
    background-color: transparent;
    border-right: 1px solid #e0e0e0;
}

QLabel#titleLabel {
    font-family: "SF Pro Display Regular";
    font-size: 32px;
    font-weight: 600;
    padding: 8px 0px;
    color: #333;
}

QPushButton {
    font-family: "SF Pro Display Regular";
    background-color: #0d6efd;
    color: white;
    border-radius: 8px;
    padding: 12px 12px;
    font-weight: 500;
    font-size: 18px;
    text-align: left;
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
    background-color: #dc3545;
    color: white;
}

QPushButton#clearButton:hover {
    background-color: #c82333;
}

QPushButton#clearButton:pressed {
    background-color: #bd2130;
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

QToolButton {
    font-family: "SF Pro Display Regular";
    background-color: transparent;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 8px;
    margin: 2px;
}

QToolButton:hover {
    background-color: #f8f9fa;
    border-color: #adb5bd;
}

QToolButton:pressed {
    background-color: #e9ecef;
    border-color: #6c757d;
}

QToolButton:checked {
    background-color: #0d6efd;
    border-color: #0d6efd;
    color: white;
}

QLabel#dropZoneLabel {
    background-color: rgba(200, 200, 200, 50);
    border: 2px dashed #ccc;
    border-radius: 10px;
    padding: 30px 20px;
    font-size: 14px;
    color: #666;
    font-weight: 500;
}

QScrollArea {
    border: none;
    background-color: transparent;
}

QLabel#titleLabel {
    font-family: "SF Pro Display Regular";
    font-size: 24px;
    font-weight: 600;
    padding: 8px 0px;
    color: #333;
}

QWidget#galleryHeader {
    background-color: transparent;
    padding: 10px 15px;
    border-bottom: 1px solid #e0e0e0;
}

QLabel#galleryTitle {
    font-family: "SF Pro Display Regular";
    font-size: 16px;
    font-weight: 600;
    color: #333;
}

QProgressBar {
    font-family: "SF Pro Display Regular";
    border: 2px solid #e0e0e0;
    border-radius: 5px;
    text-align: center;
    font-weight: 500;
}

QProgressBar::chunk {
    background-color: #0d6efd;
    border-radius: 3px;
}

/* Dark mode styles */
.dark QWidget#mainWidget {
    background-color: #2d2d2d;
}

.dark QWidget#sidebarWidget {
    border-right: 1px solid #3d3d3d;
}

.dark QWidget#galleryHeader {
    border-bottom: 1px solid #3d3d3d;
}

.dark QToolButton {
    border: 1px solid #555;
    color: #eee;
}

.dark QToolButton:hover {
    background-color: #404040;
    border-color: #666;
}

.dark QToolButton:pressed {
    background-color: #4a4a4a;
    border-color: #777;
}

.dark QLabel#dropZoneLabel {
    border: 2px dashed #555;
    color: #aaa;
    background-color: rgba(80, 80, 80, 50);
}

.dark QLabel#titleLabel {
    color: #eee;
}

.dark QLabel#galleryTitle {
    color: #eee;
}

.dark QLabel {
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