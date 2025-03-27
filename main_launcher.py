# new launcher that accommodate the new settings configurator

import sys
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox, QPushButton, QDialog
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QFont

from ui.about_dialog import AboutDialog
from ui.ui_components import ModernTextEdit, ModernProgressBar, ModernButton
from managers.config_manager import ConfigManager
from managers.theme_manager import ThemeManager
from core.folder_operations import FolderOpeningThread
from settings import ConfiguratorDialog


class FolderOpenerExecutionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        if getattr(sys, 'frozen', False):
            self.application_path = os.path.dirname(sys.executable)
        else:
            self.application_path = os.path.dirname(os.path.abspath(__file__))

        self.config_path = os.path.join(self.application_path, 'folders_config.json')

        self.config_manager = ConfigManager(self.config_path)
        self.load_config()

        self.setup_ui()

        self.folder_thread = None

        self.setup_theme()

        app = QApplication.instance()
        app.paletteChanged.connect(self.on_palette_changed)

        self.current_theme = "light" if not ThemeManager.check_theme("light") == "dark" else "dark"

        self.theme_timer = QTimer(self)
        self.theme_timer.timeout.connect(self.check_theme)
        self.theme_timer.start(2000)

        if self.start_instantly:
            self.log("Auto-execution enabled in config. Starting folder opening process...")
            self.execute_folder_opening()

        # Show welcome dialog if this is first run
        if self.is_first_run:
            self.show_welcome_dialog()

    def load_config(self):
        self.folders, self.sleep_timers, self.start_instantly, self.auto_close, self.auto_close_delay, self.is_first_run = self.config_manager.load_config(
            self)

    def setup_ui(self):
        self.setWindowTitle("Multi Folder Opener Launcher")
        self.setMinimumSize(600, 400)

        icon_path = os.path.join(self.application_path, 'icons', 'launcher.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            QApplication.instance().setWindowIcon(QIcon(icon_path))


        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        self.header_label = QLabel("Execution Log")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.header_label.setFont(font)
        self.header_label.setContentsMargins(0, 0, 0, 10)
        main_layout.addWidget(self.header_label)

        # Add warning label
        self.warning_label = QLabel("⚠️ WARNING: Please do not interact with your computer during folder opening process!")
        self.warning_label.setStyleSheet(
            "color: #721c24;"
            "background-color: #f8d7da;"
            "border: 1px solid #f5c6cb;"
            "border-radius: 4px;"
            "padding: 8px;"
            "font-weight: bold;"
        )
        self.warning_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.warning_label)

        self.log_text = ModernTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text)

        self.progress_bar = ModernProgressBar()
        main_layout.addWidget(self.progress_bar)

        # Add the new button to open the configurator
        self.open_configurator_button = QPushButton("Open Configurator")
        self.open_configurator_button.clicked.connect(self.open_configurator)
        main_layout.addWidget(self.open_configurator_button)

        self.execute_button = ModernButton("Execute Folder Opening")
        self.execute_button.clicked.connect(self.execute_folder_opening)
        main_layout.addWidget(self.execute_button)

        self.author_label = QLabel("Created by Avaxerrr")
        self.author_label.setStyleSheet("color: palette(text); text-decoration: underline; cursor: pointer;")
        self.author_label.setCursor(Qt.PointingHandCursor)
        self.author_label.mousePressEvent = self.show_about_dialog
        self.author_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.author_label)
        font = QFont()
        font.setItalic(True)
        self.author_label.setFont(font)

        self.setCentralWidget(central_widget)

    def setup_theme(self):
        ThemeManager.setup_theme(QApplication.instance(), self.execute_button)

    def on_palette_changed(self, palette):
        ThemeManager.setup_theme(QApplication.instance(), self.execute_button, True)

    def check_theme(self):
        new_theme = ThemeManager.check_theme(self.current_theme)
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            ThemeManager.setup_theme(QApplication.instance(), self.execute_button, True)

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_text.append(log_entry)

    def open_configurator(self):
        dialog = ConfiguratorDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.reload_config()

    def reload_config(self):
        self.folders, self.sleep_timers, self.start_instantly, self.auto_close, self.auto_close_delay, _ = self.config_manager.load_config(
            self)
        self.log("Configuration reloaded.")

    def execute_folder_opening(self):
        if self.folder_thread and self.folder_thread.isRunning():
            self.log("Folder opening process is already running.")
            return

        self.execute_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        self.log("Starting folder opening process...")

        self.folder_thread = FolderOpeningThread(self.folders, self.sleep_timers)
        self.folder_thread.log_signal.connect(self.log)
        self.folder_thread.progress_signal.connect(self.update_progress)
        self.folder_thread.finished_signal.connect(self.on_folder_opening_finished)
        self.folder_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue((value + 1) * 100 // len(self.folders))

    def on_folder_opening_finished(self, success, message):
        self.execute_button.setEnabled(True)
        if success:
            self.log("Folder opening process completed successfully.")
            if self.auto_close:
                delay_ms = int(self.auto_close_delay * 1000)
                self.log(f"Auto-close enabled. Closing application in {self.auto_close_delay} seconds...")
                QTimer.singleShot(delay_ms, self.close)
        else:
            self.log(f"Folder opening process failed: {message}")

    def show_about_dialog(self, event):
        dialog = AboutDialog(self)
        dialog.exec()

    def show_welcome_dialog(self):
        welcome_box = QMessageBox(self)
        welcome_box.setWindowTitle("Welcome to Multi Folder Opener")
        welcome_box.setIcon(QMessageBox.Information)
        welcome_box.setText("Before you can use it, you need to configure which folders to open.\n Please click 'Open Configurator' to set up your folder paths.")
        (QMessageBox.Ok)

        # Use the application icon for the dialog
        if self.windowIcon():
            welcome_box.setWindowIcon(self.windowIcon())

        welcome_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderOpenerExecutionApp()
    window.show()
    sys.exit(app.exec())
