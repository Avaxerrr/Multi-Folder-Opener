# theme_manager.py

import darkdetect
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor, Qt


class ThemeManager:
    @staticmethod
    def check_theme(current_theme):
        """Check if system theme has changed"""
        system_theme = "dark" if darkdetect.isDark() else "light"
        return system_theme if system_theme != current_theme else current_theme

    @staticmethod
    def setup_theme(app, button=None, force_update=False):
        """Set up application theme based on system settings"""
        # Set the application style to Fusion (from original)
        QApplication.setStyle("Fusion")

        if darkdetect.isDark():
            ThemeManager.set_dark_theme(app, button, force_update)
        else:
            ThemeManager.set_light_theme(app, button, force_update)

    @staticmethod
    def set_dark_theme(app, button=None, force_update=False):
        """Apply dark theme to the application"""
        if not isinstance(app, QApplication):
            return

        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        app.setPalette(dark_palette)

        if button:
            # Green color with add hover/pressed states
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """)

    @staticmethod
    def set_light_theme(app, button=None, force_update=False):
        """Apply light theme to the application"""
        if not isinstance(app, QApplication):
            return

        # Reset to default palette for light theme (from original)
        app.setPalette(QPalette())

        if button:
            # Green color with add hover/pressed states
            button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """)

    @staticmethod
    def on_palette_changed(app, button=None):
        """Handle palette change events"""
        ThemeManager.setup_theme(app, button, True)
