# collapsible_section.py

"""Version 1.1"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QApplication, QCheckBox, QDoubleSpinBox
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QEvent
from PySide6.QtGui import QFont, QColor, QPalette


class CollapsibleSection(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Header
        self.header_widget = QWidget()
        self.header_widget.setCursor(Qt.PointingHandCursor)
        self.header_widget.setMinimumHeight(30)

        # Header layout
        self.header_layout = QHBoxLayout(self.header_widget)
        self.header_layout.setContentsMargins(10, 0, 10, 0)

        # Arrow indicator
        self.arrow = QLabel("▶")

        # Title
        self.title_label = QLabel(title)
        font = QFont()
        font.setBold(True)
        self.title_label.setFont(font)

        # Add to header layout
        self.header_layout.addWidget(self.arrow)
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()

        # Content area
        self.content_area = QWidget()

        # Content layout
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(15, 10, 15, 10)
        self.content_layout.setSpacing(5)

        # Add separator line
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.HLine)
        self.separator.setFrameShadow(QFrame.Sunken)
        self.separator.setMaximumHeight(1)

        # Add widgets to main layout
        self.main_layout.addWidget(self.header_widget)
        self.main_layout.addWidget(self.separator)
        self.main_layout.addWidget(self.content_area)

        # Animation
        self.animation = QPropertyAnimation(self.content_area, b"maximumHeight")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(self.animation_finished)

        # Connect signals
        self.header_widget.mousePressEvent = self.toggle_content

        # Start collapsed
        self.collapsed = True
        self.content_area.setMaximumHeight(0)
        self.content_area.setMinimumHeight(0)

        # Apply initial theme
        self.update_theme()

        # Install event filter to catch palette changes
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == QApplication.instance() and event.type() == QEvent.ApplicationPaletteChange:
            self.update_theme()
        return super().eventFilter(obj, event)

    def update_theme(self):
        # Get current application palette
        app_palette = QApplication.instance().palette()
        is_dark = app_palette.base().color().lightness() < app_palette.windowText().color().lightness()

        if is_dark:
            # Dark theme
            header_bg = "#353535"
            content_bg = "#2C2C2C"
            separator_color = "#3d3d3d"
            text_color = "white"

            # Form control styling for dark theme
            form_control_style = """
                QCheckBox { color: white; }
                QDoubleSpinBox { 
                    background-color: #3d3d3d; 
                    color: white; 
                    border: 1px solid #555; 
                }
                QLabel { color: white; }
            """
        else:
            # Light theme
            header_bg = "#d0d0d0"
            content_bg = "#f0f0f0"
            separator_color = "#c0c0c0"
            text_color = "black"

            # Form control styling for light theme
            form_control_style = """
                QCheckBox { color: black; }
                QDoubleSpinBox { 
                    background-color: white; 
                    color: black; 
                    border: 1px solid #aaa; 
                }
                QLabel { color: black; }
            """

        # Apply theme to components
        self.header_widget.setStyleSheet(f"background-color: {header_bg};")
        self.content_area.setStyleSheet(f"background-color: {content_bg};")
        self.separator.setStyleSheet(f"background-color: {separator_color};")
        self.arrow.setStyleSheet(f"color: {text_color}; font-weight: bold;")
        self.title_label.setStyleSheet(f"color: {text_color};")

        # Update styles for all child widgets
        for i in range(self.content_layout.count()):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                self.apply_widget_style(widget, is_dark)

    def toggle_content(self, event):
        if self.collapsed:
            self.expand()
        else:
            self.collapse()

    def expand(self):
        if not self.collapsed:
            return

        self.collapsed = False
        self.arrow.setText("▼")

        # Get the full height
        content_height = self.content_layout.sizeHint().height()

        # Animate
        self.animation.setStartValue(0)
        self.animation.setEndValue(content_height)
        self.animation.start()

    def collapse(self):
        if self.collapsed:
            return

        self.collapsed = True
        self.arrow.setText("▶")

        # Animate
        self.animation.setStartValue(self.content_area.maximumHeight())
        self.animation.setEndValue(0)
        self.animation.start()

    def animation_finished(self):
        # Adjust window size if needed when animation completes
        if not self.collapsed and self.window():
            # Check if content is partially outside window
            window_size = self.window().size()
            content_bottom = self.mapTo(self.window(), self.content_area.geometry().bottomRight()).y()

            if content_bottom > window_size.height():
                # Resize window to fit content
                new_height = window_size.height() + (content_bottom - window_size.height()) + 20  # Add padding
                self.window().resize(window_size.width(), new_height)

    def add_widget(self, widget):
        app_palette = QApplication.instance().palette()
        is_dark = app_palette.base().color().lightness() < app_palette.windowText().color().lightness()
        self.apply_widget_style(widget, is_dark)
        self.content_layout.addWidget(widget)

    def apply_widget_style(self, widget, is_dark):
        if isinstance(widget, QCheckBox):
            self.apply_checkbox_style(widget, is_dark)
        elif isinstance(widget, QDoubleSpinBox):
            self.apply_spinbox_style(widget, is_dark)
        # Recursively apply styles to child widgets
        elif hasattr(widget, 'children'):
            for child in widget.children():
                if isinstance(child, QWidget):
                    self.apply_widget_style(child, is_dark)

    def apply_checkbox_style(self, checkbox, is_dark):
        if is_dark:
            checkbox.setStyleSheet("""
            QCheckBox { 
                color: white; 
                spacing: 5px;
            }
            
            QCheckBox::indicator {
                width: 13px;
                height: 13px;
                background-color: #3d3d3d;
                border: 1px solid #555;
                border-radius: 2px;
            }
            
            QCheckBox::indicator:checked {
                background-color: #4CAF50;
                border: 1px solid #4CAF50;
            }
            """)
        else:
            checkbox.setStyleSheet("""
                QCheckBox { color: black; }
                QCheckBox::indicator { 
                    width: 13px; 
                    height: 13px; 
                    background-color: white; 
                    border: 1px solid #aaa; 
                }
                QCheckBox::indicator:checked { 
                    background-color: #4CAF50; 
                }
            """)

    def apply_spinbox_style(self, spinbox, is_dark):
        if is_dark:
            spinbox.setStyleSheet("""
                QDoubleSpinBox { 
                    background-color: #3d3d3d; 
                    color: white; 
                    border: 1px solid #555; 
                    padding: 2px;
                }
                QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { 
                    background-color: #555; 
                    border: 1px solid #666;
                    width: 16px;
                    subcontrol-origin: margin;
                }
                QDoubleSpinBox::up-arrow, QDoubleSpinBox::down-arrow {
                    width: 7px;
                    height: 7px;
                }
                            }
                QDoubleSpinBox::up-arrow {
                    image: url(icons/arrow-up-white.png);
                    width: 7px;
                    height: 7px;
                }
                QDoubleSpinBox::down-arrow {
                    image: url(icons/arrow-down-white.png);
                    width: 7px;
                    height: 7px;
                }
            """)
        else:
            spinbox.setStyleSheet("""
                QDoubleSpinBox { 
                    background-color: white; 
                    color: black; 
                    border: 1px solid #aaa; 
                    padding: 2px;
                }
                QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { 
                    background-color: #e0e0e0; 
                    border: 1px solid #ccc;
                    width: 16px;
                    subcontrol-origin: margin;
                }
                QDoubleSpinBox::up-arrow {
                    image: url(icons/arrow-up-dark.png);
                    width: 7px;
                    height: 7px;
                }
                QDoubleSpinBox::down-arrow {
                    image: url(icons/arrow-down-dark.png);
                    width: 7px;
                    height: 7px;
                }
            """)

    def add_layout(self, layout):
        self.content_layout.addLayout(layout)
