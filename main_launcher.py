# main_launcher.py (new)

import os
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon, QCloseEvent

from managers.log_manager import LogManager
from managers.dialog_manager import DialogManager
from managers.command_line_handler import CommandLineHandler
from managers.config_manager import ConfigManager
from managers.systemtray_manager import SystemTrayManager
from managers.theme_manager import ThemeManager
from managers.folder_opening_manager import FolderOpeningManager
from ui.main_window_ui import MainWindowUI
from app_config import CONFIG_PATH


class FolderOpenerExecutionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set application path
        if getattr(sys, 'frozen', False):
            self.application_path = os.path.dirname(sys.executable)
        else:
            self.application_path = os.path.dirname(os.path.abspath(__file__))

        # Parse command line arguments
        self.cmd_handler = CommandLineHandler()
        self.configure_mode = self.cmd_handler.is_configure_mode()

        # Initialize managers
        self.config_manager = ConfigManager(CONFIG_PATH)
        self.log_manager = LogManager()

        # Set application icon
        self.icon = None
        icon_path = os.path.join(self.application_path, 'icons', 'launcher.ico')
        if os.path.exists(icon_path):
            self.icon = QIcon(icon_path)
            QApplication.instance().setWindowIcon(self.icon)
            self.setWindowIcon(self.icon)

        # Initialize dialog manager with parent and icon
        self.dialog_manager = DialogManager(self, self.icon)

        # Load configuration
        self.load_config()

        # Initialize UI
        self.ui_manager = MainWindowUI(self, self.icon)
        ui_components = self.ui_manager.setup_ui()

        # Initialize system tray manager
        self.systemtray_manager = SystemTrayManager(self, self, self.dialog_manager)
        self.systemtray_manager.toggle_tray_icon(self.system_tray)

        # Set log widget for logger
        self.log_manager.set_log_widget(ui_components['log_text'])

        # Initialize folder opening manager
        self.folder_opening_manager = FolderOpeningManager(self, self.log_manager)
        self.folder_opening_manager.set_ui_components(
            ui_components['progress_bar'],
            ui_components['execute_button'],
            ui_components['cancel_button']
        )
        self.folder_opening_manager.set_config(
            self.folders,
            self.sleep_timers,
            self.auto_close,
            self.auto_close_delay
        )

        # Connect UI signals
        ui_components['execute_button'].clicked.connect(self.execute_folder_opening)
        ui_components['cancel_button'].clicked.connect(self.cancel_folder_opening)
        ui_components['open_configurator_button'].clicked.connect(self.open_configurator)
        ui_components['author_label'].mousePressEvent = self.show_about_dialog

        # Check for configurator command line argument
        if self.configure_mode:
            QTimer.singleShot(0, self.open_configurator_and_exit)
            return

        # Setup theme
        ThemeManager.setup_theme(
            QApplication.instance(),
            ui_components['execute_button'],
            ui_components['cancel_button']
        )
        app = QApplication.instance()
        app.paletteChanged.connect(self.on_palette_changed)

        # Start theme check timer
        self.current_theme = "light" if not ThemeManager.check_theme("light") else "dark"
        self.theme_timer = QTimer(self)
        self.theme_timer.timeout.connect(self.check_theme)
        self.theme_timer.start(2000)

        # Show system tray icon if enabled
        if self.system_tray:
            self.systemtray_manager.show_tray_icon()

        # Auto-start if configured
        if self.start_instantly:
            self.log_manager.info("Auto-execution enabled in config. Starting folder opening process...")
            self.execute_folder_opening()

        # Show welcome dialog for first run
        if self.is_first_run:
            self.dialog_manager.show_welcome_dialog()

    def closeEvent(self, event: QCloseEvent):
        """Override close event to handle system tray behavior"""
        if self.system_tray:
            self.log_manager.info("System tray enabled. Hiding to system tray instead of closing.")
            event.ignore()
            self.hide_to_system_tray()
        else:
            self.log_manager.info("Closing application.")
            event.accept()

    def load_config(self):
        """Load configuration from config manager"""
        self.folders, self.sleep_timers, self.start_instantly, self.auto_close, self.auto_close_delay, self.system_tray, self.is_first_run = self.config_manager.load_config()

    def reload_config(self):
        """Reload configuration after changes"""
        self.folders, self.sleep_timers, self.start_instantly, self.auto_close, self.auto_close_delay, self.system_tray, _ = self.config_manager.load_config()
        self.folder_opening_manager.set_config(
            self.folders,
            self.sleep_timers,
            self.auto_close,
            self.auto_close_delay
        )
        self.systemtray_manager.toggle_tray_icon(self.system_tray)
        self.systemtray_manager.update_menu_state()
        self.log_manager.info("Configuration reloaded.")

    def on_palette_changed(self, palette):
        """Handle system palette changes"""
        ThemeManager.on_palette_changed(
            QApplication.instance(),
            self.ui_manager.execute_button,
            self.ui_manager.cancel_button
        )

    def check_theme(self):
        """Periodically check for theme changes"""
        new_theme = ThemeManager.check_theme(self.current_theme)
        if new_theme != self.current_theme:
            self.current_theme = new_theme
            ThemeManager.setup_theme(
                QApplication.instance(),
                self.ui_manager.execute_button,
                self.ui_manager.cancel_button,
                True
            )

    def execute_folder_opening(self):
        """Start the folder opening process"""
        self.folder_opening_manager.execute_folder_opening()

    def cancel_folder_opening(self):
        """Cancel the folder opening process"""
        self.folder_opening_manager.cancel_folder_opening()

    def open_configurator(self):
        """Open the configurator dialog"""
        self.dialog_manager.open_configurator(self.reload_config)

    def open_configurator_and_exit(self):
        """Open configurator and exit when in command line mode"""
        self.dialog_manager.open_configurator_and_exit(QApplication.instance().quit)

    def show_about_dialog(self, event):
        """Show the about dialog"""
        self.dialog_manager.show_about_dialog()

    def on_folder_opening_complete(self):
        """Handle completion of folder opening process"""
        self.log_manager.info("Folder opening process completed.")

        # Check if auto-close is enabled
        if self.auto_close:
            self.log_manager.info(f"Auto-close enabled. Will close in {self.auto_close_delay} seconds.")

            # Check if system tray is enabled
            if self.system_tray:
                # Hide to system tray instead of closing
                QTimer.singleShot(int(self.auto_close_delay * 1000), self.hide_to_system_tray)
            else:
                # Close the application
                QTimer.singleShot(int(self.auto_close_delay * 1000), self.close_application)

    def hide_to_system_tray(self):
        """Hide the main window to system tray"""
        self.log_manager.info("Hiding to system tray.")
        self.systemtray_manager.minimize_to_tray()

    def close_application(self):
        """Close the application"""
        self.log_manager.info("Closing application.")
        if self.system_tray:
            self.systemtray_manager.exit_application()
        else:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderOpenerExecutionApp()
    if not ("--configure" in sys.argv or "-c" in sys.argv):
        window.show()
    sys.exit(app.exec())