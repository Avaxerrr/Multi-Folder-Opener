# configurator_ui.py

from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                               QDoubleSpinBox, QGridLayout, QGroupBox, QCheckBox, QWidget,
                               QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.ui_components import ModernListWidget, ModernScrollBar
from managers.theme_manager import ThemeManager
from managers.startup_manager import StartupManager
from ui.settings.ui_resources import UIResources
from ui.about_dialog import AboutDialog
from ui.collapsible_section import CollapsibleSection
from core.folder_operations import FolderOperations


class ConfiguratorUI:
    def __init__(self, dialog):
        self.dialog = dialog
        self.tooltips = UIResources.tooltips

    def setup_ui(self):
        # Header
        header_widget = self.create_header()
        self.dialog.main_layout.addWidget(header_widget)

        # Scrollable content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)

        # Add modern scrollbars
        scroll_area.setVerticalScrollBar(ModernScrollBar(Qt.Vertical, scroll_area))
        scroll_area.setHorizontalScrollBar(ModernScrollBar(Qt.Horizontal, scroll_area))

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 5, 10, 5)
        content_layout.setSpacing(10)
        self.setup_content(content_layout)
        scroll_area.setWidget(content_widget)
        self.dialog.main_layout.addWidget(scroll_area, 1)  # Add stretch factor

        # Footer
        footer_widget = self.create_footer()
        self.dialog.main_layout.addWidget(footer_widget)

    def create_header(self):
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 5)

        title_label = QLabel("Configure Folders and Launch Settings")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        title_label.setFont(font)
        header_layout.addWidget(title_label)

        description_label = QLabel("Adjust delay settings based on your system performance. "
                                   "Longer delays help ensure folders open properly without errors on slower systems.")
        description_label.setWordWrap(True)
        header_layout.addWidget(description_label)

        return header_widget

    def setup_content(self, layout):
        # Folders section
        self.setup_folders_section(layout)

        # Timing settings section
        self.timing_section = CollapsibleSection("Timing Settings (seconds)")
        self.setup_timing_section()
        layout.addWidget(self.timing_section)

        # Launch options section
        self.options_section = CollapsibleSection("Launch Options")
        self.setup_options_section()
        layout.addWidget(self.options_section)

    def setup_folders_section(self, parent_layout):
        folders_group = QGroupBox("Folders to Open")
        folders_layout = QVBoxLayout(folders_group)

        # Create list widget for folders
        self.folders_list = ModernListWidget()
        self.folders_list.setSelectionMode(ModernListWidget.SelectionMode.ExtendedSelection)
        FolderOperations.update_folders_list(self.folders_list, self.dialog.folders)
        folders_layout.addWidget(self.folders_list)

        # Set up folder list behavior
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
        parent_layout.addWidget(folders_group)

    def setup_timing_section(self):
        # Create timing widget and layout
        timing_widget = QWidget()
        timing_layout = QGridLayout(timing_widget)

        # Explorer startup delay
        explorer_label = QLabel("Explorer Startup Delay:")
        explorer_label.setToolTip(self.tooltips["explorer_startup"])
        timing_layout.addWidget(explorer_label, 0, 0)
        self.explorer_startup_spin = QDoubleSpinBox()
        self.explorer_startup_spin.setRange(0.1, 5.0)
        self.explorer_startup_spin.setSingleStep(0.1)
        self.explorer_startup_spin.setValue(self.dialog.sleep_timers["explorer_startup"])
        self.explorer_startup_spin.setToolTip(self.tooltips["explorer_startup"])
        timing_layout.addWidget(self.explorer_startup_spin, 0, 1)

        # New tab delay
        new_tab_label = QLabel("New Tab Delay:")
        new_tab_label.setToolTip(self.tooltips["new_tab"])
        timing_layout.addWidget(new_tab_label, 0, 2)
        self.new_tab_spin = QDoubleSpinBox()
        self.new_tab_spin.setRange(0.1, 5.0)
        self.new_tab_spin.setSingleStep(0.1)
        self.new_tab_spin.setValue(self.dialog.sleep_timers["new_tab"])
        self.new_tab_spin.setToolTip(self.tooltips["new_tab"])
        timing_layout.addWidget(self.new_tab_spin, 0, 3)

        # Address bar focus delay
        address_bar_label = QLabel("Address Bar Focus Delay:")
        address_bar_label.setToolTip(self.tooltips["address_bar_focus"])
        timing_layout.addWidget(address_bar_label, 1, 0)
        self.address_bar_spin = QDoubleSpinBox()
        self.address_bar_spin.setRange(0.1, 5.0)
        self.address_bar_spin.setSingleStep(0.1)
        self.address_bar_spin.setValue(self.dialog.sleep_timers["address_bar_focus"])
        self.address_bar_spin.setToolTip(self.tooltips["address_bar_focus"])
        timing_layout.addWidget(self.address_bar_spin, 1, 1)

        # After typing delay
        after_typing_label = QLabel("After Typing Delay:")
        after_typing_label.setToolTip(self.tooltips["after_typing"])
        timing_layout.addWidget(after_typing_label, 1, 2)
        self.after_typing_spin = QDoubleSpinBox()
        self.after_typing_spin.setRange(0.1, 5.0)
        self.after_typing_spin.setSingleStep(0.1)
        self.after_typing_spin.setValue(self.dialog.sleep_timers["after_typing"])
        self.after_typing_spin.setToolTip(self.tooltips["after_typing"])
        timing_layout.addWidget(self.after_typing_spin, 1, 3)

        # After enter delay
        after_enter_label = QLabel("After Enter Delay:")
        after_enter_label.setToolTip(self.tooltips["after_enter"])
        timing_layout.addWidget(after_enter_label, 2, 0)
        self.after_enter_spin = QDoubleSpinBox()
        self.after_enter_spin.setRange(0.1, 5.0)
        self.after_enter_spin.setSingleStep(0.1)
        self.after_enter_spin.setValue(self.dialog.sleep_timers["after_enter"])
        self.after_enter_spin.setToolTip(self.tooltips["after_enter"])
        timing_layout.addWidget(self.after_enter_spin, 2, 1)

        # Add the widget to the collapsible section
        self.timing_section.add_widget(timing_widget)

    def setup_options_section(self):
        # Create options widget and layout
        options_widget = QWidget()
        options_layout = QVBoxLayout(options_widget)

        # System Access Options section
        system_access_label = QLabel("System Access Options:")
        font = QFont()
        font.setBold(True)
        system_access_label.setFont(font)
        options_layout.addWidget(system_access_label)

        # System tray checkbox
        self.system_tray_checkbox = QCheckBox("Run in system tray")
        self.system_tray_checkbox.setChecked(self.dialog.system_tray)
        if "system_tray" in self.tooltips:
            self.system_tray_checkbox.setToolTip(self.tooltips["system_tray"])
        else:
            self.system_tray_checkbox.setToolTip("Run the application in system tray for easy access")
        options_layout.addWidget(self.system_tray_checkbox)

        # Start on Windows boot checkbox
        self.start_on_boot_checkbox = QCheckBox("Start on Windows boot")
        self.start_on_boot_checkbox.setToolTip(self.tooltips["start_on_boot"])
        self.start_on_boot_checkbox.setChecked(StartupManager.check_startup_shortcut_exists())
        options_layout.addWidget(self.start_on_boot_checkbox)

        # Add some spacing
        options_layout.addSpacing(10)

        # Quick Launch Options section
        quick_launch_label = QLabel("Quick Launch Options:")
        quick_launch_label.setFont(font)
        options_layout.addWidget(quick_launch_label)

        # Note about shortcuts
        shortcut_note = QLabel(
            "Note: Enabling these options will automatically create shortcuts to ensure you can always access the configurator.")
        shortcut_note.setWordWrap(True)
        shortcut_note.setStyleSheet("color: #666; font-style: italic;")
        options_layout.addWidget(shortcut_note)

        # Start instantly checkbox
        self.start_instantly_checkbox = QCheckBox("Start instantly when launched")
        self.start_instantly_checkbox.setChecked(self.dialog.start_instantly)
        self.start_instantly_checkbox.setToolTip(self.tooltips["start_instantly"])
        options_layout.addWidget(self.start_instantly_checkbox)

        # Auto-close checkbox and delay
        auto_close_layout = QVBoxLayout()
        self.auto_close_checkbox = QCheckBox("Auto-close the launcher when complete")
        self.auto_close_checkbox.setChecked(self.dialog.auto_close)
        self.auto_close_checkbox.setToolTip(self.tooltips["auto_close"])
        auto_close_layout.addWidget(self.auto_close_checkbox)

        # Auto-close delay layout
        auto_close_delay_layout = QHBoxLayout()
        auto_close_delay_layout.addSpacing(20)  # Indent
        auto_close_delay_layout.addWidget(QLabel("Close delay:"))
        self.auto_close_delay_spin = QDoubleSpinBox()
        self.auto_close_delay_spin.setRange(0.1, 10.0)
        self.auto_close_delay_spin.setSingleStep(0.1)
        self.auto_close_delay_spin.setValue(self.dialog.auto_close_delay)
        self.auto_close_delay_spin.setSuffix(" seconds")
        self.auto_close_delay_spin.setToolTip(self.tooltips["auto_close_delay"])
        auto_close_delay_layout.addWidget(self.auto_close_delay_spin)
        auto_close_delay_layout.addStretch(1)
        auto_close_layout.addLayout(auto_close_delay_layout)

        options_layout.addLayout(auto_close_layout)

        # System tray behavior note
        system_tray_note = QLabel(
            "When system tray is enabled, auto-close will hide the launcher instead of quitting it.")
        system_tray_note.setWordWrap(True)
        system_tray_note.setStyleSheet("color: #666; font-style: italic;")
        options_layout.addWidget(system_tray_note)

        # Connect signals for checkbox interactions
        self.system_tray_checkbox.stateChanged.connect(self.on_system_tray_changed)
        self.auto_close_checkbox.stateChanged.connect(self.on_auto_close_changed)

        # Add the widget to the collapsible section
        self.options_section.add_widget(options_widget)

    def create_footer(self):
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(10, 5, 10, 10)

        self.author_label = QLabel("Created by Avaxerrr")
        self.author_label.setStyleSheet("color: palette(text); text-decoration: underline; cursor: pointer;")
        self.author_label.setCursor(Qt.PointingHandCursor)
        self.author_label.mousePressEvent = self.show_about_dialog

        # Set font
        font = QFont()
        font.setItalic(True)
        self.author_label.setFont(font)

        # Add author label to the left side
        footer_layout.addWidget(self.author_label)

        # Add stretch to push buttons to the right
        footer_layout.addStretch(1)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.dialog.save_config)
        footer_layout.addWidget(self.save_button)

        # Close button (doesn't save)
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.dialog.reject)
        footer_layout.addWidget(self.close_button)

        return footer_widget

    def on_system_tray_changed(self):
        # Update auto-close behavior description based on system tray state
        pass

    def on_auto_close_changed(self):
        # Enable/disable auto-close delay spin box based on checkbox state
        self.auto_close_delay_spin.setEnabled(self.auto_close_checkbox.isChecked())

    def setup_theme(self):
        ThemeManager.setup_theme(QApplication.instance(), self.save_button, self.close_button)

    def show_about_dialog(self, event):
        dialog = AboutDialog(self.dialog)
        dialog.exec()
