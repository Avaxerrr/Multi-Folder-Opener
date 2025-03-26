# theme_manager.py

import darkdetect
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor, Qt


class ThemeManager:
    @staticmethod
    def setup_theme(app_instance=None, open_button=None, force_update=False):
        # Set the application style to Fusion
        QApplication.setStyle("Fusion")

        # Check if system is using dark mode
        if darkdetect.isDark():
            # Dark palette
            ThemeManager.set_dark_theme()
        else:
            # Light palette (default)
            QApplication.setPalette(QPalette())  # Reset to default palette

        # Ensure the open button keeps its green styling if it exists
        if open_button:
            open_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")

    @staticmethod
    def set_dark_theme():
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

        QApplication.setPalette(dark_palette)

    @staticmethod
    def check_theme(current_theme):
        new_theme = "light" if not darkdetect.isDark() else "dark"
        if new_theme != current_theme:
            return new_theme
        return current_theme