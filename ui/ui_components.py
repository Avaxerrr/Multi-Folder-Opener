from PySide6.QtWidgets import QScrollBar, QListWidget
from PySide6.QtCore import Qt


class ModernScrollBar(QScrollBar):
    def __init__(self, orientation=Qt.Vertical, parent=None):
        super().__init__(orientation, parent)
        self.setStyleSheet(self._get_stylesheet())

    def _get_stylesheet(self):
        # Modern scroll bar styling
        return """
            QScrollBar:vertical {
                border: none;
                background: rgba(0, 0, 0, 0.1);
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical {
                background-color: rgba(80, 80, 80, 0.7);
                min-height: 30px;
                border-radius: 5px;
            }

            QScrollBar::handle:vertical:hover {
                background-color: rgba(80, 80, 80, 0.9);
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
                border: none;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }

            QScrollBar:horizontal {
                border: none;
                background: rgba(0, 0, 0, 0.1);
                height: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }

            QScrollBar::handle:horizontal {
                background-color: rgba(80, 80, 80, 0.7);
                min-width: 30px;
                border-radius: 5px;
            }

            QScrollBar::handle:horizontal:hover {
                background-color: rgba(80, 80, 80, 0.9);
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                background: none;
                border: none;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
        """


class ModernListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set vertical scroll bar
        self.setVerticalScrollBar(ModernScrollBar(Qt.Vertical, self))
        # Set horizontal scroll bar
        self.setHorizontalScrollBar(ModernScrollBar(Qt.Horizontal, self))

        # Additional styling for the list widget (from monolithic version)
        self.setStyleSheet("""
            QListWidget {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 5px;
                padding: 5px;
            }
        """)
