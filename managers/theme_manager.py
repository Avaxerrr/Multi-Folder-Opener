# theme_manager.py

import darkdetect
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtGui import QPalette, QColor, Qt


class ThemeManager:
    @staticmethod
    def check_theme(current_theme):
        """Check if system theme has changed"""
        system_theme = "dark" if darkdetect.isDark() else "light"
        return system_theme if system_theme != current_theme else current_theme

    @staticmethod
    def setup_theme(app, execute_button=None, cancel_button=None, force_update=False):
        """Set up application theme based on system settings"""
        # Set the application style to Fusion (from original)
        QApplication.setStyle("Fusion")

        if darkdetect.isDark():
            ThemeManager.set_dark_theme(app, execute_button, cancel_button, force_update)
        else:
            ThemeManager.set_light_theme(app, execute_button, cancel_button, force_update)

    @staticmethod
    def set_dark_theme(app, execute_button=None, cancel_button=None, force_update=False):
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

        # Style execute button
        if execute_button:
            ThemeManager.style_execute_button(execute_button)

        # Style cancel button
        if cancel_button:
            ThemeManager.style_cancel_button(cancel_button)

    @staticmethod
    def set_light_theme(app, execute_button=None, cancel_button=None, force_update=False):
        """Apply light theme to the application"""
        if not isinstance(app, QApplication):
            return

        # Reset to default palette for light theme (from original)
        app.setPalette(QPalette())

        # Style execute button
        if execute_button:
            ThemeManager.style_execute_button(execute_button)

        # Style cancel button
        if cancel_button:
            ThemeManager.style_cancel_button(cancel_button)

    @staticmethod
    def style_execute_button(button):
        """Apply execute button styling"""
        if not isinstance(button, QPushButton):
            return

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
            QPushButton:disabled {
                background-color: #a5d6a7;
                color: #e8f5e9;
            }
        """)

    @staticmethod
    def style_cancel_button(button):
        """Apply cancel button styling"""
        if not isinstance(button, QPushButton):
            return

        button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e53935;
            }
            QPushButton:pressed {
                background-color: #d32f2f;
            }
            QPushButton:disabled {
                background-color: #423736;
                color: #ffebee;
            }
        """)

    @staticmethod
    def on_palette_changed(app, execute_button=None, cancel_button=None):
        """Handle palette change events"""
        ThemeManager.setup_theme(app, execute_button, cancel_button, True)
