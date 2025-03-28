# configurator.py

import os
import sys

from PySide6.QtWidgets import QDialog, QVBoxLayout
from PySide6.QtCore import Qt

from managers.config_manager import ConfigManager
from managers.startup_manager import StartupManager
from ui.settings.configurator_ui import ConfiguratorUI
from ui.settings.configurator_handlers import ConfiguratorHandlers
from app_config import CONFIG_PATH, APP_ROOT


class ConfiguratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurator")
        self.setMinimumSize(700, 500)

        self.application_path = APP_ROOT  # Use the centralized app root path
        self.config_path = CONFIG_PATH    # Use the centralized config path
        self.config_manager = ConfigManager(self.config_path)

        # Initialize folders list and sleep timers
        self.folders, self.sleep_timers, self.start_instantly, self.auto_close, self.auto_close_delay, _ = self.config_manager.load_config(
            self)

        # Create main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)

        # Setup UI and handlers
        self.ui = ConfiguratorUI(self)
        self.handlers = ConfiguratorHandlers(self)

        # Setup UI components
        self.ui.setup_ui()
        self.ui.setup_theme()

    def save_config(self):
        # Update sleep timers from UI
        self.sleep_timers["explorer_startup"] = self.ui.explorer_startup_spin.value()
        self.sleep_timers["new_tab"] = self.ui.new_tab_spin.value()
        self.sleep_timers["address_bar_focus"] = self.ui.address_bar_spin.value()
        self.sleep_timers["after_typing"] = self.ui.after_typing_spin.value()
        self.sleep_timers["after_enter"] = self.ui.after_enter_spin.value()

        # Update start instantly option
        self.start_instantly = self.ui.start_instantly_checkbox.isChecked()

        # Update auto close option and delay
        self.auto_close = self.ui.auto_close_checkbox.isChecked()
        self.auto_close_delay = self.ui.auto_close_delay_spin.value()

        # Handle startup on boot setting
        start_on_boot = self.ui.start_on_boot_checkbox.isChecked()
        current_startup_status = StartupManager.check_startup_shortcut_exists()

        # Create or remove startup shortcut if needed
        if start_on_boot and not current_startup_status:
            if not StartupManager.create_startup_shortcut(self):
                self.ui.start_on_boot_checkbox.setChecked(False)
        elif not start_on_boot and current_startup_status:
            if not StartupManager.remove_startup_shortcut(self):
                self.ui.start_on_boot_checkbox.setChecked(True)

        # Save config
        self.config_manager.save_config(
            self.folders,
            self.sleep_timers,
            self.start_instantly,
            self,
            auto_close=self.auto_close,
            auto_close_delay=self.auto_close_delay
        )
        self.accept()
