from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QMessageBox, QScrollArea, QWidget
import os

from managers.config_manager import ConfigManager
from managers.startup_manager import StartupManager
from ui.settings.configurator_ui import ConfiguratorUI
from ui.settings.configurator_handlers import ConfiguratorHandlers
from ui.ui_components import ModernScrollBar
from app_config import CONFIG_PATH, APP_ROOT


class ConfiguratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurator")
        self.setMinimumSize(700, 500)

        self.application_path = APP_ROOT
        self.config_path = CONFIG_PATH
        self.config_manager = ConfigManager(self.config_path)

        # Initialize folders list and sleep timers
        self.folders, self.sleep_timers, self.start_instantly, self.auto_close, self.auto_close_delay, self.system_tray, _ = self.config_manager.load_config(
            self)

        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBar(ModernScrollBar(Qt.Vertical, self.scroll_area))
        self.scroll_area.setHorizontalScrollBar(ModernScrollBar(Qt.Horizontal, self.scroll_area))

        # Create a widget to hold the content
        self.content_widget = QWidget()

        # Create main layout for the content
        self.main_layout = QVBoxLayout(self.content_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)

        # Set the content widget to the scroll area
        self.scroll_area.setWidget(self.content_widget)

        # Create a layout for the dialog
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(self.scroll_area)

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

        # Update options
        self.start_instantly = self.ui.start_instantly_checkbox.isChecked()
        self.auto_close = self.ui.auto_close_checkbox.isChecked()
        self.auto_close_delay = self.ui.auto_close_delay_spin.value()
        self.system_tray = self.ui.system_tray_checkbox.isChecked()

        # Check if shortcuts need to be created
        needs_shortcuts = (self.start_instantly or self.auto_close) and not self.system_tray

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

        # Create shortcuts if needed
        if needs_shortcuts:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            desktop_shortcut_path = os.path.join(desktop_path, "Multi Folder Opener.lnk")

            # Check if desktop shortcut already exists
            if not os.path.exists(desktop_shortcut_path):
                result = QMessageBox.question(
                    self,
                    "Create Shortcuts",
                    "The selected options could make the configurator difficult to access.\n\n"
                    "Would you like to create a desktop shortcut to ensure you can always access the configurator?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )

                if result == QMessageBox.No:
                    # User rejected shortcut creation, uncheck the problematic options
                    self.ui.start_instantly_checkbox.setChecked(False)
                    self.ui.auto_close_checkbox.setChecked(False)
                    self.start_instantly = False
                    self.auto_close = False

                    # Don't save and return
                    return False
                else:
                    # Create desktop shortcut
                    from managers.shortcut_manager import ShortcutManager
                    ShortcutManager.create_desktop_shortcut()

        # Save config
        saved = self.config_manager.save_config(
            self.folders,
            self.sleep_timers,
            self.start_instantly,
            self,
            auto_close=self.auto_close,
            auto_close_delay=self.auto_close_delay,
            system_tray=self.system_tray
        )

        if saved:
            self.accept()

        return saved

