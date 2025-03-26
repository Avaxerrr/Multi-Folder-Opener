# about_dialog.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QDesktopServices


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Multi Folder Opener")
        self.setFixedSize(450, 350)

        # Main layout
        layout = QVBoxLayout()
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
        version_label = QLabel("Version 1.0.0")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        # Description
        description = (
            "Folder Opener is a utility designed to streamline your workflow by "
            "opening multiple folders simultaneously in Windows Explorer. "
            "Configure your frequently accessed folders and launch them with a single click, "
            "saving time and reducing repetitive tasks. Perfect for developers, designers, "
            "and anyone who regularly works with multiple project directories."
        )
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignJustify)
        layout.addWidget(desc_label)
        layout.addSpacing(10)

        # Author
        author_label = QLabel("Created by Avaxerrr")
        author_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(author_label)

        # GitHub link
        github_link = QLabel("<a href='https://github.com/yourusername/folder-opener'>GitHub Repository</a>")
        github_link.setOpenExternalLinks(True)
        github_link.setAlignment(Qt.AlignCenter)
        layout.addWidget(github_link)

        # License
        license_label = QLabel("Licensed under MIT License")
        license_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(license_label)

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

        # Apply theme-compatible styling
        self.setStyleSheet("""
            QDialog {
                background-color: palette(window);
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
