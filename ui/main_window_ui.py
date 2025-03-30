# main_window_ui.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from ui.ui_components import ModernTextEdit, ModernProgressBar, ModernButton


class MainWindowUI:
    def __init__(self, main_window, icon=None):
        self.main_window = main_window
        self.icon = icon

        # UI components that will be accessed by the main application
        self.log_text = None
        self.progress_bar = None
        self.execute_button = None
        self.open_configurator_button = None
        self.author_label = None

    def setup_ui(self):
        """Set up the main window UI"""
        self.main_window.setWindowTitle("Multi Folder Opener Launcher")
        self.main_window.setMinimumSize(600, 400)

        if self.icon:
            self.main_window.setWindowIcon(self.icon)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # Header label
        header_label = QLabel("Execution Log")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        header_label.setFont(font)
        header_label.setContentsMargins(0, 0, 0, 10)
        main_layout.addWidget(header_label)

        # Warning label
        warning_label = QLabel("WARNING: Please do not interact with your computer during folder opening process!")
        warning_label.setStyleSheet(
            "color: #721c24; background-color: #f8d7da; border: 1px solid #f5c6cb; "
            "border-radius: 4px; padding: 8px; font-weight: bold;"
        )
        warning_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(warning_label)

        # Log text area
        self.log_text = ModernTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text)

        # Progress bar
        self.progress_bar = ModernProgressBar()
        main_layout.addWidget(self.progress_bar)

        # Configurator button
        self.open_configurator_button = QPushButton("Open Configurator")
        main_layout.addWidget(self.open_configurator_button)

        # Execute button
        self.execute_button = ModernButton("Execute Folder Opening")
        main_layout.addWidget(self.execute_button)

        # Author label
        author_layout = QHBoxLayout()
        author_layout.addStretch(1)
        self.author_label = QLabel("Created by Avaxerrr")
        self.author_label.setStyleSheet("color: palette(text); text-decoration: underline; cursor: pointer;")
        self.author_label.setCursor(Qt.PointingHandCursor)
        font = QFont()
        font.setItalic(True)
        self.author_label.setFont(font)
        author_layout.addWidget(self.author_label)
        main_layout.addLayout(author_layout)

        self.main_window.setCentralWidget(central_widget)

        return {
            'log_text': self.log_text,
            'progress_bar': self.progress_bar,
            'execute_button': self.execute_button,
            'open_configurator_button': self.open_configurator_button,
            'author_label': self.author_label
        }
