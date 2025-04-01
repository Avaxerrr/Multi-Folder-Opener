# about_dialog.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Multi Folder Opener")
        self.setFixedSize(450, 520)  # Slightly increased height for better spacing

        # Main layout with margins
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)  # Added margins on all sides
        self.setLayout(layout)

        # App title
        title_label = QLabel("Multi Folder Opener")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Version
        version_label = QLabel("Version 1.1.0")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        layout.addSpacing(10)

        # Description
        description = (
            "Multi Folder Opener is a Windows utility that streamlines your workflow by "
            "opening multiple folders simultaneously in Windows Explorer tabs. "
            "It uses automation to navigate Explorer and open each configured folder in a new tab, "
            "saving you time and reducing repetitive tasks."
        )
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignJustify)
        layout.addWidget(desc_label)
        layout.addSpacing(10)

        # Features
        features_label = QLabel("Key Features:")
        features_label.setFont(QFont("", weight=QFont.Bold))
        layout.addWidget(features_label)

        features = QLabel(
            "• Opens multiple folders in Windows Explorer tabs with a single click\n"
            "• Configurable delay settings to accommodate different system speeds\n"
            "• Editable folder paths reordering\n"
            "• Auto-start and auto-close options for automated workflows\n"
            "• Supports both light and dark themes to match your Windows settings"
        )
        features.setWordWrap(True)
        layout.addWidget(features)
        layout.addSpacing(15)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)

        # Author
        author_label = QLabel("Created by Avaxerrr")
        author_label.setFont(QFont("", weight=QFont.Bold))
        author_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(author_label)

        # GitHub link with updated text
        github_link = QLabel("Check for updates of the app here:<br><a href='https://github.com/Avaxerrr/Multi-Folder-Opener.git'>GitHub Repository</a>")
        github_link.setOpenExternalLinks(True)
        github_link.setAlignment(Qt.AlignCenter)
        layout.addWidget(github_link)
        layout.addSpacing(10)

        # License
        license_label = QLabel("Copyright © 2025 Avaxerrr. Licensed under the MIT License.")
        license_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(license_label)
        layout.addSpacing(10)

        # Icon Credits
        credits_label = QLabel("Icon Credits:")
        credits_label.setFont(QFont("", weight=QFont.Bold))
        credits_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(credits_label)

        launcher_credit = QLabel(
            "Launcher icon created by <a href='https://www.flaticon.com/authors/3d/color/'>3D Color</a> from <a href='https://www.flaticon.com/'>Flaticon</a>")
        launcher_credit.setOpenExternalLinks(True)
        launcher_credit.setAlignment(Qt.AlignCenter)
        layout.addWidget(launcher_credit)

        layout.addStretch()

        # Close button
        close_button = QPushButton("Close")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.accept)

        # Button layout for centering
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Apply theme-compatible styling with border
        self.setStyleSheet("""
            QDialog {
                background-color: palette(window);
                border: 1px solid palette(mid);
            }
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
        """)
