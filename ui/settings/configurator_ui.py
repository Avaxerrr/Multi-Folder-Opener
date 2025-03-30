# configurator_ui.py

from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QDoubleSpinBox, QGridLayout, QGroupBox, QCheckBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.ui_components import ModernListWidget
from managers.theme_manager import ThemeManager
from managers.startup_manager import StartupManager
from ui.settings.ui_resources import UIResources
from ui.about_dialog import AboutDialog

class ConfiguratorUI:
    def __init__(self, dialog):
        self.dialog = dialog
        self.tooltips = UIResources.tooltips

    def setup_ui(self):
        # Header label
        self.header_label = QLabel("Configure Folders and Launch Settings")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.header_label.setFont(font)
        self.header_label.setContentsMargins(0, 0, 0, 10)
        self.dialog.main_layout.addWidget(self.header_label)

        # Subheader/description for delay settings
        self.delay_description = QLabel(
            "Adjust delay settings based on your system performance. "
            "Longer delays help ensure folders open properly without errors on slower systems.")
        self.delay_description.setWordWrap(True)
        self.delay_description.setContentsMargins(0, 0, 0, 10)
        self.dialog.main_layout.addWidget(self.delay_description)

        self._setup_folders_section()
        self._setup_timing_section()
        self._setup_options_section()
        self._setup_bottom_buttons()
        self._setup_author_label()

    def _setup_folders_section(self):
        # Create folders group
        folders_group = QGroupBox("Folders to Open")
        folders_layout = QVBoxLayout(folders_group)

        # Create list widget for folders with modern scrollbar
        self.folders_list = ModernListWidget()
        self.folders_list.setSelectionMode(ModernListWidget.SelectionMode.ExtendedSelection)
        from core.folder_operations import FolderOperations
        FolderOperations.update_folders_list(self.folders_list, self.dialog.folders)
        folders_layout.addWidget(self.folders_list)

        # editable view list
        self.folders_list.itemChanged.connect(self.dialog.handlers.on_folder_edited)
        self.folders_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.folders_list.customContextMenuRequested.connect(self.dialog.handlers.show_folder_context_menu)

        # Create folder buttons layout
        folder_buttons_layout = QHBoxLayout()

        # Add folder button
        self.add_button = QPushButton("Add Folders")
        self.add_button.clicked.connect(self.dialog.handlers.add_folders)
        folder_buttons_layout.addWidget(self.add_button)

        # Remove folder button
        self.remove_button = QPushButton("Remove Selected")
        self.remove_button.clicked.connect(self.dialog.handlers.remove_folder)
        folder_buttons_layout.addWidget(self.remove_button)

        # Move up button
        self.move_up_button = QPushButton("Move Up")
        self.move_up_button.clicked.connect(self.dialog.handlers.move_folder_up)
        folder_buttons_layout.addWidget(self.move_up_button)

        # Move down button
        self.move_down_button = QPushButton("Move Down")
        self.move_down_button.clicked.connect(self.dialog.handlers.move_folder_down)
        folder_buttons_layout.addWidget(self.move_down_button)

        folders_layout.addLayout(folder_buttons_layout)
        self.dialog.main_layout.addWidget(folders_group)

    def _setup_timing_section(self):
        # Create timing settings group
        timing_group = QGroupBox("Timing Settings (seconds)")
        timing_layout = QGridLayout(timing_group)

        # Explorer startup delay
        timing_layout.addWidget(QLabel("Explorer Startup Delay:"), 0, 0)
        self.explorer_startup_spin = QDoubleSpinBox()
        self.explorer_startup_spin.setRange(0.1, 5.0)
        self.explorer_startup_spin.setSingleStep(0.1)
        self.explorer_startup_spin.setValue(self.dialog.sleep_timers["explorer_startup"])
        self.explorer_startup_spin.setToolTip(self.tooltips["explorer_startup"])
        timing_layout.addWidget(self.explorer_startup_spin, 0, 1)

        # New tab delay
        timing_layout.addWidget(QLabel("New Tab Delay:"), 0, 2)
        self.new_tab_spin = QDoubleSpinBox()
        self.new_tab_spin.setRange(0.1, 5.0)
        self.new_tab_spin.setSingleStep(0.1)
        self.new_tab_spin.setValue(self.dialog.sleep_timers["new_tab"])
        self.new_tab_spin.setToolTip(self.tooltips["new_tab"])
        timing_layout.addWidget(self.new_tab_spin, 0, 3)

        # Address bar focus delay
        timing_layout.addWidget(QLabel("Address Bar Focus Delay:"), 1, 0)
        self.address_bar_spin = QDoubleSpinBox()
        self.address_bar_spin.setRange(0.1, 5.0)
        self.address_bar_spin.setSingleStep(0.1)
        self.address_bar_spin.setValue(self.dialog.sleep_timers["address_bar_focus"])
        self.address_bar_spin.setToolTip(self.tooltips["address_bar_focus"])
        timing_layout.addWidget(self.address_bar_spin, 1, 1)

        # After typing delay
        timing_layout.addWidget(QLabel("After Typing Delay:"), 1, 2)
        self.after_typing_spin = QDoubleSpinBox()
        self.after_typing_spin.setRange(0.1, 5.0)
        self.after_typing_spin.setSingleStep(0.1)
        self.after_typing_spin.setValue(self.dialog.sleep_timers["after_typing"])
        self.after_typing_spin.setToolTip(self.tooltips["after_typing"])
        timing_layout.addWidget(self.after_typing_spin, 1, 3)

        # After enter delay
        timing_layout.addWidget(QLabel("After Enter Delay:"), 2, 0)
        self.after_enter_spin = QDoubleSpinBox()
        self.after_enter_spin.setRange(0.1, 5.0)
        self.after_enter_spin.setSingleStep(0.1)
        self.after_enter_spin.setValue(self.dialog.sleep_timers["after_enter"])
        self.after_enter_spin.setToolTip(self.tooltips["after_enter"])
        timing_layout.addWidget(self.after_enter_spin, 2, 1)

        self.dialog.main_layout.addWidget(timing_group)

    def _setup_options_section(self):
        # Create options group
        options_group = QGroupBox("Launch Options")
        options_layout = QGridLayout(options_group)

        # Start instantly checkbox (left column)
        self.start_instantly_checkbox = QCheckBox("Start instantly when launched")
        self.start_instantly_checkbox.setChecked(self.dialog.start_instantly)
        self.start_instantly_checkbox.setToolTip(self.tooltips["start_instantly"])
        self.start_instantly_checkbox.setChecked(self.dialog.start_instantly)
        options_layout.addWidget(self.start_instantly_checkbox, 0, 0, Qt.AlignLeft)

        # Start on Windows boot checkbox (right column)
        self.start_on_boot_checkbox = QCheckBox("Start on Windows boot")
        self.start_on_boot_checkbox.setToolTip(self.tooltips["start_on_boot"])
        # Check if startup shortcut exists and set checkbox accordingly
        self.start_on_boot_checkbox.setChecked(StartupManager.check_startup_shortcut_exists())
        options_layout.addWidget(self.start_on_boot_checkbox, 0, 1, Qt.AlignRight)

        # Auto-close executioner checkbox (left column)
        self.auto_close_checkbox = QCheckBox("Auto-close the launcher when complete")
        self.auto_close_checkbox.setChecked(self.dialog.auto_close)
        self.auto_close_checkbox.setToolTip(self.tooltips["auto_close"])
        options_layout.addWidget(self.auto_close_checkbox, 1, 0, Qt.AlignLeft)

        # Auto-close delay layout (left column, below checkbox)
        auto_close_delay_layout = QHBoxLayout()
        auto_close_delay_layout.addWidget(QLabel("Close delay:"))
        self.auto_close_delay_spin = QDoubleSpinBox()
        self.auto_close_delay_spin.setRange(0.1, 10.0)
        self.auto_close_delay_spin.setSingleStep(0.1)
        self.auto_close_delay_spin.setValue(self.dialog.auto_close_delay)
        self.auto_close_delay_spin.setSuffix(" seconds")
        self.auto_close_delay_spin.setToolTip(self.tooltips["auto_close_delay"])
        auto_close_delay_layout.addWidget(self.auto_close_delay_spin)
        auto_close_delay_layout.addStretch(1)
        options_layout.addLayout(auto_close_delay_layout, 2, 0)

        self.dialog.main_layout.addWidget(options_group)

    def _setup_bottom_buttons(self):
        # Create bottom buttons layout
        bottom_buttons_layout = QHBoxLayout()

        # Save button
        self.save_button = QPushButton("Save Configuration")
        self.save_button.clicked.connect(self.dialog.save_config)
        bottom_buttons_layout.addWidget(self.save_button)

        self.dialog.main_layout.addLayout(bottom_buttons_layout)

    def _setup_author_label(self):
        # Create horizontal layout for author label
        author_layout = QHBoxLayout()
        author_layout.addStretch(1)  # Add stretch to push label to the right

        # Create the author label
        self.author_label = QLabel("Created by Avaxerrr")
        self.author_label.setStyleSheet("color: palette(text); text-decoration: underline; cursor: pointer;")
        self.author_label.setCursor(Qt.PointingHandCursor)
        self.author_label.mousePressEvent = self.show_about_dialog

        # Set font
        font = QFont()
        font.setItalic(True)
        self.author_label.setFont(font)

        # Add label to horizontal layout
        author_layout.addWidget(self.author_label)

        # Add horizontal layout to main layout
        self.dialog.main_layout.addLayout(author_layout)

    def setup_theme(self):
        ThemeManager.setup_theme(QApplication.instance(), self.save_button)

    def show_about_dialog(self, event):
        dialog = AboutDialog(self.dialog)
        dialog.exec()
