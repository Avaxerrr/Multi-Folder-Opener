import sys
import os
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QFont

from ui.ui_components import ModernTextEdit
from managers.config_manager import ConfigManager
from managers.theme_manager import ThemeManager
from core.folder_operations import FolderOpeningThread


class FolderOpenerExecutionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        if getattr(sys, 'frozen', False):
            self.application_path = os.path.dirname(sys.executable)
        else:
            self.application_path = os.path.dirname(os.path.abspath(__file__))

        self.config_path = os.path.join(self.application_path, 'folders_config.json')

        self.config_manager = ConfigManager(self.config_path)
        self.folders, self.sleep_timers, self.start_instantly = self.config_manager.load_config(self)

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

    def setup_ui(self):
        self.setWindowTitle("Folder Opener Execution")
        self.setMinimumSize(600, 400)

        icon_path = os.path.join(self.application_path, 'icons', 'folder_automator.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            QApplication.instance().setWindowIcon(QIcon(icon_path))

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        self.header_label = QLabel("Folder Opener Execution Log")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.header_label.setFont(font)
        self.header_label.setContentsMargins(0, 0, 0, 10)
        main_layout.addWidget(self.header_label)

        self.log_text = ModernTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text)

        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 5px;
                text-align: center;
                background-color: rgba(0, 0, 0, 0.1);
                height: 20px;
            }

            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        self.execute_button = QPushButton("Execute Folder Opening")
        self.execute_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }

            QPushButton:hover {
                background-color: #45a049;
            }

            QPushButton:pressed {
                background-color: #3d8b40;
            }

            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.execute_button.clicked.connect(self.execute_folder_opening)
        main_layout.addWidget(self.execute_button)

        author_label = QLabel("Created by Avaxerrr")
        author_label.setAlignment(Qt.AlignRight)
        font = QFont()
        font.setItalic(True)
        author_label.setFont(font)
        main_layout.addWidget(author_label)

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
        else:
            self.log(f"Folder opening process failed: {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderOpenerExecutionApp()
    window.show()
    sys.exit(app.exec())