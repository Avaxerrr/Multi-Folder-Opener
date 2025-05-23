# config_manager.py

"""Version 1.1"""

import os
import json
from PySide6.QtWidgets import QMessageBox

from app_config import CONFIG_PATH


class ConfigManager:
    def __init__(self, config_path):
        self.config_path = CONFIG_PATH

    def load_config(self, parent_widget=None):
        # Default values
        folders = []
        sleep_timers = {
            "explorer_startup": 1.5,
            "new_tab": 0.5,
            "address_bar_focus": 0.5,
            "after_typing": 0.5,
            "after_enter": 0.5
        }
        start_instantly = False
        auto_close = False
        auto_close_delay = 3
        system_tray = False

        # Flag to indicate if this is first run or using default config
        is_first_run = False

        # Check if config file exists, if not create a default one
        if not os.path.exists(self.config_path):
            default_config = {
                "folders": [
                    "Your folder will display here...(Please delete this)"
                ],
                "sleep_timers": sleep_timers,
                "start_instantly": False,
                "auto_close": False,
                "auto_close_delay": 3,
                "system_tray": False
            }

            try:
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                folders = default_config['folders']
                sleep_timers = default_config['sleep_timers']
                start_instantly = default_config['start_instantly']
                auto_close = default_config['auto_close']
                auto_close_delay = default_config['auto_close_delay']
                system_tray = default_config['system_tray']

                # Set the first run flag to True
                is_first_run = True

            except Exception as e:
                if parent_widget:
                    QMessageBox.critical(parent_widget, "Error", f"Error creating config file: {e}")
                return folders, sleep_timers, start_instantly, auto_close, auto_close_delay, system_tray, is_first_run

        # Read config from file
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                folders = config.get('folders', [])

                # Check if folders list contains only default/placeholder entries
                if len(folders) <= 2 and any(folder.startswith("Add you folder") for folder in folders):
                    is_first_run = True

                # Normalize paths to Windows format
                folders = [os.path.normpath(folder) for folder in folders]

                # Load sleep timers if they exist, otherwise use defaults
                if 'sleep_timers' in config:
                    sleep_timers = config['sleep_timers']
                else:
                    # Add sleep_timers to existing config
                    config['sleep_timers'] = sleep_timers
                    with open(self.config_path, 'w') as f:
                        json.dump(config, f, indent=2)

                # Load start_instantly setting if it exists
                start_instantly = config.get('start_instantly', False)

                # Load auto_close setting if it exists
                auto_close = config.get('auto_close', False)

                # Load auto_close_delay setting if it exists
                auto_close_delay = config.get('auto_close_delay', 1.5)

                # Load system_tray setting if it exists
                system_tray = config.get('system_tray', False)

        except Exception as e:
            if parent_widget:
                QMessageBox.critical(parent_widget, "Error", f"Error loading config: {e}")

        return folders, sleep_timers, start_instantly, auto_close, auto_close_delay, system_tray, is_first_run

    def save_config(self, folders, sleep_timers, start_instantly, parent_widget=None, auto_close=False,
                    auto_close_delay=1.5, system_tray=False):
        try:
            # Normalize all folder paths to Windows format
            normalized_folders = [os.path.normpath(folder) for folder in folders]

            config = {
                "folders": normalized_folders,
                "sleep_timers": sleep_timers,
                "start_instantly": start_instantly,
                "auto_close": auto_close,
                "auto_close_delay": auto_close_delay,
                "system_tray": system_tray
            }

            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)

            if parent_widget:
                QMessageBox.information(parent_widget, "Success", "Configuration saved successfully!")
            return True
        except Exception as e:
            if parent_widget:
                QMessageBox.critical(parent_widget, "Error", f"Error saving config: {e}")
            return False