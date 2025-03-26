# main_configurator.py

import sys
import os
import subprocess
import darkdetect
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLabel, QMessageBox,
                               QDoubleSpinBox, QGridLayout, QGroupBox, QCheckBox, QMenu, QListWidgetItem)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QFont

# Import our modules
from ui.ui_components import ModernListWidget
from managers.theme_manager import ThemeManager
from managers.config_manager import ConfigManager
from core.folder_operations import FolderOperations
from managers.startup_manager import StartupManager
from ui.about_dialog import AboutDialog


class FolderOpenerConfigApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Get the directory where the executable is located
        if getattr(sys, 'frozen', False):
            self.application_path = os.path.dirname(sys.executable)
        else:
            self.application_path = os.path.dirname(os.path.abspath(__file__))

        # Path to the config file
        self.config_path = os.path.join(self.application_path, 'folders_config.json')

        # Initialize config manager
        self.config_manager = ConfigManager(self.config_path)

        # Initialize folders list and sleep timers
        self.folders, self.sleep_timers, self.start_instantly, self.auto_close, self.auto_close_delay = self.config_manager.load_config(
            self)

        # Setup UI
        self.setWindowTitle("Multi Folder Opener Configurator")
        self.setMinimumSize(700, 500)

        # Set application icon
        # Replace 'app_icon.ico' with your actual icon file path
        icon_path = os.path.join(self.application_path, 'icons', 'configurator.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            app = QApplication.instance()
            app.setWindowIcon(QIcon(icon_path))

        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # Header label
        self.header_label = QLabel("Configure Folders and Launch Settings")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.header_label.setFont(font)
        self.header_label.setContentsMargins(0, 0, 0, 10)
        main_layout.addWidget(self.header_label)

        # Subheader/description for delay settings
        self.delay_description = QLabel(
            "Adjust delay settings based on your system performance. "
            "Longer delays help ensure folders open properly without errors on slower systems.")
        self.delay_description.setWordWrap(True)
        self.delay_description.setContentsMargins(0, 0, 0, 10)
        main_layout.addWidget(self.delay_description)

        # Create folders group
        folders_group = QGroupBox("Folders to Open")
        folders_layout = QVBoxLayout(folders_group)

        # Create list widget for folders with modern scrollbar
        self.folders_list = ModernListWidget()
        self.folders_list.setSelectionMode(ModernListWidget.SelectionMode.ExtendedSelection)
        FolderOperations.update_folders_list(self.folders_list, self.folders)
        folders_layout.addWidget(self.folders_list)

        # editable view list
        self.folders_list.itemChanged.connect(self.on_folder_edited)
        self.folders_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.folders_list.customContextMenuRequested.connect(self.show_folder_context_menu)

        # Create folder buttons layout
        folder_buttons_layout = QHBoxLayout()

        # Add folder button
        self.add_button = QPushButton("Add Folders")
        self.add_button.clicked.connect(self.add_folders)
        folder_buttons_layout.addWidget(self.add_button)

        # Remove folder button
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.remove_folder)
        folder_buttons_layout.addWidget(self.remove_button)

        # Move up button
        self.move_up_button = QPushButton("Move Up")
        self.move_up_button.clicked.connect(self.move_folder_up)
        folder_buttons_layout.addWidget(self.move_up_button)

        # Move down button
        self.move_down_button = QPushButton("Move Down")
        self.move_down_button.clicked.connect(self.move_folder_down)
        folder_buttons_layout.addWidget(self.move_down_button)

        folders_layout.addLayout(folder_buttons_layout)
        main_layout.addWidget(folders_group)

        # Create timing settings group
        timing_group = QGroupBox("Timing Settings (seconds)")
        timing_layout = QGridLayout(timing_group)

        # Explorer startup delay
        timing_layout.addWidget(QLabel("Explorer Startup Delay:"), 0, 0)
        self.explorer_startup_spin = QDoubleSpinBox()
        self.explorer_startup_spin.setRange(0.1, 5.0)
        self.explorer_startup_spin.setSingleStep(0.1)
        self.explorer_startup_spin.setValue(self.sleep_timers["explorer_startup"])
        self.explorer_startup_spin.setToolTip(
            "Time to wait after launching Windows Explorer before performing any actions.\n"
            "Increase this value if Explorer is slow to start on your system."
        )
        timing_layout.addWidget(self.explorer_startup_spin, 0, 1)

        # New tab delay
        timing_layout.addWidget(QLabel("New Tab Delay:"), 0, 2)
        self.new_tab_spin = QDoubleSpinBox()
        self.new_tab_spin.setRange(0.1, 5.0)
        self.new_tab_spin.setSingleStep(0.1)
        self.new_tab_spin.setValue(self.sleep_timers["new_tab"])
        self.new_tab_spin.setToolTip(
            "Time to wait after opening a new tab (Ctrl+T) before focusing the address bar.\n"
            "Increase this value if Explorer is slow to respond to the new tab command."
        )
        timing_layout.addWidget(self.new_tab_spin, 0, 3)

        # Address bar focus delay
        timing_layout.addWidget(QLabel("Address Bar Focus Delay:"), 1, 0)
        self.address_bar_spin = QDoubleSpinBox()
        self.address_bar_spin.setRange(0.1, 5.0)
        self.address_bar_spin.setSingleStep(0.1)
        self.address_bar_spin.setValue(self.sleep_timers["address_bar_focus"])
        self.address_bar_spin.setToolTip(
            "Time to wait after focusing the address bar (Ctrl+L) before typing the path.\n"
            "Increase this value if Explorer is slow to focus the address bar."
        )
        timing_layout.addWidget(self.address_bar_spin, 1, 1)

        # After typing delay
        timing_layout.addWidget(QLabel("After Typing Delay:"), 1, 2)
        self.after_typing_spin = QDoubleSpinBox()
        self.after_typing_spin.setRange(0.1, 5.0)
        self.after_typing_spin.setSingleStep(0.1)
        self.after_typing_spin.setValue(self.sleep_timers["after_typing"])
        self.after_typing_spin.setToolTip(
            "Time to wait after typing the folder path before pressing Enter.\n"
            "Increase this value if Explorer is slow to process the typed path."
        )
        timing_layout.addWidget(self.after_typing_spin, 1, 3)

        # After enter delay
        timing_layout.addWidget(QLabel("After Enter Delay:"), 2, 0)
        self.after_enter_spin = QDoubleSpinBox()
        self.after_enter_spin.setRange(0.1, 5.0)
        self.after_enter_spin.setSingleStep(0.1)
        self.after_enter_spin.setValue(self.sleep_timers["after_enter"])
        self.after_enter_spin.setToolTip(
            "Time to wait after pressing Enter before proceeding to the next folder.\n"
            "Increase this value if Explorer is slow to navigate to the folder."
        )
        timing_layout.addWidget(self.after_enter_spin, 2, 1)

        main_layout.addWidget(timing_group)

        # Create options group
        options_group = QGroupBox("Launch Options")
        options_layout = QGridLayout(options_group)
        options_layout.setContentsMargins(20, 10, 20, 10)  # Add padding to shift content inward

        # Start instantly checkbox (left column)
        self.start_instantly_checkbox = QCheckBox("Start instantly when launched")
        self.start_instantly_checkbox.setChecked(self.start_instantly)
        self.start_instantly_checkbox.setToolTip(
            "If checked, the folder opener will automatically open all folders when launched.\n"
            "This is useful if you want to set up a shortcut to quickly open all your folders."
        )
        options_layout.addWidget(self.start_instantly_checkbox, 0, 0, Qt.AlignLeft)  # Row 0, Column 0

        # Start on Windows boot checkbox (right column)
        self.start_on_boot_checkbox = QCheckBox("Start on Windows boot")
        self.start_on_boot_checkbox.setToolTip(
            "If checked, the folder opener will automatically start when Windows starts."
        )
        # Check if startup shortcut exists and set checkbox accordingly
        self.start_on_boot_checkbox.setChecked(StartupManager.check_startup_shortcut_exists())
        options_layout.addWidget(self.start_on_boot_checkbox, 0, 1, Qt.AlignRight)  # Row 0, Column 1

        # Auto-close executioner checkbox (left column)
        self.auto_close_checkbox = QCheckBox("Auto-close the launcher when complete")
        self.auto_close_checkbox.setChecked(self.auto_close if hasattr(self, 'auto_close') else False)
        self.auto_close_checkbox.setToolTip(
            "If checked, the executioner will automatically close after opening all folders."
        )
        options_layout.addWidget(self.auto_close_checkbox, 1, 0, Qt.AlignLeft)  # Row 1, Column 0

        # Auto-close delay layout (left column, below checkbox)
        auto_close_delay_layout = QHBoxLayout()
        auto_close_delay_layout.addWidget(QLabel("Close delay:"))
        self.auto_close_delay_spin = QDoubleSpinBox()
        self.auto_close_delay_spin.setRange(0.1, 10.0)  # 0.5 to 10 seconds
        self.auto_close_delay_spin.setSingleStep(0.1)
        self.auto_close_delay_spin.setValue(self.auto_close_delay if hasattr(self, 'auto_close_delay') else 1.5)
        self.auto_close_delay_spin.setSuffix(" seconds")
        self.auto_close_delay_spin.setToolTip(
            "Delay in seconds before closing the executioner after completing folder opening."
        )
        auto_close_delay_layout.addWidget(self.auto_close_delay_spin)
        auto_close_delay_layout.addStretch(1)
        options_layout.addLayout(auto_close_delay_layout, 2, 0)  # Row 2, Column 0

        main_layout.addWidget(options_group)

        # Create bottom buttons layout
        bottom_buttons_layout = QHBoxLayout()

        # Save button
        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.save_config)
        bottom_buttons_layout.addWidget(self.save_button)

        # Open folders button
        self.open_button = QPushButton("Start Launcher")
        self.open_button.clicked.connect(self.open_folders)
        self.open_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        bottom_buttons_layout.addWidget(self.open_button)

        main_layout.addLayout(bottom_buttons_layout)

        self.author_label = QLabel("Created by Avaxerrr")
        self.author_label.setStyleSheet("color: palette(text); text-decoration: underline; cursor: pointer;")
        self.author_label.setCursor(Qt.PointingHandCursor)
        self.author_label.mousePressEvent = self.show_about_dialog
        self.author_label.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.author_label)
        font = QFont()
        font.setItalic(True)
        self.author_label.setFont(font)

        # Set central widget
        self.setCentralWidget(central_widget)

        # Setup theme
        ThemeManager.setup_theme(QApplication.instance(), self.open_button)

        # Connect theme change detection
        self.theme_timer = QTimer(self)
        self.theme_timer.timeout.connect(self.check_theme)
        self.theme_timer.start(1000)  # Check every second

        # Connect to application palette changed signal (from monolithic version)
        app = QApplication.instance()
        app.paletteChanged.connect(self.on_palette_changed)

        # Store current theme state
        self.is_dark_mode = darkdetect.isDark()

    def on_palette_changed(self, palette):
        """Handle palette changes from the application (from monolithic version)"""
        ThemeManager.setup_theme(QApplication.instance(), self.open_button, True)

    def check_theme(self):
        # Check if theme has changed
        current_dark_mode = darkdetect.isDark()
        if current_dark_mode != self.is_dark_mode:
            self.is_dark_mode = current_dark_mode
            ThemeManager.setup_theme(QApplication.instance(), self.open_button, True)

    def add_folders(self):
        if FolderOperations.add_folders(self, self.folders):
            FolderOperations.update_folders_list(self.folders_list, self.folders)

    def remove_folder(self):
        if FolderOperations.remove_folder(self.folders_list, self.folders):
            FolderOperations.update_folders_list(self.folders_list, self.folders)

    def move_folder_up(self):
        if FolderOperations.move_folder_up(self.folders_list, self.folders):
            FolderOperations.update_folders_list(self.folders_list, self.folders)

    def move_folder_down(self):
        if FolderOperations.move_folder_down(self.folders_list, self.folders):
            FolderOperations.update_folders_list(self.folders_list, self.folders)

    def save_config(self):
        # Update sleep timers from UI
        self.sleep_timers["explorer_startup"] = self.explorer_startup_spin.value()
        self.sleep_timers["new_tab"] = self.new_tab_spin.value()
        self.sleep_timers["address_bar_focus"] = self.address_bar_spin.value()
        self.sleep_timers["after_typing"] = self.after_typing_spin.value()
        self.sleep_timers["after_enter"] = self.after_enter_spin.value()

        # Update start instantly option
        self.start_instantly = self.start_instantly_checkbox.isChecked()

        # Update auto close option and delay
        self.auto_close = self.auto_close_checkbox.isChecked()
        self.auto_close_delay = self.auto_close_delay_spin.value()

        # Handle startup on boot setting
        start_on_boot = self.start_on_boot_checkbox.isChecked()
        current_startup_status = StartupManager.check_startup_shortcut_exists()

        # Create or remove startup shortcut if needed
        if start_on_boot and not current_startup_status:
            if not StartupManager.create_startup_shortcut(self.application_path, self):
                self.start_on_boot_checkbox.setChecked(False)
        elif not start_on_boot and current_startup_status:
            if not StartupManager.remove_startup_shortcut(self):
                self.start_on_boot_checkbox.setChecked(True)

        # Save config
        self.config_manager.save_config(
            self.folders,
            self.sleep_timers,
            self.start_instantly,
            self,
            auto_close=self.auto_close,
            auto_close_delay=self.auto_close_delay
        )

    def open_folders(self):
        """Open the launcher application"""
        try:
            # Get the correct path based on execution environment
            if getattr(sys, 'frozen', False):
                # Packaged executable path
                launcher_path = os.path.join(self.application_path, "launcher.exe")
            else:
                # Development environment path
                launcher_path = os.path.join(self.application_path, "main_launcher.py")

            # Launch the executioner
            if os.path.exists(launcher_path):
                subprocess.Popen([launcher_path] if getattr(sys, 'frozen', False)
                                 else [sys.executable, launcher_path])
            else:
                raise FileNotFoundError("Launcher not found")

        except Exception as e:
            QMessageBox.critical(self, "Error",
                                 f"Could not open the launcher:\n{str(e)}")

    # Add these methods to your FolderOpenerConfigApp class:
    def on_folder_edited(self, item):
        """Handle when a folder path is edited in the list"""
        FolderOperations.edit_folder_path(item, self.folders_list, self.folders)

    def show_folder_context_menu(self, position):
        """Show context menu for folder items"""
        item = self.folders_list.itemAt(position)
        if not item:
            return

        context_menu = QMenu(self)

        # Add actions
        edit_action = context_menu.addAction("Edit Path")
        explore_action = context_menu.addAction("Open in Explorer")
        remove_action = context_menu.addAction("Remove")

        # Show the menu and get the selected action
        action = context_menu.exec(self.folders_list.mapToGlobal(position))

        # Handle the selected action
        if action == edit_action:
            self.folders_list.editItem(item)
        elif action == explore_action:
            try:
                folder_path = item.text()
                if os.path.exists(folder_path):
                    # Open the folder in Explorer
                    subprocess.Popen(f'explorer "{folder_path}"')
                else:
                    QMessageBox.warning(self, "Warning", f"The path '{folder_path}' doesn't exist.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open folder: {str(e)}")
        elif action == remove_action:
            index = self.folders_list.row(item)
            self.folders.pop(index)
            self.folders_list.takeItem(index)

    def update_folders_list(self):
        self.folders_list.clear()
        for folder in self.folders:
            item = QListWidgetItem(folder)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.folders_list.addItem(item)

    def show_about_dialog(self, event):
        dialog = AboutDialog(self)
        dialog.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderOpenerConfigApp()
    window.show()
    sys.exit(app.exec())
