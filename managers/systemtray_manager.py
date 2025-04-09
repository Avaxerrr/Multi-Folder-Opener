# systemtray_mananger.py (new)

"""Version 1.1"""

from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QInputDialog
from PySide6.QtGui import QIcon, QAction
import os


class SystemTrayManager:
    def __init__(self, main_app, launcher, configurator):
        self.main_app = main_app
        self.launcher = launcher
        self.configurator = configurator
        self.config_manager = main_app.config_manager
        self.tray_icon = None
        self.tray_menu = None
        self.setup_tray()

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self.main_app)
        icon_path = os.path.join(self.main_app.application_path, "icons", "launcher.ico")
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))

        self.tray_menu = QMenu()

        # Execute Folder Opening action
        execute_folders_action = self.tray_menu.addAction("Execute Folder Opening")
        execute_folders_action.triggered.connect(self.execute_folder_opening)

        self.tray_menu.addSeparator()

        # Main options
        open_launcher_action = self.tray_menu.addAction("Open Launcher")
        open_launcher_action.triggered.connect(self.show_launcher)

        open_configurator_action = self.tray_menu.addAction("Open Configurator")
        open_configurator_action.triggered.connect(self.open_configurator)

        self.tray_menu.addSeparator()

        # Launch Options submenu
        launch_options_menu = QMenu("Launch Options")
        self.tray_menu.addMenu(launch_options_menu)

        # Auto-close option with visible checkbox
        self.auto_close_action = QAction("Auto-Close", launch_options_menu)
        self.auto_close_action.setCheckable(True)
        self.auto_close_action.setChecked(self.main_app.auto_close)
        self.auto_close_action.triggered.connect(self.toggle_auto_close)
        launch_options_menu.addAction(self.auto_close_action)

        # Start instantly option with visible checkbox
        self.start_instantly_action = QAction("Start Instantly", launch_options_menu)
        self.start_instantly_action.setCheckable(True)
        self.start_instantly_action.setChecked(self.main_app.start_instantly)
        self.start_instantly_action.triggered.connect(self.toggle_start_instantly)
        launch_options_menu.addAction(self.start_instantly_action)

        # Configure delay option
        configure_delay_action = launch_options_menu.addAction("Configure Delay...")
        configure_delay_action.triggered.connect(self.configure_delay)

        # Exit option
        self.tray_menu.addSeparator()
        exit_action = self.tray_menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_application)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def execute_folder_opening(self):
        """Execute folder opening directly from the system tray"""
        self.main_app.log_manager.info("Executing folder opening from system tray")

        # Show launcher and then execute
        self.show_launcher()
        self.main_app.execute_folder_opening()

    def update_menu_state(self):
        """Update menu checkboxes to reflect current config"""
        self.auto_close_action.setChecked(self.main_app.auto_close)
        self.start_instantly_action.setChecked(self.main_app.start_instantly)

    def toggle_auto_close(self):
        """Toggle auto-close setting and save to config"""
        current_state = self.auto_close_action.isChecked()
        self.main_app.auto_close = current_state

        # Update config file
        folders, sleep_timers, start_instantly, _, auto_close_delay, system_tray, _ = self.config_manager.load_config()
        self.config_manager.save_config(
            folders,
            sleep_timers,
            start_instantly,
            None,  # parent_widget parameter
            current_state,  # autoclose parameter
            auto_close_delay,
            system_tray
        )
        self.main_app.log_manager.info(f"Auto-close setting changed to: {current_state}")

    def toggle_start_instantly(self):
        """Toggle start instantly setting and save to config"""
        current_state = self.start_instantly_action.isChecked()
        self.main_app.start_instantly = current_state

        # Update config file
        folders, sleep_timers, _, auto_close, auto_close_delay, system_tray, _ = self.config_manager.load_config()
        self.config_manager.save_config(
            folders,
            sleep_timers,
            current_state,  # start_instantly parameter
            None,  # parent_widget parameter
            auto_close,
            auto_close_delay,
            system_tray
        )
        self.main_app.log_manager.info(f"Start instantly setting changed to: {current_state}")

    def configure_delay(self):
        """Open dialog to configure auto-close delay"""
        current_delay = self.main_app.auto_close_delay
        delay, ok = QInputDialog.getInt(
            self.main_app,
            "Configure Auto-Close Delay",
            "Enter delay in seconds:",
            current_delay,
            1,
            60
        )

        if ok:
            self.main_app.auto_close_delay = delay

            # Update config file
            folders, sleep_timers, start_instantly, auto_close, _, system_tray, _ = self.config_manager.load_config()
            self.config_manager.save_config(
                folders,
                sleep_timers,
                start_instantly,
                None,  # parent_widget parameter
                auto_close,
                delay,  # auto_close_delay parameter
                system_tray
            )
            self.main_app.log_manager.info(f"Auto-close delay changed to: {delay} seconds")

    def show_tray_icon(self):
        if self.tray_icon:
            self.tray_icon.show()

    def hide_tray_icon(self):
        if self.tray_icon:
            self.tray_icon.hide()

    def toggle_tray_icon(self, state):
        if state:
            self.show_tray_icon()
        else:
            self.hide_tray_icon()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_launcher()

    def show_launcher(self):
        self.launcher.show()
        self.launcher.activateWindow()

    def open_configurator(self):
        self.configurator.open_configurator()

    def exit_application(self):
        QApplication.quit()

    def minimize_to_tray(self):
        self.launcher.hide()
        self.show_tray_icon()

    def update_menu_state(self):
        self.auto_close_action.setChecked(self.main_app.auto_close)
        self.start_instantly_action.setChecked(self.main_app.start_instantly)
